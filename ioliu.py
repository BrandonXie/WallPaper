# -*- coding: utf-8 -*- 
import urllib2
import re
import os.path
import hashlib
import threading


url = "http://bing.ioliu.cn"

# 匹配文本
def findStrs(content,compileStr):
    pattern = re.compile(compileStr)
    return pattern.findall(content)

# 下载文件
def downloadPicture(link):
    try:
        req = urllib2.build_opener().open(link,timeout=5)
        meta = req.info()
    except Exception,e:
        print "get name fail:"+link
    content = meta.getheaders("Content-Disposition")[0]
    dis=findStrs(content,'filename=(.+)')[0]
    name = hashlib.md5(os.path.splitext(dis)[0].encode('utf-8')).hexdigest()
    stuff = os.path.splitext(dis)[1]
    fileName = fileDir+name+stuff
    
    if not os.path.exists(fileName):
        try:
            f = urllib2.urlopen(link,timeout=10)
            data = f.read()
            with open(fileName, "wb") as code:     
                code.write(data)
        except Exception,e:
            print "download fail:"+link

# 获取下载列表
def requestPictureUrl(request):
    try:
        response = urllib2.urlopen(request,timeout=5)
        home = response.read().decode("utf-8")
        urls=findStrs(home,'href="(.+?)"')
        for link in urls:
            if link.endswith('=download'):
                link = url+link
                downloadPicture(link)
    except Exception,e:
        print "request fail:"+request


if __name__ == '__main__':
    fileDir = 'C:\\Users\\Administrator\\Pictures\\Camera Roll\\'
    page = '?p='
    for index in range(55,1,-1):
        requestPictureUrl(url+page+str(index))
    print 'this is over'

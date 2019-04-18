#!/bin/env python3.6
#-*- coding: UTF-8 -*-

# 该脚本可以定位访问web页面的服务质量
# 通过Python下的pycurl模块来实现定位
# 它可以通过调用pycurl提供的方法，来探测Web服务质量
# 比如了解相应的HTTP状态码、请求延时、HTTP头信息、下载速度等


import os
import time
import sys
import pycurl
import certifi

#探测目标URL
URL = "https://www.taobao.com/"

#创建一个Curl对象
detect_object = pycurl.Curl()

#处理https需要
detect_object.setopt(pycurl.CAINFO, certifi.where())

# 定义请求的URL变量
detect_object.setopt(pycurl.URL, URL)
# 定义请求链接的等待时间
detect_object.setopt(pycurl.CONNECTTIMEOUT, 5)
# 定义请求超时的时间
detect_object.setopt(pycurl.TIMEOUT, 5)
# 屏蔽下载进度条
detect_object.setopt(pycurl.FORBID_REUSE, 1)
# 指定HTTP重定向的最大数为1
detect_object.setopt(pycurl.MAXREDIRS, 1)
# 完成交互后强制断开链接，不重用
detect_object.setopt(pycurl.NOPROGRESS, 1)
# 设置保存DNS信息的时间为30秒
detect_object.setopt(pycurl.DNS_CACHE_TIMEOUT, 30)


#创建一个文件对象，以“wb”方式打开，用来存储返回的http头部及页面的内容
indexfile = open(os.path.dirname(os.path.realpath(__file__))+"/content.txt", "wb")
# 将返回的HTTP HEADER 定向到indexfile文件
detect_object.setopt(pycurl.WRITEHEADER, indexfile)
# 将返回的HTML内容定向到indexfile文件
detect_object.setopt(pycurl.WRITEDATA, indexfile)


# 捕捉Curl.perform请求的提交，如果错误直接退出
try:
    detect_object.perform()
except Exception as e:
    print("链接错误")
    indexfile.close()
    detect_object.close()
    sys.exit()

# DNS解析所消耗的时间
NAMELOOKUP_TIME = detect_object.getinfo(detect_object.NAMELOOKUP_TIME)
# 建立连接所消耗的时间（运程服务器连接时间）
CONNECT_TIME = detect_object.getinfo(detect_object.CONNECT_TIME)
# 从建立连接到准备传输所消耗的时间
PRETRANSFER_TIME = detect_object.getinfo(detect_object.PRETRANSFER_TIME)
# 从建立连接到传输开始消耗的时间
STARTTRANSFER_TIME = detect_object.getinfo(detect_object.STARTTRANSFER_TIME)
# 传输结束所消耗的总时间
TOTAL_TIME = detect_object.getinfo(detect_object.TOTAL_TIME)
# 返回HTTP状态吗
HTTP_CODE = detect_object.getinfo(detect_object.HTTP_CODE)
# 下载数据包的大小
SIZE_DOWNLOAD = detect_object.getinfo(detect_object.SIZE_DOWNLOAD)
# HTTP头部大小
HEADER_SIZE = detect_object.getinfo(detect_object.HEADER_SIZE)
# 平均下载速度
SPEED_DOWNLOAD = detect_object.getinfo(detect_object.SPEED_DOWNLOAD)


print("HTTP状态码：%d\n\
DNS解析时间：%.2f ms\n\
建立连接时间：%.2f ms\n\
准备传输时间：%.2f ms\n\
传输开始时间：%.2f ms\n\
传输结束总时间：%.2f ms\n\
下载数据包大小：%d bytes\n\
HTTP头部大小：%d bytes\n\
平均下载速度：%d bytes/s\n"\
%(HTTP_CODE, NAMELOOKUP_TIME*1000, CONNECT_TIME*1000, PRETRANSFER_TIME*1000, STARTTRANSFER_TIME*1000,\
    TOTAL_TIME*1000, SIZE_DOWNLOAD, HEADER_SIZE, SPEED_DOWNLOAD))

indexfile.close()
detect_object.close()
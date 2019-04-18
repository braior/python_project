#!/bin/env python3
#-*- code:utf-8 -*-

import psutil
import time

#网卡，可以得到网卡属性，连接数，当前流量等信息
net = psutil.net_io_counters()
print(net)
bytes_sent = '{0:.2f}Mb'.format(net.bytes_sent /1024/1024)
bytes_rcvd = '{0:.2f}Mb'.format(net.bytes_recv / 1024/1024)

print('网卡接收流量%s 网卡发送流量%s' % (bytes_rcvd, bytes_sent))
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: braior
# Date: 2020/1/2

import sys
import importlib
import time, datetime
import pymysql
import xlsxwriter
import smtplib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

importlib.reload(sys)

zbx_host = '172.20.0.3'
zbx_port = 3306
zbx_username = 'root'
zbx_password = '123456'
zbx_dbname = 'zabbixdb'

# 需要查询的服务器所在的组名
groupname = '线上服务器组'

# 文件产生日期
date = time.strftime("%Y%m%d", time.localtime())

# 文件名称
xls_fname = 'Zabbix_Report_weekly_%s.xls' % date
csv_fname = 'Zabbix_Report_weekly_%s.csv' % date

keys = [
    ['CPU5分钟负载', 'trends', 'system.cpu.load[all,avg5]', 'avg', '%.2f', 1, ''],
    ['CPU平均空闲值', 'trends', 'system.cpu.util[,idle]', 'avg', '%.2f', 1, ''],
    ['CPU最小空闲值', 'trends', 'system.cpu.util[,idle]', 'min', '%.2f', 1, ''],
    ['swap总大小(单位G)', 'trends_uint', 'system.swap.size[,total]', 'avg', '', 1073741824, 'G'],
    ['swap平均剩余(单位G)', 'trends_uint', 'system.swap.size[,free]', 'avg', '', 1073741824, 'G'],
    ['根分区总大小(单位G)', 'trends_uint', 'vfs.fs.size[/,total]', 'avg', '', 1073741824, 'G'],
    ['根分区剩余(单位G)', 'trends_uint', 'vfs.fs.size[/,free]', 'avg', '', 1073741824, 'G'],
    ['物理内存总大小(单位G)', 'trends_uint', 'vm.memory.size[total]', 'avg', '', 1073741824, 'G'],
    ['物理内存可用(单位G)', 'trends_uint', 'vm.memory.size[available]', 'avg', '', 1073741824, 'G'],
    ['物理内存已使用(单位G)', 'trends_uint', 'vm.memory.size[used]', 'avg', '', 1073741824, 'G'],
    ['网卡进口流量(单位Kbps)', 'trends_uint', 'net.if.in[eth0]', 'avg', '', 1024, 'Kbps'],
    ['网卡进口流量(单位Kbps)', 'trends_uint', 'net.if.in[em1]', 'avg', '', 1024, 'Kbps'],
    ['网卡出口流量(单位Kbps)', 'trends_uint', 'net.if.out[eth0]', 'avg', '', 1024, 'Kbps'],
    ['网卡出口流量(单位Kbps)', 'trends_uint', 'net.if.out[em1]', 'avg', '', 1024, 'Kbps'],
    ['data分区总大小(单位G)', 'trends_uint', 'vfs.fs.size[/data,total]', 'avg', '', 1073741824, 'G'],
    ['data分区剩余(单位G)', 'trends_uint', 'vfs.fs.size[/data,free]', 'avg', '', 1073741824, 'G'],
]

Title_dict = {
    'CPU5分钟负载': 1,
    'CPU平均空闲值': 2,
    'CPU最小空闲值': 3,
    'swap总大小(单位G)': 4,
    'swap平均剩余(单位G)': 5,
    'Swap剩余率(单位%)': 6,
    '根分区总大小(单位G)': 7,
    '根分区剩余(单位G)': 8,
    '根分区剩余率(单位%)': 9,
    '物理内存总大小(单位G)': 10,
    '物理内存可用(单位G)': 11,
    '物理内存已使用(单位G)': 12,
    '物理内存使用率(单位%)': 13,
    '网卡出口流量(单位Kbps)': 14,
    '网卡进口流量(单位Kbps)': 15,
    'data分区总大小(单位G)': 16,
    'data分区剩余(单位G)': 17,
    'data分区剩余率(单位%)': 18
}

Title = [
    '主机名',
    'CPU5分钟负载',
    'CPU平均空闲值',
    'CPU最小空闲值',
    'swap总大小(单位G)',
    'swap平均剩余(单位G)',
    'Swap剩余率(单位%)',
    '根分区总大小(单位G)',
    '根分区剩余(单位G)',
    '根分区剩余率(单位%)',
    '物理内存总大小(单位G)',
    '物理内存可用(单位G)',
    '物理内存已使用(单位G)',
    '物理内存使用率(单位%)',
    '网卡出口流量(单位Kbps)',
    '网卡进口流量(单位Kbps)',
    'data分区总大小(单位G)',
    'data分区剩余(单位G)',
    'data分区剩余率(单位%)',
]

keys_cpu= Title[1]

disk_full = Title[7]
disk_free = Title[8]
keys_disk = Title[9]

swap_full = Title[4]
swap_free = Title[5]
keys_swap = Title[6]

mem_full = Title[10]
mem_free = Title[11]
mem_used = Title[12]
keys_mem = Title[13]

data_full = Title[16]
data_free = Title[17]
keys_data = Title[18]


class Report(object):
    def __init__(self):
        self.conn = pymysql.connect(host=zbx_host, port=zbx_port, user=zbx_username, passwd=zbx_password, db=zbx_dbname)
        self.cursor = self.conn.cursor()
    
    def getgroupid(self):
        # 将要执行的sql语句
        sql = "select groupid from hstgrp where name='%s'" % groupname
        # 执行sql语句
        self.cursor.execute(sql)

        # 首先fetchone()函数它的返回值是单个的元组,也就是一行记录,如果没有结果,那就会返回null
        # 其次是fetchall()函数,它的返回值是多个元组,即返回多个行记录,如果没有结果,返回的是()
        # groupid = self.cursor.fetchone()['groupid']
        groupid = self.cursor.fetchone()[0]

        # print(groupid)
        return groupid

    def gethostid(self):
        groupid = self.getgroupid()
        sql = "select hostid from hosts_groups where groupid='%s'" % groupid
        self.cursor.execute(sql)
        hostid_list = self.cursor.fetchall()

        # print(hostid_list)
        return hostid_list

    def gethostlist(self):
        host_list = {}
        hostid_list = self.gethostid()
        
        for item in hostid_list:
            # print(item)
            # hostid = item['hostid']
            hostid = item[0]
            sql = "select host from hosts where status=0 and flags=0 and hostid=%s" % hostid
            self.cursor.execute(sql)
            host_name = self.cursor.fetchone()
            # print(host_ip)

            #！！！判断如果主机被zabbix改成disable的状态时，hosts表格里面host变为空后，字典空键赋值报错《TypeError: 'NoneType' object has no attribute '__getitem__'》
            if host_name is None:
                continue
            # host_list[host_ip['host']] = {'hostid': hostid}
            host_list[host_name[0]] = {'hostid': hostid}

        # print(host_list)
        return host_list

    def getitemid(self):
        hostid_list = self.gethostlist()
        keys_dict = {}
        for hostitem in hostid_list.items():
            # print(hostitem)
            hostname = hostitem[0]
            hostid = hostitem[1]['hostid']
            host_info = []
            for item in keys:
                keys_list = []
                keys_list.append({'title': item[0]})
                keys_list.append({'table': item[1]})
                keys_list.append({'itemname': item[2]})
                keys_list.append({'value': item[3]})
                keys_list.append({'form': item[4]})
                keys_list.append({'ratio': item[5]})
                keys_list.append({'unit': item[6]})

                # print(keys_list)

                itemname = item[2]
                sql = "select itemid from items where hostid='%s' and key_='%s'" % (hostid, itemname)
                self.cursor.execute(sql)
                itemid = self.cursor.fetchone()
                if itemid is None:
                    continue
                keys_list.append(itemid)
                # print(keys_list)
                host_info.append(tuple(keys_list))
                # print(host_info)
            keys_dict[hostname] = host_info
        # print(keys_dict)
        return keys_dict

    def getvalue(self):
        # 时间为七天内
        stoptime = 1577980800 - 7*24*60*60
        # starttime = time.time()
        # 起始时间点:2020-01-03 00:00:00
        starttime = 1577980800
        host_info_list = self.getitemid()
        host_dict = {}
        for ip in host_info_list:
            host_info = host_info_list[ip]
            # print(host_info)
            length = len(host_info)
            host_item = {}
            for i in range(length):
                value = host_info[i][3]['value']
                ratio = host_info[i][5]['ratio']
                table = host_info[i][1]['table']
                # itemid = host_info[i][7]['itemid']
                itemid = host_info[i][7][0]
                # itemname = host_info[i][2]['itemname']
                unit = host_info[i][6]['unit']
                title = host_info[i][0]['title']
                sql = "select avg(value_%s)/%s result from %s where itemid=%s and clock<=%d and clock>=%d" % (
                    value, ratio, table, itemid, starttime, stoptime)
                self.cursor.execute(sql)
                # result = self.cursor.fetchone()['result']
                result = self.cursor.fetchone()[0]
                if result is None:
                    continue
                else:
                    host_item[title] = '%.2f%s' % (result, unit)
            
            print(host_item)
            # /硬盘剩余率
            if disk_full in host_item and disk_free in host_item:
                # print("Disk_percent:%.2f%%" %(float(host_item[disk_free].strip("GKbps"))/float(host_item[disk_full].strip("GKbps"))*100))
                host_item[keys_disk] = "%.2f" % (
                    float(host_item[disk_free].strip("GKbps")) / float(host_item[disk_full].strip("GKbps")) * 100)
            # data硬盘剩余率
            if data_full in host_item and data_free in host_item:
                # print("Disk_percent:%.2f%%" %(float(host_item[data_free].strip("GKbps"))/float(host_item[data_full].strip("GKbps"))*100))
                host_item[keys_data] = "%.2f" % (
                    float(host_item[data_free].strip("GKbps")) / float(host_item[data_full].strip("GKbps")) * 100)
            # Swap剩余率
            if swap_full in host_item and swap_free in host_item:
                # print(host_item[swap_full, host_item[swap_free]])
                # print("Swap_percent:%.2f%%" %(float(host_item[swap_full].strip("GKbps"))/float(host_item[swap_full].strip("GKbps"))*100))
                if(int(float(host_item[swap_full].strip("GKbps"))) != 0):
                    host_item[keys_swap] = "%.2f" % (
                        float(host_item[swap_free].strip("GKbps")) / float(host_item[swap_full].strip("GKbps")) * 100)
                else:
                    host_item[swap_full], host_item[swap_free] = "", ""
                    host_item[keys_swap] = ""
            # 内存使用率
            if mem_free in host_item and mem_full in host_item:
                # print("Mem_percent:%.2f%%" %(float(host_item[mem_used].strip("GKbps")) / float(host_item[mem_full].strip("GKbps")) * 100))
                host_item[mem_used] = "%.2f" % (float(host_item[mem_full].strip("GKbps")) - float(host_item[mem_free].strip("GKbps")))
                print(host_item[mem_used])
                host_item[keys_mem] = "%.2f" % (float(host_item[mem_used]) / float(host_item[mem_full].strip("GKbps")) * 100)
            host_dict[ip] = host_item
        print(host_dict)
        return host_dict

    def dispalyvalue(self):
        value = self.getvalue()
        for ip in value:
            print("\n\rip:%s\n\r获取服务器信息:" % (ip))
            for key in value[ip]:
                print("%s:%s" %(key,value[ip][key]))

    def __del__(self):
        #关闭数据库连接
        self.cursor.close()
        self.conn.close()

    def createreport_csv(self):
        host_name_list = []
        data_list = []
        host_info = self.getvalue()
        # print(host_info)
        df = pd.DataFrame(columns=Title)

        for host_name in host_info:
           app = list(host_info[host_name].values())
           app.insert(0, host_name)
           app.insert(1, 0)
           data_list.append(app)
               
        # print(data_list)
        data_list.insert(0, Title)
        df = pd.DataFrame(data_list)
        df.to_csv("result.csv", index=None)

    def createreport(self):
        host_info = self.getvalue()

        # 创建一个excel表格
        
        workbook = xlsxwriter.Workbook(xls_fname)
        # 设置第一行标题格式
        format_title = workbook.add_format()
        format_title.set_border(1)  # 边框
        format_title.set_bg_color('#1ac6c0')  # 背景颜色
        format_title.set_align('center')  # 左右居中
        format_title.set_bold()  # 字体加粗
        format_title.set_valign('vcenter')  # 上下居中
        format_title.set_font_size(12)
        # 设置返回值的格式
        format_value = workbook.add_format()
        format_value.set_border(1)
        format_value.set_align('center')
        format_value.set_valign('vcenter')
        format_value.set_font_size(12)


        # 创建一个名为Report的工作表
        worksheet1 = workbook.add_worksheet("总览表格")
        # 设置列宽
        worksheet1.set_column('A:D', 15)
        worksheet1.set_column('E:J', 23)
        worksheet1.set_column('K:P', 25)
        # 设置行高
        worksheet1.set_default_row(25)
        # 冻结首行首列
        worksheet1.freeze_panes(1, 1)
        # 将标题写入第一行
        i = 0
        for title in Title:
            # worksheet1.write(0, i, title.decode('utf-8'), format_title)
            worksheet1.write(0, i, title, format_title)
            i += 1
        # 写入第一列、第一行
        # worksheet1.write(0, 0, "主机".decode('utf-8'), format_title)
        # worksheet1.write(0, 0, "主机", format_title)
        # 根据每个ip写入相应的数值
        j = 1
        for ip in host_info:
            keys_ip = sorted(host_info[ip])  # 取出每个ip的键值，并把键值进行排序
            host_value = host_info[ip]  # 取出没有排序的键值
            if len(host_value) != 0:  # 如果出现｛'10.1.12.1':{}｝这种情况的时候，需要跳过，不将其写入表格中
                worksheet1.write(j, 0, ip, format_value)
            else:
                continue
            # k = 1
            # print(keys_ip)
            for item in keys_ip:
                # worksheet1.write(j,k,host_value[item],format_value)
                worksheet1.write(j, Title_dict[item], host_value[item], format_value)
                # k += 1
            j += 1

##########################性能报表#############################
        worksheet2 = workbook.add_worksheet("性能报表")
        # 设置列宽
        worksheet2.set_column('A:E', 25)
        # 设置行高
        worksheet2.set_default_row(25)
        # 冻结首行首列
        worksheet2.freeze_panes(1, 1)
        # 写入第一列、第一行
        worksheet2.write(0, 0, "主机", format_title)
        worksheet2.write(0, 1, keys_cpu, format_title)
        worksheet2.write(0, 2, keys_mem, format_title)
        worksheet2.write(0, 3, keys_swap, format_title)
        worksheet2.write(0, 4, keys_disk, format_title)
        worksheet2.write(0, 5, keys_data, format_title)
        j = 1

        for ip in host_info:
            # print(ip)
            keys_ip = sorted(host_info[ip])  # 取出每个ip的键值，并把键值进行排序
            host_value = host_info[ip]  # 取出没有排序的键值
            print(host_value)
            #Title[12]=硬盘剩余率(单位%)
            # print(len(host_value), keys_disk, keys_swap, keys_mem, keys_cpu, keys_data)
            if len(host_value) != 0:  # 如果出现｛'10.1.12.1':{}｝这种情况的时候，需要跳过，不将其写入表格中
                # print(host_value[keys_mem], host_value[keys_swap], host_value[keys_disk], host_value[keys_data])
                worksheet2.write(j, 0, ip, format_value)
                try:
                    worksheet2.write(j, 1, host_value[keys_cpu], format_value)
                except KeyError:
                    host_value[keys_cpu] = ""
                    worksheet2.write(j, 1, host_value[keys_cpu], format_value)
                worksheet2.write(j, 2, host_value[keys_mem], format_value)
                worksheet2.write(j, 3, host_value[keys_swap], format_value)
                worksheet2.write(j, 4, host_value[keys_disk], format_value)
                try:
                    worksheet2.write(j, 5, host_value[keys_data], format_value)
                except KeyError:
                    host_value[keys_data] = ""
                    worksheet2.write(j, 1, host_value[keys_data], format_value)
                    
    #keys_mem in host_value: # or keys_swap in host_value
            else:
                continue
            j += 1
###############制作内存大于90%的服务器表格########################
        worksheet3 = workbook.add_worksheet("内存大于90%")
        # 设置列宽
        worksheet3.set_column('A:B', 25)
        # 设置行高
        worksheet3.set_default_row(25)
        # 冻结首行首列
        worksheet3.freeze_panes(1, 1)
        # 写入第一列、第一行
        worksheet3.write(0, 0, "主机", format_title)
        worksheet3.write(0, 1, keys_mem, format_title)
        j = 1
        for ip in host_info:
            keys_ip = sorted(host_info[ip])  # 取出每个ip的键值，并把键值进行排序
            host_value = host_info[ip]  # 取出没有排序的键值
            if len(host_value) != 0 and keys_mem in host_value and float(host_value[keys_mem]) > 90.0:  # 如果出现｛'10.1.12.1':{}｝这种情况的时候，需要跳过，不将其写入表格中
                #print type(float(host_value[keys_mem]))
                #if float(host_value[keys_mem]) < 20.0:
                worksheet3.write(j, 0, ip, format_value)
                worksheet3.write(j, 1, host_value[keys_mem], format_value)
            else:
                continue
            j += 1
#######################制作硬盘空间小于20%的服务器表格#########################
        # 制作硬盘空间小于20%的服务器表格
        worksheet4 = workbook.add_worksheet("磁盘空间低于20%")
        # 设置列宽
        worksheet4.set_column('A:B', 25)
        # 设置行高
        worksheet4.set_default_row(25)
        # 冻结首行首列
        worksheet4.freeze_panes(1, 1)
        # 写入第一列、第一行
        worksheet4.write(0, 0, "主机", format_title)
        worksheet4.write(0, 1, keys_disk, format_title)
        j = 1
        for ip in host_info:
            keys_ip = sorted(host_info[ip])  # 取出每个ip的键值，并把键值进行排序
            host_value = host_info[ip]  # 取出没有排序的键值)
            if len(host_value) != 0 and keys_disk in host_value and float(
                    host_value[keys_disk]) < 20.0:  # 如果出现｛'10.1.12.1':{}｝这种情况的时候，需要跳过，不将其写入表格中
                # print type(float(host_value[keys_disk]))
                # if float(host_value[keys_disk]) < 20.0:
                worksheet4.write(j, 0, ip, format_value)
                worksheet4.write(j, 1, host_value[keys_disk], format_value)
            else:
                continue
            j += 1
             
#######################制作CPU负载大于8的服务器表格#########################
            # 制作CPU负载大于8的服务器表格
            worksheet5 = workbook.add_worksheet("CPU负载大于8")
            # 设置列宽
            worksheet5.set_column('A:B', 25)
            # 设置行高
            worksheet5.set_default_row(25)
            # 冻结首行首列
            worksheet5.freeze_panes(1, 1)
            # 写入第一列、第一行
            worksheet5.write(0, 0, "主机", format_title)
            worksheet5.write(0, 1, keys_cpu, format_title)
            j = 1
            for ip in host_info:
                keys_ip = sorted(host_info[ip])  # 取出每个ip的键值，并把键值进行排序
                host_value = host_info[ip]  # 取出没有排序的键值
                if len(host_value) != 0 and keys_cpu in host_value and float(
                        host_value[keys_cpu]) > 8:  # 如果出现｛'10.1.12.1':{}｝这种情况的时候，需要跳过，不将其写入表格中
                    # print type(float(host_value[keys_cpu]))
                    # if float(host_value[keys_cpu]) < 20.0:
                    worksheet5.write(j, 0, ip, format_value)
                    worksheet5.write(j, 1, host_value[keys_cpu], format_value)
                else:
                    continue
                j += 1
        workbook.close()

    def xls_transform_csv(self):
        
        xl = pd.ExcelFile(xls_fname)
        for item in xl.sheet_names:
            # print(item)
            df = pd.read_excel(xls_fname, item)
            df.to_csv(item+'.csv', index=False,  encoding='utf-8')
 
    def draw_charts(self):
        
        csv = pd.read_csv("总览表格.csv")
        
        rows = []
        data = []
        host_name = list(csv['主机名'])
        host_attribute = (list(csv.columns))[1:]
        print(host_attribute)

        for i in range(len(host_name)):
            data.append((list(csv.loc[i,:]))[2])
        # print(data)
        # matplotlib.pyplot.figure（num = None，figsize = None，dpi = None，
        # facecolor = None，edgecolor = None，frameon = True，
        # FigureClass = <class'matplotlib.figure.Figure'>，clear = False，** kwargs ）

        plt.rcParams['savefig.dpi'] = 200 #图片像素
        plt.rcParams['figure.dpi'] = 300 #分辨率
        # 设置画布大小
        plt.rcParams['figure.figsize'] = (10.0, 8.0)

        plt.bar(host_name, data, width=0.35, align='center', \
                color='c', alpha=0.8)
         
        # 旋转x轴单元的角度
        plt.xticks(rotation=30)

        for a,b in zip(host_name, data):
            plt.text(a,b+0.1,'%.0f'%b,ha = 'center',va = 'bottom',fontsize=7)
        plt.savefig('label_distribution.png')

    def sendreport(self):
        # 发件服务器地址
        mail_host = 'smtp.163.com'
        # 发件邮箱地址
        sender_user = 'xxxx_monitor@163.com'
        # mail_pass = 'xxxx'#登录密码
        # 邮箱授权码，不是登录密码
        sender_pass = 'xxxxx'
        # 收件邮箱地址
        receivers = ['wangpengtai@xxx.com', 'wangpeng@xxx.cn']
        # 创建带附件实例
        message = MIMEMultipart()
        # 邮件内容
        # message = MIMEText('Python 邮件测试发送','plain','utf-8')
        # 发送邮箱地址
        message['From'] = sender_user
        # 群发邮件时会报错message['To']不支持列表，使用join函数把地址合成字符串
        message['To'] = ",".join(receivers)
        # 邮件主题
        subject = '一周服务器资源使用情况报表'
        message['Subject'] = subject.decode('utf-8')
        # 邮件正文内容
        message.attach(MIMEText('一周服务器资源使用情况报表', 'plain', 'utf-8'))
        # 构造附件1，传送当前目录下
        excel = MIMEApplication(open(fname, 'rb').read(), 'utf-8')
        excel.add_header('Content-Disposition', 'attachment', filename=fname)
        message.attach(excel)
        try:
            smtpobj = smtplib.SMTP()
            # smtpobj.set_debuglevel(1)
            smtpobj.connect(mail_host, 25)
            smtpobj.login(sender_user, sender_pass)
            smtpobj.sendmail(sender_user, receivers, message.as_string())
            smtpobj.close()
            print('邮件发送成功')
        except:
            print("邮件发送失败")

if __name__ == "__main__":
    zabbix = Report()
    zabbix.dispalyvalue()
    zabbix.createreport()
    zabbix.xls_transform_csv()
    zabbix.draw_charts()
#    zabbix.createreport_csv()
#    zabbix.sendreport()

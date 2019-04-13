#!/bin/env python3.6


import sys
#imp.reload(sys)
#import getopt
import smtplib

from email.mime.text import MIMEText
#from email.mime.multipart import MIMEMultipart

#from subprocess import *

def sendqqmail(username,password,mailfrom,mailto,subject,content):
    gserver = 'smtp.qq.com'
    gport = 25
    try:
        '''-------编辑邮件的内容------'''
        # 邮件内容
        msg = MIMEText(str(content))
        # 发送者账号
        msg['from'] = mailfrom
        # 接收者账号
        msg['to'] = mailto
        # “Replay-to:”：对方回信所用的地址，该地址可以与发送人发信时的地址不同。
        msg['Reply-To'] = mailfrom
        # 邮件主题
        msg['Subject'] = subject

        # 连接邮箱，传入邮箱地址，和端口号，smtp的端口号是25
        smtp = smtplib.SMTP(gserver, gport)
        # 我们用set_debuglevel(1)就可以打印出和SMTP服务器交互的所有信息，0为不打印。
        smtp.set_debuglevel(0)
        # 使用ehlo指令像ESMTP（SMTP扩展）确认你的身份
        smtp.ehlo()
        # 登录发送者的邮箱账号，密码
        smtp.login(username, password)
        # 参数分别是发送者，接收者，第三个是把上面的发送邮件的内容变成字符串
        smtp.sendmail(mailfrom, mailto, msg.as_string())
        smtp.close()
    except Exception as err:
        print("Send mail failed.Error:%s" %err)

def main():
    to = sys.argv[1]
    subject = sys.argv[2]
    content = sys.argv[3]
    sendqqmail('529898989@qq.com','dooryddcinqwcaef','529898989@qq.com',to,subject,content)
    #sendqqmail('529898989@qq.com','dooryddcinqwcaef','529898989@qq.com',"529898989@qq.com",'1','1')

if __name__=="__main__":
    main()


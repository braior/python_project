
#!/bin/env python3
#-*- code:utf-8 -*-


import psutil

disk = psutil.disk_partitions()
for i in disk:
    print('磁盘：%s 分区格式: %s' %(i.device, i.fstype))
    disk_use = psutil.disk_usage(i.mountpoint)
    data_list = [disk_use.used/1024/1024/1024, disk_use.free/1024/1024/1024, \
        disk_use.total/1024/1024/1024, disk_use.percent]
    #print(data_list)
    #for i in range(0,len(data_list)-1):
    #    template = "使用了：{:.2f}M;空闲：{:.2f}M,总共：{:.2f}M,使用率:\033[1;31;42m{:.2f}%%\033[0m"
    #    print(template.format(*data_list))
    #print("使用了：%sM;空闲：%sM,总共：%sM,使用率:\033[1;31;42m%s%%\033[0m".format(data_list[1:len(data_list)-1]))
    print("使用了：{:.2f}G;\n空闲：{:.2f}G;\n总共：{:.2f}G;\n使用率:\033[1;31;42m{:.2f}%\033[0m\n".format(*data_list))
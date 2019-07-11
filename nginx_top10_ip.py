
#!/env/bin/env python3
# -*- coding: utf-8 -*-

# Author :braior
# File   :redisdel.py
# Time   :2018-12-20 15:30



import matplotlib.pyplot as plt
nginx_file = 'nginx'

ip = {}
# 筛选nginx日志文件中的ip
with open(nginx_file) as f:
    for i in f.readlines():

        # Python strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列。
        # 注意：该方法只能删除开头或是结尾的字符，不能删除中间部分的字符。
        s = i.strip().split()[0]
        # print(s)
        # print(type(s))
        # lengh = len(ip.keys())

        # 统计每个ip的访问量以字典存储
        if s in ip.keys():
            ip[s] = ip[s] + 1
            print(ip)
        else:
            ip[s] = 1
            # print(ip)

#以ip出现的次数排序返回对象为list
ip = sorted(ip.items(), key=lambda e:e[1], reverse=True)

#取列表前十
newip = ip[0:10:1]
tu = dict(newip)

x = []
y = []
for k in tu:
    x.append(k)
    y.append(tu[k])
plt.title('ip access')
plt.xlabel('ip address')
plt.ylabel('PV')

#x轴项的翻转角度
plt.xticks(rotation=0)

#显示每个柱状图的值
for a,b in zip(x,y):
    plt.text(a, b, '%.0f' % b, ha='center', va= 'bottom',fontsize=7)

plt.bar(x,y)
plt.legend()
plt.show()

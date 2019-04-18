
#!/env/bin python3.6
#-*- coding: utf-8 -*-

'''
采集系统信息包括了CPU，内存，磁盘，网络等。结合自身情况
psutil模块是一个跨平台的获取进程和系统应用情况（CPU，内存，磁盘，网络，传感器）的库。
该模块用于系统监控、限制进程资源和运行进程的管理等方面。
'''
'''
(1) CPU信息
psutil.cpu_count() # CPU逻辑数量
psutil.cpu_count(logical=False) # CPU物理核心
psutil.cpu_percent() # CPU当前使用率

(2) 内存信息
mem = psutil.virtual_memory() # 实例化内存对象
mem.total  # 系统总计内存
mem.used  # 系统已经使用内存
mem.free # 系统空闲内存
psutil.swap_memory() # swap内存信息

(3) 硬盘信息
psutil.disk_usage('/')

(4) 网络信息
psutil.net_io_counters(pernic=True)
'''
# python 监测服务器的cpu和内存占用率，单进程的内存和cpu占用率
# 先安装两个包psutil和pymysql
# 在mysql创建数据库test1，然后创建table
# sql = "create table memory_and_cpu(cpu_lv varchar(100),memory_lv varchar(100),pro_cpu_lv varchar(100), pro_memory_lv varchar(100));"


import psutil
import time
import pymysql

cpu_list = []
memory_list = []
pro_cpu_list = []
pro_memory_list = []
data = []


def useagent(pid_list):
    for i in range(5):
        try:
            time.sleep(3)
            cpu_lv = psutil.cpu_percent()
            cpu_list.append(cpu_lv)
            print('当前服务器cpu利用率：\033[1;31;42m%.2f%%\033[0m' %cpu_lv)

            memory = psutil.virtual_memory()
            memory_lv = memory.used/memory.total*100
            memory_list.append(memory_lv)
            print("当前服务器内存利用率%.2f%%" % memory_lv)

            #pro = psutil.pids()
            pro_cpu_lv = get_cpu_percent(pid_list)
            print("当前进程cpu利用率%.2f%%" % pro_cpu_lv[0])
            #pro_cpu_lv_ = float(pro_cpu_lv[-1])
            pro_cpu_list.append(float(pro_cpu_lv[-1]))

            p = psutil.Process(pid_list[0])
            pro_memory_lv = p.memory_percent()
            pro_memory_list.append(pro_memory_lv)
            print("当前进程内存利用率%.2f%%" % pro_memory_lv)
            #print(p)
            #print("\n")
            
            #data.append([cpu_lv[-1], memory_lv[-1], pro_cpu_lv[-1], pro_memory_lv[-1])
            data = (cpu_list[-1], memory_list[-1], pro_cpu_list[-1], pro_memory_list[-1])
            #print(data)
            DB_operatiom(data)

        except:
            print("连接服务器异常")
            print(cpu_list)
            print(memory_list)
            print(pro_cpu_list)
            print(pro_memory_list)

def get_cpu_percent(pid_list, interval=0.5):
    process = [psutil.Process(pid=i) for i in pid_list]
    #print(type(process))
    #[psutil.Process(pid=3700, name='vmnat.exe', started='2019-03-02 08:36:56')]
    #print(process)
    for p in process:
        p.cpu_percent(interval=None)
        time.sleep(interval)
        percents = [p.cpu_percent(interval=None) for p in process]
        #print(type(percents))
        #print(percents)
        return percents

def DB_operatiom(data_list):

    connect = pymysql.Connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='123456',
    db='test12',
    charset='utf8'
)

    # 创建数据路数据承载对象--获取游标对象cursor
    cursor = connect.cursor()

    # 创建一个数据库--test12
    #cursor.execute('create database if not exists test12')

    # 选择数据库
    #connect.select_db('test12')

    # 删除数据库
    #cursor.execute('drop database if exists test12')

    # 数据库插入操作
    def mysql_insert(data_list):

        # 创建数据库中的表
        #cursor.execute('create table if not exists cpu_and_memory(cpu_lv vachar(100), \
        #    memory_lv varchar(100), pro_cpu_lv varchar(100), pro_memory_lv varchar(100)')

        # 删除数据库中的表
        # cursor.execute('drop talbe if exists cpu_and_memory')

        

        sql_insert= "insert into cpu_and_memory(cpu_lv, memory_lv, pro_cpu_lv, pro_memory_lv) values('%s','%s','%s','%s')"
        #sql = '''create talbe if ont exists cpu_and_memory(cpu_lv vachar(100), \
        #        memory_lv varchar(100), pro_cpu_lv varchar(100), pro_memory_lv varchar(100))engine=InnoDB,charset=utf8;'''
        
        try:
            #插入数据
            cursor.execute(sql_insert % data_list)
            #提交数据
            connect.commit()
            print('成功插入', cursor.rowcount, '条数据')
        except Exception as e:
            #错误回滚
            connect.rollback()
            print('插入数据失败！')

        finally:
            cursor.close()
            connect.close()

    # 数据库查询操作
    def mysql_select():

        sql_select = "select * from cpu_and_memory"

        try:
            cursor.execute(sql_select)
            for row in cursor.fetchall():
                print("cpu_lv:%s, memory_lv:%s, pro_cpu_lv:%s, pro_memory_lv:%s" % row)
            print("共查找出",cursor.rowcount, "条数据")

        except Exception as e:
            raise e

        finally:
            cursor.close()
            connect.close()

    def mysql_update():

        sql_update = "update cpu_and_memory set cpu_lv = %s where cpu_lv = %s"
        data = (99, 11)

        try:
            cursor.execute(sql_update % data)
            connect.commit()
            print('成功修改', cursor.rowcount, '条数据')

        except Exception as e:
            connect.rollback()
            print('更新数据失败！')

        finally:
            cursor.close()
            connect.close()

    def mysql_delete():
        sql_delete = "delete from cpu_and_memory where cpu_lv = '99' "

        try:
            cursor.execute(sql_delete)
            connect.commit()
            print('成功删除', cursor.rowcount, '条数据')
        
        except Exception as e:
            connect.rollback()
            print('删除数据失败！')
        
        finally:
            cursor.close()
            connect.close()

    mysql_insert(data_list)


if __name__ == '__main__':
    useagent([3040])








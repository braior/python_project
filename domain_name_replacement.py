
# Auth: braior
# Email: braior@163.com
# Date: 2019.08.02


# 注意事项：
# ssl认证证书的存放目录及其文件名必须与站点域名相同

import os
import shutil

old_domain_name = 'ukex.com'
new_domain_name = 'abc.com'
old_conf_suffix = 'ukex.com.conf'
new_conf_suffix = 'abc.com.conf'

new_path = "./abc.com/"
old_path = './vhost/'
ssl_cert_path = '/ssl/'

# old_domain_name = 'abc.com'
# new_domain_name = 'ukex.com'
# old_conf_suffix = 'abc.com.conf'
# new_conf_suffix = 'ukex.com.conf'

file_list = []

print(os.path.exists(new_path))
if os.path.exists(new_path):
    # 删除该文件夹及文件夹内所有文件
    shutil.rmtree(new_path, ignore_errors=True)

# 对要源目录进行copy 
shutil.copytree(old_path, new_path)


def list_dir():
    
    # os.listdir()函数得到的是仅当前路径下的文件名
    # 不包括子目录中的文件，所以需要使用递归的方法得到全部文件名
    for file_name in os.listdir(new_path):
        if old_conf_suffix == file_name.split('.', 1)[1]:
            new_file_name = new_path + file_name.split('.', 1)[0] + '.' + new_conf_suffix
            # print(new_file_name)
            file_list.append(new_file_name)
            # 将包含ukex.com.conf结尾的文件放入file_list
            os.rename(new_path + file_name, new_file_name)
    return file_list

# list_dir()

def replace_content():

    file_paths = list_dir()

    for file_path in file_paths:
        # 读取文件内容到内存
        with open(file_path, "r", encoding="utf-8") as document:
            lines = document.readlines()
            with open(file_path, "w", encoding="utf-8") as document_content:
                for line in lines:
                    if "server_name" in line:
                        # 替换字符
                        line = line.replace(old_domain_name, new_domain_name)

                    if "ssl_certificate " in line:
                        new_ssl_cert = '        ssl_certificate ' + ssl_cert_path + \
                                        file_path.split('/', -1)[-1].split('.conf')[0] + '.crt;\n'
                        # print(new_ssl_cert)
                        line = new_ssl_cert
                    
                    if "ssl_certificate_key " in line:
                        new_ssl_cert_key = '        ssl_certificate_key ' + ssl_cert_path + \
                                            file_path.split('/', -1)[-1].split('.conf')[0] + '.key;\n'
                        # print(new_ssl_cert_key)
                        line = new_ssl_cert_key
                    document_content.writelines(line)


replace_content()
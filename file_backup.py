#!/bin/env python
# @Time     :2019-10-12
# @Author   :braior@163.com
# @File      :file_backup.py

import time
import os
import tarfile
import shutil

# Python中的Pickle模块实现了基本的数据序列与反序列化。
import pickle
import hashlib

'''实现每周一全量备份，其余时间增量备份'''
def md5check(fname):
    md5 = hashlib.md5()
    # print(md5)
    with open(fname) as fobj:
        while True:
            data = fobj.read(4096)
            if not data:
                break
            md5.update(data.encode())
    # print(md5.hexdigest())
    return md5.hexdigest()

# if __name__  == "__main__":
#     md5check("./achievement.py")

def full_backup(src_dir, dst_dir, md5file):
    # Python rstrip() 删除 string 字符串末尾的指定字符（默认为空格）.
    #base_dir = os.path.split(src_dir.rstrip('/'))[1]
    # print(base_dir)
    # back_name = '%s_full_%s.tar.gz' % (base_dir, time.strftime('%Y%m%d'))
    # print(back_name)
    # full_name = os.path.join(dst_dir, back_name)
    # print(full_name)
    md5dict = {}

    # tar = tarfile.open(full_name, 'w:gz')
    # tar.add(src_dir)
    # tar.close()

    if os.path.exists(dst_dir):
        # shutil.rmtree() 表示递归删除文件夹下的所有子文件夹和子文件。
        shutil.rmtree(dst_dir)
    shutil.copytree(src_dir, dst_dir)
    #shutil.make_archive(dst_dir,'zip',src_dir)#将文件压缩，注：如果压缩tar，中文文件名有可能乱码


    for path, folders, files in os.walk(src_dir):
        #print(path, folders, files)
        for fname in files:
            full_path = os.path.join(path, fname)
            print(full_path)
            md5dict[full_path] = md5check(full_path)
            print(md5dict)

    if os.path.exists(md5file):
        # 以二进制格式打开一个文件只用于写入
        with open(md5file, 'wb') as f0:
            pickle.dump(md5dict, f0)
    else:
        # 'xb'独占创建打开 (若文件已存在的话，操作会失败)
        with open(md5file, 'xb') as f1:
            pickle.dump(md5dict, f1)

def incr_backup(src_dir, dst_dir, md5file):
    # par_dir, base_dir = os.path.split(src_dir.rstrip('/'))
    # back_name = '%s_incr_%s.tar.gz' % (base_dir, time.strftime('%Y%m%d'))
    # full_name = os.path.join(dst_dir, back_name)
    md5new = {}

    for path, folders, files in os.walk(src_dir):
        for fname in files:
            full_path = os.path.join(path, fname)
            md5new[full_path] = md5check(full_path)

    with open(md5file, 'rb') as fobj:
        md5old = pickle.load(fobj)


    with open(md5file, 'wb') as fobj:
        pickle.dump(md5new, fobj)

    #tar = tarfile.open(full_name, 'w:gz')
    for key in md5new:
        if md5old[key] != md5new[key]:
            #tar.add(key)
            shutil.copyfile(key, dst_dir)
#     #tar.close()

if __name__ == '__main__':
    src_dir = "E://Python_project//成绩//test"
    dst_dir = "E://Python_project//成绩//test_backup"
    md5file = "E://Python_project//成绩//md5.data"
    full_backup(src_dir, dst_dir, md5file)
    # if time.strftime('%a') == 'Mon':
    #     full_backup(src_dir, dst_dir, md5file)
    # else:
    #     incr_backup(src_dir, dst_dir, md5file)
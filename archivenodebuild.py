#! /usr/bin/env python
# coding: utf-8
import re
import os
import datetime
import sys
import tarfile
import hashlib

# variables
projectName = os.getenv('JOB_NAME')
projectWorkspace = os.getenv('WORKSPACE')
#projectName = 'www.smeiec.com'
#projectWorkspace = '/opt/jenkins/workspace/www.smeiec.com'
runEnv = 'fat'
currentTime = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
distBase = '/dist'
# other
nodeFile = '%s.tar.gz'%(projectName)
sourceDir = os.path.join(projectWorkspace, 'build')
sourceFile = os.path.join(projectWorkspace, 'build', nodeFile)
distDir = os.path.join(distBase, runEnv, 'node', projectName)

# upload the target file.
if os.path.exists(sourceDir):
    # compress the dist directory.
    os.chdir(sourceDir)
    distTargGzFile = tarfile.open(nodeFile,'w:gz')
    #distTargGzFile.add('dist')
    #pwd = os.getcwd()
    for root,dir,files in os.walk('.', topdown=False):
        for file in files:
            pathfile = os.path.join(root, file)
	    distTargGzFile.add(pathfile)
    distTargGzFile.close()
    # md5
    m = hashlib.md5()
    m.update(open(sourceFile, 'rb').read())
    # create path
    if not os.path.exists(distDir):
    	os.makedirs(distDir, 0755)
    elif os.path.exists(os.path.join(distDir, 'md5')):
	md5Value = open(os.path.join(distDir, 'md5')).read()
        print('DEBUG: md5Value is %s vs newMd5 is %s.'%(md5Value, m.hexdigest()))
	if md5Value == m.hexdigest():
	    print('INFO: Code is not changed.')
	    exit(0)
	else:
            if os.path.exists(os.path.join(distDir, nodeFile)):
	       os.rename(os.path.join(distDir, nodeFile), os.path.join(distDir, '%s-bak-%s'%(nodeFile, currentTime)))
               # os.remove(os.path.join(distDir, nodeFile))
            os.remove(os.path.join(distDir, 'md5'))
    open(os.path.join(distDir, nodeFile), 'wb').write(open(sourceFile, 'rb').read())
    open(os.path.join(distDir, 'md5'), 'wb').write(m.hexdigest())
    os.remove(sourceFile)
    print('INFO: Code has been uploaded.')
else:
    print('ERROR: Target file is not exists, %s.'%(sourceFile))
    exit(1)

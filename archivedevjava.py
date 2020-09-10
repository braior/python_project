#! /usr/bin/env python
# coding: utf-8
import os
import datetime
import hashlib
import sys
import tarfile

# variables
#projectName = os.getenv('JOB_NAME')
#projectWorkspace = os.getenv('WORKSPACE')
projectName = sys.argv[1]
projectWorkspace = sys.argv[2]
runEnv = 'dev'
distBase = '/dist'
jarName = sys.argv[3]


# backup the target file.
jarFile= os.path.join(projectWorkspace, 'target', jarName)
sourceFile = os.path.join(projectWorkspace, 'target', '%s.tar.gz'%(jarFile))
distDir = os.path.join(distBase, runEnv, 'java', projectName)
print('sourceFile:%s'%sourceFile)
if os.path.exists(jarFile):
    # compress jar file.
    os.chdir(os.path.join(projectWorkspace, 'target'))
    tf = tarfile.open('%s.tar.gz'%(jarName), 'w:gz')
    tf.add(jarName)
    tf.close()
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
            if os.path.exists(os.path.join(distDir, '%s.tar.gz'%(jarName))):
		os.remove(os.path.join(distDir, '%s.tar.gz'%(jarName)))
            os.remove(os.path.join(distDir, 'md5'))
    open(os.path.join(distDir, '%s.tar.gz'%(jarName)), 'wb').write(open(sourceFile, 'rb').read())
    open(os.path.join(distDir, 'md5'), 'wb').write(m.hexdigest())
    print('INFO: Code has been uploaded.')
else:
    print('ERROR: Target file is not exists, %s.'%(sourceFile))
    exit(1)

#! /usr/bin/env python
# coding: utf-8
import xml.etree.cElementTree as ET
import re
import hashlib
import sys
import os

# variable
#projectWorkspace = "/opt/jenkins/workspace/fat-humi-job-admin/"
projectWorkspace = os.getenv('WORKSPACE')

# namespace
def get_namespace(element):
    m = re.match('\{.*\}', element.tag)
    return m.group(0) if m else ''
# purseXml
tree = ET.ElementTree()
root = tree.parse('%s/pom.xml'%(projectWorkspace))
namespace = get_namespace(tree.getroot())
# 获取parent下的version
pomXmlVersion = tree.find('%sversion' % (namespace))
if pomXmlVersion is None:
    pomXmlVersion = root.find("./%sparent/%sversion" % (namespace, namespace))
pomVersion = pomXmlVersion.text
pomSartifact = tree.find('%sartifactId'%(namespace)).text
jarFile = '%s-%s.jar'%( pomSartifact, pomVersion)
print(jarFile)

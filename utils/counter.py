# !/usr/bin/python
# -*- coding: utf-8 -*-

import os
import re


os.chdir('SMS-Front-End')
ficherosFrontEnd = []
linesFrontEnd = 0
for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        fullname = os.path.join(root, name)
        if not re.match('./app/css|./app/js|./app/out|./app/images|./app/fonts', root) and not re.match('LICENSE|logo.svg', name):
            ficherosFrontEnd.append(fullname)
            f=open(fullname)
            linesFrontEnd = linesFrontEnd + len(f.readlines())

os.chdir('../SMS-Back-End')
os.chdir('apigateway')
ficherosapig = []
linesapig = 0
for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        fullname = os.path.join(root, name)
        if not re.match('./lib', root) and not name.endswith(('pyc','jpg')):
            ficherosapig.append(fullname)
            #print fullname
            f=open(fullname)
            linesapig = linesapig + len(f.readlines())


os.chdir('..')
os.chdir('microservicio1')
ficherossbd = []
linessbd = 0
for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        fullname = os.path.join(root, name)
        if not re.match('./docs|./lib', root) and not name.endswith('pyc'):
            ficherossbd.append(fullname)
            print fullname
            f=open(fullname)
            linessbd = linessbd + len(f.readlines())

os.chdir('..')
os.chdir('sce')
ficherossce = []
linessce = 0
for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        fullname = os.path.join(root, name)
        if not re.match('./lib', root) and not name.endswith(('pyc','png')):
            ficherossce.append(fullname)
            print fullname
            f=open(fullname)
            linessce = linessce + len(f.readlines())

'''
print 'Tams'
print linesFrontEnd
print linesapig
print linessbd
print linessce
'''


#Extraemos el número del commit

import subprocess
cmd = "git rev-list --count HEAD"
x = subprocess.Popen(cmd, shell=True, stdout = subprocess.PIPE, stderr=subprocess.PIPE)
out, error = x.communicate()
numCommit=out[:-1]

#print 'numcommit' +str(numCommit)

os.system("git checkout gh-pages")

import datetime
date = datetime.date.today()
line=str(numCommit)+';'+str(date)+';'+str(linesFrontEnd)+';'+str(linesapig)+';'+str(linessbd)+';'+str(linessce)
'''cmd="echo \""+line+"\" >> lines.txt"
print cmd
x = subprocess.Popen(cmd, shell=True, stdout = subprocess.PIPE, stderr=subprocess.PIPE)
out, error = x.communicate()
print out
print error
'''
os.chdir('../..')
f = open('lines.txt', 'a')
f.write(line+'\n')
f.close()

os.system("git commit -am \" Commit de actualizacion"+numCommit+" . \"")

cmd = "git checkout master"
os.system(cmd)

#coding=utf8
__version__= 1.0
__author__="lucky_kris"
import os
import sys
def Start():
	pid=os.fork()
	if pid != 0:
		sys.exit(0)
	os.setsid()
	os.umask(0)
	pid=os.fork()
	if pid != 0:
		sys.exit(0)
	pid=os.getpid()
	os.umask(18)
	null=open("/dev/null",'rw')
	os.dup2(null.fileno(),0)
	os.dup2(null.fileno(),1)
	os.dup2(null.fileno(),2)
	return pid
	


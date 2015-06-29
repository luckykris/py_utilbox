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
	return pid
	


#author:luckykris
#version 1.0
#last modified : 2015-01-07
import multiprocessing
import Queue
import time
import socket
from py_utilbox import TcpServer
class New(TcpServer.TcpServer):
	def __init__(self,workerfunc,mode="finish",process=1,overseer={"status":False}):
		self.MANAGER = multiprocessing.Manager()
		self.RESULTQUE = self.MANAGER.Queue()
		self.JOBQUE = self.MANAGER.Queue()
		self.KILL= self.MANAGER.Value('k',0) 
		self.WORKER = workerfunc
		self.PROCESS = process
		self.WORKERMODE = mode
		self.WORKERS=[]
		self.OVERSEER = overseer
		TcpServer.TcpServer.__init__(self,port=self.OVERSEER['port'])
        def HandleFunc(self,conn,ip):
                print("MyTcpServer:you got a handler"+str(ip))
		conn.send(">>Welcome To Process Overseer:\n1.stop all process\n2.show proccesslist\n3.exit\n>>")
		while True:
			try:
				r=int(conn.recv(1024))	
			except:
				try:
					conn.send(">>Wrong Command!\n")
					continue
				except:
					continue
			if r == 1 :
				self.KILL.set(1)
				conn.send(">>Command Accept!\n")
				return -1
			elif r == 3:
				conn.send(">>bye!\n")
				break
		return
	def __Overseer(self):
		self.StartServer()
		#self.KILL.set(1)
	def __Worker(self,jq,rq,):
		if self.WORKERMODE == "persist":
			while not self.KILL.get():
				print self.KILL.get()
				rq.put(self.WORKER(jq.get(block=True)))
		elif self.WORKERMODE == "finish":
			while not jq.empty() or not self.KILL.get():
				try:
					rq.put(self.WORKER(jq.get(block=False)))
				except:
					continue
		return 0
	def Start(self):
		if self.OVERSEER['status'] == True:
			wd = multiprocessing.Process(target=self.__Overseer)
			wd.start()
		for proc in xrange(0,self.PROCESS):
			prc = multiprocessing.Process(target=self.__Worker,args=(self.JOBQUE,self.RESULTQUE))                           
			prc.start()
			self.WORKERS.append(prc)		
		try:                    
			for worker in self.WORKERS:
				worker.join()
		except KeyboardInterrupt:
			for worker in self.WORKERS:
				worker.terminate()
				worker.join()
	def Get(self):
		return self.RESULTQUE.get()
	def Put(self,args):
		return self.JOBQUE.put(args)
	def JobQueLen(self):
		return self.JOBQUE.qsize() 

#author:luckykris
#version 1.0
#last modified : 2015-01-07
import multiprocessing
import Queue
import time
import socket
from py_utilbox import TcpServer
import sys
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
		self.status=[]
	#	self.WORLERS=self.MANAGER.list()
		self.OVERSEER = overseer
		TcpServer.TcpServer.__init__(self,port=self.OVERSEER['port'])
	def HandleFunc(self,conn,ip):
                print("MyTcpServer:you got a handler"+str(ip))
                conn.send(">>Welcome To Process Overseer:\n1.stop all process safely\n2.show proccesslist\n3.exit\n>>")
                while True:
                        try:
                                r=int(conn.recv(1024))
                        except:
                                try:
                                        conn.send(">>Wrong Command!\n>>")
                                        continue
                                except:
                                        continue
                        if r == 1 :
                                self.KILL.set(1)
                                conn.send(">>Command Accept!\n")
                                return -1
                        elif r == 2:
                                info="Total:"+str(len(self.WORKERS))+"\nNAME\t\tPID\t\tALIVE\n"
                                print(self.WORKERS)
                                for i in self.status:
                                        print(i[0])
                                        info=info+i[0]+"\t\t"+str(i[1])+"\t\t"+str(i[2])+"\n"
                                info+=">>"
                                conn.send(info)
                        elif r == 3:
                                conn.send(">>bye!\n")
                                break
                        else:
                                conn.send(">>Undefined command!!\n>>")
                return
	def __Overseer(self):
		self.StartServer()
		self.Close()
		#self.KILL.set(1)
	def __Worker(self,jq,rq,):
		if self.WORKERMODE == "persist":
			while not self.KILL.get():
				rq.put(self.WORKER(jq.get(block=True)))
		elif self.WORKERMODE == "finish":
			while  not self.KILL.get() and not jq.empty():
				try:
					rq.put(self.WORKER(jq.get(block=False)))
				except:
					continue
		sys.exit()
		return 
	def Start(self):
		for proc in xrange(0,self.PROCESS):
			prc = multiprocessing.Process(target=self.__Worker,args=(self.JOBQUE,self.RESULTQUE))                           
			prc.start()
			self.WORKERS.append(prc)		
		if self.OVERSEER['status'] == True:
			for  i in self.WORKERS:
				self.status.append((i.name,i.pid,i.is_alive()))
			wd = multiprocessing.Process(target=self.__Overseer)
			wd.start()
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

#author:luckykris
#version 1.0
#last modified : 2015-01-07
import multiprocessing
import Queue
import time

class New(object):
	def __init__(self,workerfunc,mode="finish",process=1):
		self.MANAGER = multiprocessing.Manager()
		self.RESULTQUE = self.MANAGER.Queue()
		self.JOBQUE = self.MANAGER.Queue()
		self.WORKER = workerfunc
		self.PROCESS = process
		self.WORKERMODE = mode
		self.TERMINATE = False

	def __Worker(self,jq,rq,):
		if self.WORKERMODE == "persist":
			while True:
				rq.put(self.WORKER(jq.get(block=True,timeout=1)))
		elif self.WORKERMODE == "finish":
			while not jq.empty():
				try:
					rq.put(self.WORKER(jq.get(block=False)))
				except:
					continue
		return 0
	def Start(self):
		workers=[]
		for proc in xrange(0,self.PROCESS):
			prc = multiprocessing.Process(target=self.__Worker,args=(self.JOBQUE,self.RESULTQUE))                           
			prc.start()
			workers.append(prc)		
		try:                    
			for worker in workers:
				worker.join()
		except KeyboardInterrupt:
			for worker in workers:
				worker.terminate()
				worker.join()
	def Get(self):
		return self.RESULTQUE.get()
	def Put(self,args):
		return self.JOBQUE.put(args)
	def JobQueLen(self):
		return self.JOBQUE.qsize() 

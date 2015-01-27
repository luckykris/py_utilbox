#__version__= 0.1
#__author__="lucky_kris"
#__Email__"luckykris@yeah.net"
import signal
class Handler:
	def __init__(self):
		self.isexit=False
	def StartHandler(self):
		signal.signal(signal.SIGINT,self.HandleFunction)
	        signal.signal(signal.SIGHUP, self.HandleFunction)
	        signal.signal(signal.SIGTERM, self.HandleFunction)
	def HandleFunction(self,sig,frame):
		print("SignalHandler: I Got Sig:"+str(sig))
	

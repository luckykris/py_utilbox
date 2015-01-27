import threading
import socket
class TcpServer:
	def __init__(self,port,mode="threading",mask='0.0.0.0',length=100):
		self.port=port
		self.mode=mode
		self.mask=mask
		self.length=length
		self.bool=True
	def HandleFunc(self,conn,ip):
		print("TcpServer:you got a handler")
		conn.send("Please input 'a' :")
		print conn.recv(1024)	
		return 
		
		
	def Handler(self,conn,ip):
		r=self.HandleFunc(conn,ip)
		conn.close()
		del conn
		if r==-1:
			self.SafeExit()
		return
	def SafeExit(self):
		self.bool=False
		c = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		c.connect(('127.0.0.1',self.port))
		c.close()
	def StartServer(self):
		self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.s.bind((self.mask,self.port))
		self.s.listen(self.length)
		while self.bool:
			conn,ip=self.s.accept()
			threading.Thread(target=self.Handler,args=(conn,ip)).start()
	def __del__(self):
		self.s.close()

from py_utilbox import TcpServer
import time
class MyTcpServer(TcpServer.TcpServer):
        def HandleFunc(self,conn,ip):
		print("MyTcpServer:you got a handler"+ str(conn))
		time.sleep(3)
a=MyTcpServer(port=9999)
a.StartServer()

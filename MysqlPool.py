import pymysql
import queue
class New:
	def __init__(self,user,passwd,db,charset="utf8",host='localhost',port=3306,size=10):
		self.size=size
		self.user=user
		self.passwd=passwd
		self.host=host
		self.port=port
		self.charset=charset
		self.db=db
		self.isClose=True
		self.queue=queue.Queue(maxsize = self.size)
	def __connect(self):
		conn = pymysql.connect(user=self.user,passwd=self.passwd,host=self.host,port=self.port,charset=self.charset,db=self.db)
		return conn
	def Start(self):
		if self.isClose:
			self.isClose=False
		else:
			return
		for c in range(0,self.size):
			conn=self.__connect()
			self.queue.put(conn)
	def __runSql(self,conn,sql):
		cur=conn.cursor()
		cur.execute(sql)
		return cur
	def Set(self,sql):
		try:
			conn=self.queue.get()
			cur=self.__runSql(conn,sql)
			conn.commit()
		except pymysql.err.OperationalError:
			conn=self.__connect()
			cur=self.__runSql(conn,sql)
			conn.commit()
		finally:
			if 'cur'   in   locals().keys():
				cur.close()
			self.queue.put(conn)
	def Get(self,sql):
		try:
			conn=self.queue.get()
			cur=self.__runSql(conn,sql)
			result=cur.fetchall()
		except pymysql.err.OperationalError:
			conn=self.__connect()
			cur=self.__runSql(conn,sql)
			result=cur.fetchall()
		finally:
			if 'cur'   in   locals().keys():
				cur.close()
			self.queue.put(conn)
		return result
	def __del__(self):
		if self.isClose:
			return
		for c in  range(0,self.size):
			conn=self.queue.get(False) 
			conn.close()
	def Close(self):
		if self.isClose:
			return
		for c in  range(0,self.size):
			conn=self.queue.get()           
			conn.close()
		self.isClose=True

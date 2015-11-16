import DNS
import time
import random
version="1.0.1"
class New:
	def __init__(self,service,servers=None,interval=300,base="service.consul",tags=[]):
		self.servers=servers
		self.interval=interval
		self.tags=tags
		self.timestamp=time.time()
		self.baseStr=service+"."+base
		self.srvs=[]
		if servers is None:
			reqobj = DNS.Request()
			self.reqDnss=[reqobj]
		else:
			self.reqDnss=[]
			for s in servers:
				reqobj = DNS.Request(server=s)
				self.reqDnss.append(reqobj)
		self.initCache([x for x in range(0,len(self.servers))])
	def initCache(self,ls):
		if ls==[]:
			raise IOError("all the dns are down")
		i=random.randint(0,len(ls)-1)
		ri=ls[i]
		reqobj=self.reqDnss[ri]
		self.srv=[]
		try:
			self.__tagFilter(reqobj)
		except :
			ls.remove(ri)
			self.initCache(ls)
	def __tagFilter(self,reqobj):
		tmp_list=[]
		first=True
		if self.tags==[]:
			answerobj=reqobj.req(name =self.baseStr , qtype = DNS.Type.SRV)
			self.srvs=answerobj.answers
		for tag in self.tags:
			answerobj=reqobj.req(name =".".join([tag,self.baseStr]) , qtype = DNS.Type.SRV)
			if len(answerobj.answers) == 0:
				self.srvs=[]
				return 
			if first:
				tmp_list=answerobj.answers
				first=False
				#print("tag:"+tag+str(tmp_list))
				continue
			tmp_list2=[]
			for i in answerobj.answers:
				for j in tmp_list:
					if j['data']==i['data']:
						tmp_list2.append(i)
						break
			tmp_list=tmp_list2
		for i in range(0,len(tmp_list)):
			ls=list(tmp_list[i]['data'])
			IpDnsObj=reqobj.req(name =ls[3] , qtype = DNS.Type.ANY)
			ls[3]=IpDnsObj.answers[0]['data']
			tmp_list[i]['data']=tuple(ls)
		self.srvs=tmp_list
		return
	def get(self,info="srv"):
		if time.time() - self.timestamp > self.interval:
			self.initCache([x for x in range(0,len(self.servers))] )
		if self.srvs == []:
			raise IOError("didn`t find the service which has tags '%s'" % ",".join(self.tags))
		else:
			min={'k':None,'v':100000}
			for i in self.srvs:
				if i['rdlength']<min['v']:
					min['k']=i
			if info == "port":
				return min['k']['data'][2]
			if info == "ip":
				return min['k']['data'][3]
			if info == "srv":
				return ("%s:%d")% (min['k']['data'][3],min['k']['data'][2])
			raise IOError("Error info ->'%s'" % info)

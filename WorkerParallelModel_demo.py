from  py_utilbox import WorkerParallelModel
import time
def Workerfunc(a):
	time.sleep(6)
	print "hi"


a=WorkerParallelModel.New(workerfunc=Workerfunc,mode="persist",process=2,overseer={"status":True,"port":9999})
#	a.Terminate()
for i in xrange(1,100):
        a.Put(i)
a.Start()


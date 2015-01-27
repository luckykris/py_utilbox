from py_utilbox import SignalExit
import time
class Hd(SignalExit.Handler):
        def HandleFunction(self,sig,frame):
	        print("niehahahaha:"+str(sig))

hd=Hd()
hd.StartHandler()

while True:
	time.sleep(3)

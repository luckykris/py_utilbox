import threading
def go(func,args=()):
	t=threading.Thread(target=func,args=args)
	t.start()
	return
def NumGoroutine():
	return threading.active_count()

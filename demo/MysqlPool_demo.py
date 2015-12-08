from py_utilbox import MysqlPool
import time
a=MysqlPool.New(user='root',passwd='root',db='troy',host='192.168.33.13',port=3306,charset='utf8',size=5)
a.Start()
r=a.Get('select * from t_tag')
print(1)
time.sleep(30)
r=a.Get('select * from t_tag')
print(2)
time.sleep(160)

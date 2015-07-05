#!/usr/bin/env python

import sys, time
import socket
import subprocess
import threading
import MySQLdb

from daemon import Daemon
from datetime import datetime, timedelta

def tell_me_somth(charact):
	pass
#	dict={}
#	now=datetime.now()
#	now_five=datetime.now()-timedelta(minutes=5)
#	now_date_time='%s-%s-%s %s:%s:%s' % (now.year, now.month, now.day, now.hour, now.minute, now.second)
#	now_five_format = '%s-%s-%s %s:%s:%s' % (now_five.year, now_five.month, now_five.day, now_five.hour, now_five.minute, now_five.second)
#	db = MySQLdb.connect(host="localhost", user="sprint", passwd="sprint", db="spirit", charset='utf8')
#	cursor = db.cursor()
#	if charact == "CPU":
#		sql = 'SELECT date_time, user, cpu FROM cpu WHERE date_time > "%s"' % (now_five_format)
#		cursor.execute(sql)
#		data = cursor.fetchall()
#		for rec in data:
#			dict[rec[1]]+=rec[2]
#			b = list(dict.items())
#			b.sort(key=lambda item: item[1])
#		db.close()

def scan_me_all():
    while True:
        now=datetime.now()
        now_date_time='%s-%s-%s %s:%s:%s' % (now.year, now.month, now.day, now.hour, now.minute, now.second)
        p=subprocess.Popen("ps -aux | awk '{sum[$1] += $3}END {for(i in sum)print i \":\"sum[i]}'", shell=True, stdout=subprocess.PIPE)
        a=[]
        db = MySQLdb.connect(host="localhost", user="sprint", passwd="sprint", db="spirit", charset='utf8')
        cursor = db.cursor()
        while True:
            strin_answ=p.stdout.readline()
            if not strin_answ: break
            a.append(strin_answ.split(":"))
        for elem in a:
        	sql = """INSERT INTO cpu(date_time, user, cpu) VALUES ('%(date_time)s', '%(user)s', '%(cpu)s')"""%{"date_time":(str(now_date_time)), "user":str(elem[0]), "cpu":str(elem[1])}
        	cursor.execute(sql)
        db.commit()
        db.close()
        time.sleep(90)


def wait_take_it_easy():
	while True:
		sock = socket.socket()
		sock.bind(('', 9090))
	    	sock.listen(1)
		conn, addr = sock.accept()
		print 'connected:', addr
		while True:
			data = conn.recv(1024)
			if not data:
				break
			try:
				str(data)
			except:
				conn.send("Bad parametr")
				break
			#doing somth.
			if str(data) == "CPU":
				print tell_me_somth("CPU")
			elif str(data) == "HDD":
				pass
			else:
				conn.send("Parametr Does exist")
				conn.close()
		time.sleep(1)

def shut_up_and_write():
	pass

class MyDaemon(Daemon):
	def run(self):
		#t1 = threading.Thread(target=wait_take_it_easy, args=())
		#t2 = threading.Thread(target=scan_me_all, args=())
#		sock = socket.socket()
#		sock.bind(('', 9090))
#		sock.listen(1)
#		conn, addr = sock.accept()
#		print 'connected:', addr
#		while True:
#			while True:
#				data = conn.recv(1024)
#				if not data:
#					break
#				conn.send(data.upper())
#			conn.close()
#			time.sleep(1)
		#t1.start()
		#t2.start()

if __name__ == "__main__":
	daemon = MyDaemon('/tmp/PIDsprint.pid')
	if len(sys.argv) == 2:
		if 'start' == sys.argv[1]:
			daemon.start()
		elif 'stop' == sys.argv[1]:
			daemon.stop()
		elif 'restart' == sys.argv[1]:
			daemon.restart()
		else:
			print "Unknown command"
			sys.exit(2)
		sys.exit(0)
	else:
		print "usage: %s start|stop|restart" % sys.argv[0]
		sys.exit(2)

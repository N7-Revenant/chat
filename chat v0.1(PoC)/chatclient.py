import socket
import threading
import time

tLock = threading.Lock()
shutdown = False

def reciving(name, sock):
	while not shutdown:
		try:
			tLock.acquire()
			while True:
				data, addr = sock.recvfrom(1024)
				data = data.decode('utf-8')
				print(str(data))
		except:
			pass
		finally:
			tLock.release()

host = '127.0.0.1'
port = 0

server = ('127.0.0.1', 9029)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind((host, port))
s.setblocking(0)

rT = threading.Thread(target=reciving, args=("RecvThread", s))
rT.start()

alias = input("Name: ")
message = input(alias + "-> ")
while message != 'q':
	if message != '':
		s.sendto((alias + ": " + message).encode('utf-8'), server)
	time.sleep(0.2)
	tLock.acquire()
	message = input(alias + "-> ")
	tLock.release()

shutdown = True
rT.join()
s.close()

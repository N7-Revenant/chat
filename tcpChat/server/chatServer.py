#!/usr/bin/env python3
"""Multithread chat server"""

import socket
import threading
import time
import re

def  accept_connections():
	"""Handling of incoming clients"""
	
	while True:
		client, client_address = SERVER.accept()
		print("%s:%s has connected." % client_address)
		client.send(bytes("Connection established.", "utf-8"))
		#--Added for future use--
		#time.sleep(0.03)
		#client.send(bytes("Type login <login> <password> to enter as existing user.", "utf-8"))
		#time.sleep(0.03)
		#client.send(bytes("Type regitster <login> <password> to enter as new user.", "utf-8"))
		#time.sleep(0.03)
		#client.send(bytes("Type msg <login> <text> to send message for specific user.", "utf-8"))
		#time.sleep(0.03)
		#client.send(bytes("Type msgall <text> to send message for all users online.", "utf-8"))
		#-----------------
		time.sleep(0.03)
		client.send(bytes("Type {logout} to quit.", "utf-8"))
		addresses[client] = client_address
		threading.Thread(target=handle_client, args=(client,)).start()


def handle_client(client):
	"""Handles client connection"""
	
	name = client.recv(BUFFER_SIZE).decode("utf-8")
	if name == "{logout}":
		delete_client(client)
		return
	welcome = 'Welcome %s! If you want to quit, type {logout} to exit.' % name
	client.send(bytes(welcome, "utf-8"))
	msg = "%s has joined chat!" % name
	broadcast_message(bytes(msg, "utf-8"))
	clients[client] = name

	while True:
		msg = client.recv(BUFFER_SIZE)
		if msg != bytes("{logout}", "utf-8"):
			broadcast_message(msg, name+": ")
		else:
			delete_client(client)
			del clients[client]
			broadcast_message(bytes("%s has left the chat." % name, "utf-8"))
			break

def broadcast_message(msg, prefix=""):
	"""Broadcast a message to all active clients"""

	for sock in clients:
		sock.send(bytes(prefix, "utf-8")+msg)

clients = {}
addresses = {}

def delete_client(client):
	client.send(bytes("{logout}", "utf-8"))
	client.close()
	print ("%s:%s has disconnected" % addresses[client])

HOST = ''
PORT = 9029
BUFFER_SIZE = 1024

try:
	config=open('config.txt')
	for line in config:
		line = re.sub('\n', '', line)
		line = re.split('=', line)
		if line[0] == 'HOST':
			HOST = line[1]
		elif line[0] == 'PORT':
			PORT = int(line[1])
		elif line[0] == 'BUFFER_SIZE':
			BUFFER_SIZE = int(line[1])
	config.close()
except:
	pass

ADDR = (HOST, PORT)

SERVER = socket.socket()
SERVER.bind(ADDR)

if __name__ == "__main__":
	SERVER.listen(5)
	print("Server started. Waiting for connections...")
	ACCEPT_THREAD = threading.Thread(target=accept_connections)
	ACCEPT_THREAD.start()
	ACCEPT_THREAD.join()
	SERVER.close()

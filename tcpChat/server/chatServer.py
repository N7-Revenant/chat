#!/usr/bin/env python3
"""Multithread chat server"""

import socket
import threading
import time
import re

import connectDB

def  accept_connections():
	"""Handling of incoming clients"""
	
	while True:
		client, client_address = SERVER.accept()
		print("%s:%s has connected." % client_address)
		client.send(bytes("Connection established.", "utf-8"))
		time.sleep(0.08)
		client.send(bytes("Type regitster <login> <password> to enter as new user.", "utf-8"))
		time.sleep(0.08)
		client.send(bytes("Type login <login> <password> to enter as existing user.", "utf-8"))
		time.sleep(0.08)
		client.send(bytes("Type regitster <login> <password> to enter as new user.", "utf-8"))
		time.sleep(0.08)
		client.send(bytes("Type msg <login> <text> to send message for specific user.", "utf-8"))
		time.sleep(0.08)
		client.send(bytes("Type msgall <text> to send message for all users online.", "utf-8"))
		time.sleep(0.08)
		client.send(bytes("Type logout to quit.", "utf-8"))
		
		addresses[client] = client_address
		threading.Thread(target=handle_client, args=(client,)).start()


def slice_word(message):
	command = re.split(' ', message,1)
	if len(command) == 1:
		return command[0], ''
	else:
		return command[0], command[1]


def handle_client(client):
	"""Handles client connection"""

	login = ''

	while True:
		msg = client.recv(BUFFER_SIZE).decode("utf-8")
		command, text = slice_word(msg)
		if command in commands:
			if command == "logout":
				delete_client(client)
				return
			elif command == 'login':
				login, password = slice_word(text)
				if login in list(clients.values()):
					client.send(bytes("User already online", "utf-8"))
					continue
				elif not(connectDB.authorise(login, password)):
					client.send(bytes("Wrong login/password combination", "utf-8"))
					continue

			elif command == 'register':
				login, password = slice_word(text)
				if login in list(clients.values()):
					client.send(bytes("User already exists and online", "utf-8"))
					continue

				registered, message = connectDB.register(login, password)
				if registered:
					client.send(bytes(message, "utf-8"))
					time.sleep(0.1)
				else:
					client.send(bytes(message, "utf-8"))
					continue
			else:
				client.send(bytes("Register or Login first.", "utf-8"))
				continue
		else:
			client.send(bytes("Unknown command %s" % command, "utf-8"))
			continue
		welcome = 'Welcome %s!' % login
		client.send(bytes(welcome, "utf-8"))
		msg = "%s has joined chat!" % login
		broadcast_message(msg)
		clients[client] = login
		break

	while True:
		msg = client.recv(BUFFER_SIZE)
		command, text = slice_word(msg.decode('utf-8'))
		if command in commands:
			if command == 'msgall':
				broadcast_message(text, login)
			elif command == 'msg':
				target, text = slice_word(text)
				if not connectDB.check_user_exist(target):
					client.send(bytes("User %s doesn't exist" % target, "utf-8"))
				elif target not in list(clients.values()):
					client.send(bytes("User %s isn't online" % target, "utf-8"))
				else:
					for socket, user in clients.items():
						if user == target:
							private_message(client, socket, text)
					
			elif command == 'logout':
				delete_client(client)
				del clients[client]
				broadcast_message("%s has left the chat." % login)
				break
			else:
				client.send(bytes("Command %s is unavailable. You're already logged in." % command, "utf-8"))
		else:
			client.send(bytes("Unknown command %s" % command, "utf-8"))

def broadcast_message(msg, login=''):
	"""Broadcast a message to all active clients"""
	prefix = ''
	time_stamp = time.ctime(time.time())
	
	if len(login) != 0:
		prefix = login+': '
	
	for sock in clients:
		sock.send(bytes(prefix+msg, "utf-8"))
		if prefix!='':
			connectDB.log_message(time_stamp, login, '<broadcast>', msg)

def private_message(sender, reciver, message_text):
	"""Send private message to specific usser"""
	login = clients[sender]
	target = clients[reciver]
	time_stamp = time.ctime(time.time())
	reciver.send(bytes(login+"->"+target+": "+message_text, "utf-8"))
	sender.send(bytes(login+"->"+target+": "+message_text, "utf-8"))

	connectDB.log_message(time_stamp, login, target, message_text)

def delete_client(client):
	client.send(bytes("logout", "utf-8"))
	client.close()
	print ("%s:%s has disconnected" % addresses[client])


clients = {}
addresses = {}

commands = ('register', 'login', 'msg', 'msgall', 'logout')

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
	SERVER.listen(8)
	print("Server started. Waiting for connections...")
	ACCEPT_THREAD = threading.Thread(target=accept_connections)
	ACCEPT_THREAD.start()
	ACCEPT_THREAD.join()
	SERVER.close()

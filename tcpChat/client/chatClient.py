#!/usr/bin/env python3
"""Chat client with simple GUI"""

import socket
import threading
import tkinter
import re

def recive():
	"""Handles messages reciving"""
	while True:
		try:
			msg = client_socket.recv(BUFFER_SIZE).decode("utf-8")
			msg_list.insert(tkinter.END, msg)
		except:
			break

def send(event=None):
	"""Handles messages sending"""
	msg = my_msg.get()
	if msg != "":
		my_msg.set("")
		client_socket.send(bytes(msg, "utf-8"))
		if msg == "logout":
			client_socket.close()
			top.quit()

def onClosing(event=None):
	"""EventHandler for window closing"""
	my_msg.set("logout")
	send()

top = tkinter.Tk()
top.title("Chat")

messages_frame = tkinter.Frame(top)
my_msg = tkinter.StringVar()
my_msg.set("Name")
yscrollbar = tkinter.Scrollbar(messages_frame)

msg_list = tkinter.Listbox(messages_frame, height=20, width=60, yscrollcommand=yscrollbar.set)
yscrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
msg_list.pack()
messages_frame.pack()

entry_label = tkinter.Label(text="Command:")
entry_label.pack()

entry_field = tkinter.Entry(top, textvariable=my_msg, width=50)
entry_field.bind("<Return>", send)
entry_field.pack()

send_button = tkinter.Button(top, text="Send", command=send)

top.protocol("WM_DELETE_WINDOW", onClosing)

HOST = '127.0.0.1'
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

ADDRESS = (HOST, PORT)

client_socket = socket.socket()
client_socket.connect(ADDRESS)

recive_thread = threading.Thread(target=recive)
recive_thread.start()

tkinter.mainloop()


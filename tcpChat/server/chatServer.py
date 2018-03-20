#!/usr/bin/env python3
"""Multithreaded chat server"""

import socket
import threading
import time
import re
import mysql.connector

import requestSender


def accept_connections():
    """Handling of incoming clients"""

    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        client.send(bytes("Connection established.", "utf-8"))
        time.sleep(0.08)
        client.send(bytes("Type login <login> <password> to enter as existing user.", "utf-8"))
        time.sleep(0.08)
        client.send(bytes("Type register <login> <password> to enter as new user.", "utf-8"))
        time.sleep(0.08)
        client.send(bytes("Type msg <login> <text> to send message for specific user.", "utf-8"))
        time.sleep(0.08)
        client.send(bytes("Type msgall <text> to send message for all users online.", "utf-8"))
        time.sleep(0.08)
        client.send(bytes("Type logout to quit.", "utf-8"))

        addresses[client] = client_address
        threading.Thread(target=handle_client, args=(client,)).start()


def slice_word(message):
    """Slices first word of the string"""
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
                del addresses[client]
                return
            elif command == 'login':
                login, password = slice_word(text)
                if login in list(clients.values()):
                    client.send(bytes("User already online", "utf-8"))
                    continue
                elif not(requestSender.authorise(cursor, login, password)):
                    client.send(bytes("Wrong login/password combination", "utf-8"))
                    continue

            elif command == 'register':
                login, password = slice_word(text)
                if login in list(clients.values()):
                    client.send(bytes("User already exists and online", "utf-8"))
                    continue

                registered, message = requestSender.register(cursor, login, password)
                if registered:
                    connection.commit()
                    client.send(bytes(message, "utf-8"))
                    time.sleep(0.1)
                else:
                    client.send(bytes(message, "utf-8"))
                    continue
            else:
                client.send(bytes("Register or Login first.", "utf-8"))
                continue
        else:
            try:
                client.send(bytes("Unknown command %s" % command, "utf-8"))
                continue
            except:
                delete_client(client)
                del addresses[client]
                return
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
                if not requestSender.check_user_exist(cursor, target):
                    client.send(bytes("User %s doesn't exist" % target, "utf-8"))
                elif target not in list(clients.values()):
                    client.send(bytes("User %s isn't online" % target, "utf-8"))
                else:
                    for socket, user in clients.items():
                        if user == target:
                            private_message(client, socket, text)
                            connection.commit()

            elif command == 'logout':
                delete_client(client)
                del clients[client]
                del addresses[client]
                broadcast_message("%s has left the chat." % login)
                break
            else:
                client.send(bytes("Command %s is unavailable. You're already logged in." % command, "utf-8"))
        else:
            try:
                client.send(bytes("Unknown command %s" % command, "utf-8"))
            except:
                delete_client(client)
                del clients[client]
                del addresses[client]
                broadcast_message("%s has left the chat." % login)
                break


def broadcast_message(msg, login=''):
    """Broadcast a message to all active clients"""
    prefix = ''
    time_stamp = time.ctime(time.time())

    if len(login) != 0:
        prefix = login+': '
        requestSender.log_message(cursor, time_stamp, login, 'All users', msg)
        connection.commit()

    for sock in clients:
        sock.send(bytes(prefix+msg, "utf-8"))


def private_message(sender, receiver, message_text):
    """Send private message to specific user"""
    login = clients[sender]
    target = clients[receiver]
    time_stamp = time.ctime(time.time())
    receiver.send(bytes(login + "->" + target + ": " + message_text, "utf-8"))
    sender.send(bytes(login+"->"+target+": "+message_text, "utf-8"))

    requestSender.log_message(cursor, time_stamp, login, target, message_text)


def delete_client(client):
    """Send logout command back to client and closes socket"""
    try:
        client.send(bytes("logout", "utf-8"))
        client.close()
    except:
        pass
    print("%s:%s has disconnected" % addresses[client])


clients = {}
addresses = {}

commands = ('register', 'login', 'msg', 'msgall', 'logout')

HOST = ''
PORT = 9029,
BUFFER_SIZE = 1024

DB_USER = 'chat'
DB_PASS = 'Rfv753'
DB_HOST = 'localhost'
DB_NAME = 'tcpChat'

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
        elif line[0] == 'DB_USER':
            DB_USER = line[1]
        elif line[0] == 'DB_PASS':
            DB_PASS = line[1]
        elif line[0] == 'DB_HOST':
            DB_HOST = line[1]
        elif line[0] == 'DB_NAME':
            DB_NAME = line[1]

    config.close()

except:
    pass

ADDRESS = (HOST, PORT)

connection = mysql.connector.connect(user=DB_USER, password=DB_PASS, host=DB_HOST, database=DB_NAME)
cursor = connection.cursor()

SERVER = socket.socket()
SERVER.bind(ADDRESS)

SERVER.listen(8)
print("Server started. Waiting for connections...")
ACCEPT_THREAD = threading.Thread(target=accept_connections)
ACCEPT_THREAD.start()
ACCEPT_THREAD.join()
SERVER.close()

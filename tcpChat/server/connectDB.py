"""Handles DB connections for chatServer"""
#TODO: add actual connection to DB later, for now let's work with files

import re

def authorise(login, password):
	try:
		users = open('users.txt')
		for line in users:
			line = re.sub('\n', '', line)
			line = re.split(' ', line)
			if line[0] == login and line[1] == password:
				return True
			else:
				return False
		users.close()
	except:
		return False

def check_user_exist(login):
	try:
		users = open('users.txt')
		for line in users:
			line = re.sub('\n', '', line)
			line = re.split(' ', line)
			if line[0] == login:
				return True
			else:
				return False
		users.close()
	except:
		return False

def register(login, password):
	if len(login) < 3:
		return False, 'Login must contain at least 3 symbols.'
	elif len(password)< 3:
		return False, 'Password must contain at least 3 symbols.'
	elif check_user_exist(login):
		return False, 'This login already taken.'
	else:
		try:
			users = open('users.txt', 'a')
			users.write(login+' '+password+'\n')
			users.close()
			return True, 'New user added successefully.'
		except:
			return False, 'Internal error'
		


"""Handles DB connections for chatServer"""
#TODO: add actual connection to DB later, for now let's work with files

import re
import hashlib

def authorise(login, password):
	user_authorised = False
	try:
		users = open('users.txt')
		for line in users:
			line = re.sub('\n', '', line)
			line = re.split(' ', line)
			if line[0] == login and line[1] == hashlib.md5(password.encode()).hexdigest():
				user_authorised =  True
				break
		users.close()
	except:
		pass

	return user_authorised

def check_user_exist(login):
	user_found = False

	try:
		users = open('users.txt')
		for line in users:
			line = re.sub('\n', '', line)
			line = re.split(' ', line)
			if line[0] == login:
				user_found =  True
				break
		users.close()
	except:
		pass
	
	return user_found

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
			users.write(login+' '+hashlib.md5(password.encode()).hexdigest()+'\n')
			users.close()
			return True, 'New user added successefully.'
		except:
			return False, 'Internal error'

def log_message(time, sender, reciver, text):
	log_entry = time+'\t'+sender+'\t'+reciver+'\t'+text+'\n'
	try:
		log = open('log.txt', 'a')
		log.write(log_entry)
		log.close()
	except:
		print("Error logging message: " + log_entry)


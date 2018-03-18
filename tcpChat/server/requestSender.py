"""Handles DB connections for chatServer"""

import re
import hashlib

def authorise(cursor, login, password):
	"""User authorisation"""
	user_authorised = False
	try:
		find_user = ("SELECT login FROM users WHERE login='"+login+"' AND password='"+str(hashlib.md5(password.encode()).hexdigest())+"'")
		cursor.execute(find_user)
		data = cursor.fetchall()
		if cursor.rowcount > 0:
			user_authorised = True
	except:
		pass

	return user_authorised

def check_user_exist(cursor, login):
	"""Check for user existance"""
	user_found = False
	try:
		find_user = ("SELECT login FROM users WHERE login='" + login + "'")
		cursor.execute(find_user)
		data = cursor.fetchall()
		if cursor.rowcount > 0:
			user_found = True
	except:
		pass
	
	return user_found

def register(cursor, login, password):
	"""Registration of new user"""
	if len(login) < 3:
		return False, 'Login must contain at least 3 symbols.'
	elif len(password)< 3:
		return False, 'Password must contain at least 3 symbols.'
	elif check_user_exist(cursor, login):
		return False, 'This login already taken.'
	else:
		try:
			register_user = ("INSERT INTO users (login, password) VALUES (%s, %s)")
			cursor.execute(register_user,(login, str(hashlib.md5(password.encode()).hexdigest())))
			return True, 'New user added successefully.'
		except:
			return False, 'Internal error'

def log_message(cursor, time, sender, reciver, text):
	"""Logging message"""
	log_entry = time+'\t'+sender+'\t'+reciver+'\t'+text+'\n'
	try:
		log_message = ("INSERT INTO log (time, sender, reciver, message) VALUES (%s, %s, %s, %s)")
		cursor.execute(log_message,(time, sender, reciver, text))
	except:
		print("Error logging message: " + log_entry)


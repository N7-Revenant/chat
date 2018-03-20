"""Handles DB connections for chatServer"""

import re
from hashlib import md5


def authorise(cursor, login, password):
    """User authorisation"""
    user_authorised = False
    try:
        find_user = ("SELECT login FROM users WHERE login='" +
                     login + "' AND password='" +
                     str(md5(password.encode()).hexdigest()) + "'")
        cursor.execute(find_user)
        data = cursor.fetchall()
        if cursor.rowcount > 0:
            user_authorised = True
    except:
        pass

    return user_authorised


def check_user_exist(cursor, login):
    """Check for user existence"""
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
    elif len(password) < 3:
        return False, 'Password must contain at least 3 symbols.'
    elif check_user_exist(cursor, login):
        return False, 'This login already taken.'
    else:
        try:
            register_user = "INSERT INTO users (login, password) VALUES (%s, %s)"
            cursor.execute(register_user,(login, str(md5(password.encode()).hexdigest())))
            return True, 'New user added successfully.'
        except:
            return False, 'Internal error'


def log_message(cursor, time, sender, receiver, text):
    """Logging message"""
    log_entry = time +'\t' + sender +'\t' + receiver + '\t' + text + '\n'
    try:
        log_entry = "INSERT INTO log (time, sender, receiver, message) VALUES (%s, %s, %s, %s)"
        cursor.execute(log_entry, (time, sender, receiver, text))
    except:
        print("Error logging message: " + log_entry)


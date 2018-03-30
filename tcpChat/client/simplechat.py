"""simplechat package with basic chat client interface"""

import re
import socket
import threading


class Controller:
    """Basic chat functions controller class"""
    def __init__(self):
        self.__conf = {
            'HOST': '127.0.0.1',
            'PORT': 9029,
            'BUFFER_SIZE': 1024
            }
        self.__exit_msg = 'logout'
        self.__socket = None
        self.__err_code = 0
        self.__error = threading.Event()

        self.__send_interface_update_func = None
        self.__receive_interface_update_func = None

        self.__error_codes_list = [
            'Unknown error',
            'Socket connection failed.',
            'Error happened while receiving message, connection severed',
            'Error happened while sending message, connection severed',
            'No socket connection established',
            'Logout message received, connection severed'
            ]

        self.__error_handler = None

        self.__err_thread = threading.Thread(target=self.error_catcher, args=(self.__error,))
        self.__err_thread.daemon = True
        self.__receive_thread = threading.Thread(target=self.receive_message)

        self.__err_thread.start()

    def set_send_interface_update_func(self, send_func):
        """Sets interface update callback function on sending message"""
        self.__send_interface_update_func = send_func

    def set_receive_interface_update_func(self, receive_func):
        """Sets interface update callback function on receiving message"""
        self.__receive_interface_update_func = receive_func

    def set_error_handler_func(self, error_handler):
        """Sets error handler callback function"""
        self.__error_handler = error_handler

    def get_error_description(self, index):
        """Get error description by code"""
        i = index
        try:
            desc = self.__error_codes_list[i]

        except IndexError:
            desc = self.__error_codes_list[0]

        return desc

    def update_config(self, config_file):
        """Updates configuration dictionary with data from configuration file"""
        cf = config_file

        try:
            config = open(cf)
            for line in config:
                line = re.sub('\n', '', line)
                line = re.split('=', line)
                if line[0] == 'HOST':
                    try:
                        self.__conf[line[0]] = line[1]
                    except ValueError:
                        pass
                else:
                    try:
                        self.__conf[line[0]] = int(line[1])
                    except ValueError:
                        pass
            config.close()

        except FileNotFoundError:
            pass

    def connect(self):
        """Creates connection to Chat server via socket"""
        try:
            self.__socket = socket.socket()
            self.__socket.connect((self.__conf['HOST'], self.__conf['PORT']))
        except:
            self.__err_code = 1
            self.__error.set()

    def receive_message(self):
        """Receives messages via specified socket"""
        if self.__socket is not None:
            msg = 'text'
            while msg != '':
                msg = self.__socket.recv(self.__conf['BUFFER_SIZE']).decode("utf-8")
                if msg == self.__exit_msg:
                    self.__err_code = 5
                    self.__error.set()
                    break
                if self.__receive_interface_update_func is not None:
                    self.__receive_interface_update_func(msg)
            else:
                self.__err_code = 2
                self.__error.set()
        else:
            self.__err_code = 4
            self.__error.set()

    def send_message(self, message):
        """Sends message via specified socket"""
        msg = message
        if self.__socket is not None:
            try:
                if msg != '':
                    self.__socket.send(bytes(msg, "utf-8"))
                if self.__send_interface_update_func is not None:
                    self.__send_interface_update_func()
            except:
                self.__err_code = 3
                self.__error.set()
        else:
            self.__err_code = 4
            self.__error.set()

    def close_connection(self):
        """Closes connection via specified socket"""
        if self.__socket is not None:
            self.__socket.close()
            self.__socket = None

    def start_chat(self):
        """Starts chat connection and receiving thread"""
        self.connect()
        if self.__socket is not None:
            self.__receive_thread.start()

    def stop_chat(self):
        """Stops chat connection and receiving thread"""
        if self.__receive_thread.is_alive():
            self.__receive_thread.join()
        self.close_connection()

    def error_catcher(self, event):
        """Catches all error and logout events"""
        e = event
        while True:
            e.wait()
            self.stop_chat()
            if self.__error_handler is not None:
                self.__error_handler(self.__err_code)
            e.clear()

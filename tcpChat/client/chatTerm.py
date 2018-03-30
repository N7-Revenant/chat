"""Terminal chat client with shared simplechat package dependency"""


from simplechat import Controller


class Terminal:
    """Terminal class for simple chat program"""
    def __init__(self, control):
        self.__control = control

        self.__control.set_send_interface_update_func(self.send)
        self.__control.set_receive_interface_update_func(self.receive)
        self.__control.set_error_handler_func(self.error_handler)

        self.__exit_function = None

    def set_exit_func(self, exit_func):
        """Sets callback exit function"""
        self.__exit_function = exit_func

    def receive(self, msg):
        """Updates message list with new message"""
        print(msg)

    def send(self):
        """Takes user messages and send it via chat controller"""
        msg = input('')
        self.__control.send_message(msg)

    def error_handler(self, index):
        """Handles error events received from chat controller"""
        i = index
        if i != 5:
            print("Error: %s" % self.__control.get_error_description(i))
        else:
            print(self.__control.get_error_description(i))
        print("Press <Enter> to exit")
        self.__exit_function()

    def start_chat(self):
        """Starts chat"""
        self.__control.start_chat()

        self.send()


def close_program():
    """Closing program"""
    exit()


def main():
    """Main function"""
    control = Controller()

    control.update_config('config.txt')

    term = Terminal(control)

    term.set_exit_func(close_program)

    term.start_chat()


if __name__ == '__main__':
    main()
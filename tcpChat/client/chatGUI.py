"""GUI chat client with shared simple-chat package dependency"""

import tkinter

from simplechat import Controller


class GUI:
    """GUI class for simple chat program based on Tkinter module"""
    def __init__(self, control):

        self.__control = control

        self.__control.set_receive_interface_update_func(self.update_message_list)
        self.__control.set_error_handler_func(self.error_handler)

        self.__top = tkinter.Tk()
        self.__top.title("Chat")

        self.__messages_frame = tkinter.Frame(self.__top)
        self.__my_msg = tkinter.StringVar()
        self.__my_msg.set("")
        self.__scrollbar = tkinter.Scrollbar(self.__messages_frame)

        self.__msg_list = tkinter.Listbox(self.__messages_frame, height=20, width=60, yscrollcommand=self.__scrollbar.set)
        self.__scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        self.__msg_list.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        self.__msg_list.pack()
        self.__messages_frame.pack()

        self.__entry_label = tkinter.Label(text="Command:")
        self.__entry_label.pack()

        self.__entry_field = tkinter.Entry(self.__top, textvariable=self.__my_msg, width=50)
        self.__entry_field.bind("<Return>", self.send)
        self.__entry_field.pack()

        self.__top.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.__exit_function = None

    def set_exit_func(self, exit_func):
        """Sets callback exit function"""
        self.__exit_function = exit_func

    def update_message_list(self, msg):
        """Updates message list with new message"""
        self.__msg_list.insert(tkinter.END, msg)

    def send(self, event=None):
        """Sends user message via chat controller"""
        msg = self.__my_msg.get()
        if msg != '':
            self.__my_msg.set('')
            self.__control.send_message(msg)

    def error_handler(self, index):
        """Handles error events received from chat controller"""
        i = index
        if i != 5:
            print("Error: %s" % self.__control.get_error_description(i))
        self.__exit_function()

    def on_closing(self, event=None):
        """EventHandler for window closing"""
        self.__my_msg.set("logout")
        self.send()

    def stop_chat(self):
        """Exit function"""
        self.__control.stop_chat()
        self.__top.quit()

    def start_chat(self):
        """Starts chat"""
        self.__control.start_chat()

        self.send()


def main():
    """Main function"""
    control = Controller()

    control.update_config('config.txt')

    gui = GUI(control)

    gui.set_exit_func(gui.stop_chat)

    gui.start_chat()

    tkinter.mainloop()


if __name__ == '__main__':
    main()
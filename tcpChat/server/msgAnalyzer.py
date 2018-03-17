import re


def analyze(message):
	command = re.split(' ', message,1)
	if len(command) == 1:
		return command[0], ''
	else:
		return command[0], command[1]

if __name__ == '__main__':
	#code for testing
	a, b = analyze('fjdskalghkldf')
	if a != 'unknown':
		print("Command is: " + a + ", text is: " + b)
	else:
		print("Unknown command.")

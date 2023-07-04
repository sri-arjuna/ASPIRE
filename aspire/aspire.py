"""
	Created on:		2023.July.02
	Created by:		Simon Arjuna Erat
	License:		MIT
	URL:			https://www.github.com/sri-arjuna/ASPIRE
"""

from .aspire_utils_print import PrintUtils as put
import sys
import os

class Aspire:
	def __init__(self):
		put.text("Hello, World!")
		put.border()

	@staticmethod
	def header(str1, str2, str3):
		# Implementation for header method
		pass

	@staticmethod
	def title(text):
		# Implementation for title method
		pass

	@staticmethod
	def print(*args, end='\n'):
		# Implementation for printe method
		put.border()
		put.text(args, end=end)
		pass

	@staticmethod
	def press(text=None):
		# if no text is passed, prints "Press enter to continue" left and right
		if text is None or text == "":
			text = "Please press any key to continue"
		Aspire.print(text, text)
		# Workaround to hide the default message
		stdout = os.dup(1)
		os.dup2(os.open(os.devnull, os.O_WRONLY), 1)
		os.system("pause")
		os.dup2(stdout, 1)

	@classmethod
	def status(cls, text, end='\n'):
		# Prints the "text" on the left, and a status indicator on the right
		pass


"""
	Created on:		2023.July.02
	Created by:		Simon Arjuna Erat
	License:		MIT
	URL:			https://www.github.com/sri-arjuna/ASPIRE
"""


# Imports
import sys
import os
from enum import Enum

# Internals
from .aspire_core import PrintUtils as put
from .aspire_core import AspireCore as AC
from .aspire_core import Theme
from .aspire_data_status import StatusEnum
from .aspire_data_status import dict_status



os.system("")

class Aspire:
	@staticmethod
	def header(*args, style="header", end='\n'):
		# Implementation for header method
		put.border(style=style)
		put.text(*args, style=style, end=end)

	@staticmethod
	def title(text=None, style="title", end='\n'):
		# Implementation for title method
		put.border(style=style)
		put.text(text, style=style, end=end)

	@staticmethod
	def print(*args, end='\n'):
		# Implementation for printe method
		if len(args) == 1:
			single_arg = args[0]
			if isinstance(single_arg, str) and '\n' in single_arg:
				lines = single_arg.strip().split('\n')
				for line in lines:
					put.border()
					put.text(line, end='\n')
			elif isinstance(single_arg, list):
				for line in single_arg:
					put.border()
					put.text(line, end='\n')
			else:
				put.border()
				put.text(single_arg, end=end)
		else:
			put.border()
			put.text(*args, end=end)

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
	def yesno(self, question: str, yesno_option="yn") -> bool:
		theme = Theme.get()
		answer = ""
		question_string = f"{question} ({yesno_option}) {theme.prompt_read} "
		yes = yesno_option[:1]
		no = yesno_option[1:]
		
		# Default Aspire / TUI output
		put.border()
		put.text(question_string, end="")
		#sys.stdout.flush()		# Makes no difference

		# Loop for proper input:
		while True:
			# Make input ready to be checked
			answer = AC.get_input_charcount(1) 
			#answer = input()
			if answer in yesno_option:
				break
		# Print answer
		put._right(answer)
		# Return the according bool
		if answer in yes and "" != answer:
			return True
		elif answer in no and "" != answer:
			return False

	@staticmethod
	def status(ID, text, end='\n'):
		# Prints the "text" on the left, and a status indicator on the right
		if isinstance(ID, int):
			entry = dict_status[str(ID)]
			# TODO: FIX use of eval
			display = eval(entry)
			Aspire.print(text, f"[ {display.value} ]", end=end)
			return ID
		elif isinstance(ID, bool):
			entry = dict_status[str(ID)]
			display = getattr(StatusEnum, entry)
			Aspire.print(text, f"[ {display.value} ]", end=end)
			return ID
		elif isinstance(ID, Enum):
			Aspire.print(text, f"[ {ID.value} ]", end=end)
		else:
			print("Wrong type: ", ID)

	@classmethod
	def progress(self, text: str, cur: float, max: float, fstyle="bar"):
		if "num" == fstyle:
			prog_out = f"{cur} / {max}"
		elif "bar" == fstyle:
			theme = Theme.get()
			AC._console_width = AC._get_terminal_width()
			# Get default subtractions
			width = AC._console_width - 2 * len(theme.border_left) - len(text) -2
			# Get the actual size for the bar
			width_work = width - 2 - int(width / 6)
			# Placeholer - respece this space
			prog_full = theme.bar_empty * width_work  #int(len(theme.bar_empty) / width_work * max)
			# Prepare the progress that has been done
			#prog_done = theme.bar_full * int(width_work / 100 * cur)
			prog_done = theme.bar_full * int(width_work * (cur / max))
			cut_len = len(prog_done)
			# Cut off what has been done from placeholder
			prog_full = prog_full[:-cut_len]
			# Final step
			#p = 100 / max * cur
			p = format(100 * cur / max, ".2f")
			prog_out = f"[{prog_done}{prog_full}] {p}%"
		else:
			prog_out = "failed progress"
		put.border()
		put.text(text, f"{prog_out}")


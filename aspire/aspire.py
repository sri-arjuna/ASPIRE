"""
	Created on:		2023.July.02
	Created by:		Simon Arjuna Erat
	License:		MIT
	URL:			https://www.github.com/sri-arjuna/ASPIRE
"""

from .aspire_core import PrintUtils as put
from .aspire_core import AspireCore as AC
from .aspire_core import Theme
import sys
import os

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
	def status(self, text, end='\n'):
		# Prints the "text" on the left, and a status indicator on the right
		pass

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
			prog_out = f"[{prog_done}{prog_full}]"
			#p = 100 / max * cur
			p = format(100 * cur / max, ".2f")
		else:
			prog_out = "failed progress"
		put.border()
		put.text(text, f"{prog_out} {p}%")


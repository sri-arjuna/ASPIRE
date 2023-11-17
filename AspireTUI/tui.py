"""
	Created on:		2023 Nov. 09
	Created by:		Simon Arjuna Erat
	License:		MIT
	URL:			https://www.github.com/sri-arjuna/ASPIRE

	Based on my TUI & SWARM for the BASH shell © 2011
"""
################################################################################################################
#####                                            Shared Imports                                            #####
################################################################################################################
#
#	Essential imports
#
import os
import sys
import re
import string
#
#	Cross Platform & Advanced usage
#
import platform
import msvcrt
import shutil
import subprocess
from typing import Union
#
#	Prepare for multi language support
#
import gettext #as _
from pathlib import Path
# Lang setup
translation_directory = Path("locales")
translation = gettext.translation("AspireTUI", translation_directory, fallback=True)
translation.install()
#
#	Internals
#
import AspireTUI._PrintUtils as put
import AspireTUI._theme as Theme
import AspireTUI.StringUtils as stew
from . import settings
################################################################################################################
#####                                           Public Functions                                           #####
################################################################################################################
def header(*args, end='\n'):
	"""
	Prints up to 3 strings, L, L+R, LCR.
	Theme:Default = White font and blue background.
	"""
	put._update(True)
	style="header"
	put.border(style=style)
	put.text(*args, style=style, end=end)

def title(text="", end='\n'):
	"""
	Prints 1 (one) string in the center.
	Theme:Default = Blue font and white background.
	"""
	put._update()
	style="title"
	put.border(style=style)
	put.text(text, style=style, end=end)

def print(*args, end='\n'):
	"""
	Default output method.
	Prints up to 3 strings, L, L+R, LCR.
	Theme:Default = Blue font and white background for borders, default console colors for output.
	"""
	# Implementation for printe method
	put._update()
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

def press(text=None):
	"""
	Theme conform wrapper for os.system("pause").
	If no text is passed, "Please press any key to continue." is used.
	If passed or default text fits twice on the line, it will do so, otherwise center.
	"""
	put._update()
	if text is None or text == "":
		text = _("Please press any key to continue.")
	put.border()
	if settings["inner"] >= 2 * (len(text) + 1):
		# Fits twice
		put.text(text, text)
	else:
		# Fits only once
		put.text(text)
	# Workaround to hide the default message
	stdout = os.dup(1)
	os.dup2(os.open(os.devnull, os.O_WRONLY), 1)
	os.system("pause")
	os.dup2(stdout, 1)

def yesno(question: str, yesno_option="yn") -> bool:
	"""
	Ask the user a simple yes/no question.
	Pass an optional 2 character-string, of which 1. is positive and 2. is negative.
	"""
	put._update()
	style = Theme.get()
	answer = ""
	question_string = f"{question} ({yesno_option}) {style.prompt_read} "
	yes = yesno_option[:1]
	no = yesno_option[1:]
	
	# Default Aspire / TUI output
	put.border()
	put.text(question_string, end="")

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

def status(ID: Union[int, bool], *args, align_right=True, end='\n'):
	"""
	Requires ID to be int or bool, and 1 additional string as message for the status.					\n
	By default (orientation=right), text is printed left, center, and the actual status on the right.	\n

	Change orientation=left to have status on the left, main text on the right. If an optional text is passed,
	main text will be in the center and the optional text on the right.
	"""
	if len(args) > 2:
		msg_status_many_args = _("Too many strings, only 2 accepted.")
		raise SyntaxError(msg_status_many_args)

	put._update()
	put.border()

	if len(args) == 0:
		if align_right:
			put.text("", put.status(ID), end=end)
		else:  # left
			put.text(put.status(ID),  "", end=end)
	else:
		if align_right:
			put.text(*args, put.status(ID), end=end)
		else:  # left
			put.text(put.status(ID), *args, end=end)

def progress( text: str, cur: float, max: float, style: str = "bar", cut_from_end: bool = True, reverse: bool = False):
	"""
	Prints a leading 'text' with a progress indicator according to passed style.	\n
	If no 'text' is passed (read: empty-string=""), the progress bar fills all of the screen, otherwise its 50/50.
	Default style is 'bar'.		\n
	Valid styles are: bar, num	\n
	"""
	put._update(DEBUG=text)
	if "num" == style:
		prog_out = f"{cur} / {max}"
		return True
	elif "bar" == style:
		if text:
			width = settings["inner"] / 2
		else:
			# TODO: Why do i need " - 14" for this value???
			width = settings["inner"] - 12
		prog_out = f"{put.bar(cur,max,width,reverse=reverse)}"
	else:
		msg_progress_style = _("Wrong style for progress, only 'bar' and 'num' are supported.")
		raise ValueError(msg_progress_style)
	
	if text == "":
		text_new = ""	# There is no text anyway... idk...
	else:
		if cut_from_end:
			text_new = stew.shorten(text, width)
		else:
			text_new = stew.shorten(text, width, True)
	put.border()
	put.text(text_new, prog_out, end="")
	if cur == max:
		print()
	return True

def wait(Time: Union[float, int] ,  msg=None, unit="s",hidden=False, bar=False):
	"""
	If just used as: tui.wait(1), it waits for 1 second before it continues. \n
	To save effort, you can change unit="h" if you want to wait 1 hour instead,
	or use unit="m" to wait the passed number in minutes.

	"""
	# Init final vars:
	output = ""
	# Get measurement
	if unit == "s":
		secs = Time
	else:
		secs = Time
		print("TODO work with other time units for wait")
		# TODO: sec2time , min2sec, hour2sec
	
	# Prepare strings:
	if msg is not None:
		str_left = msg
	


def msgbox(*args, bOutside=False):
	# Print "border"
	put._update()
	if bOutside:
		header()
	else:
		title()
	# Print the content
	if len(args) > 1:
		for a in args:
			print(a)
		else:
			print(args)
	# Print "border"
	if bOutside:
		header()
	else:
		title()

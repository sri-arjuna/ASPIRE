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
import os as _os
#
#	Cross Platform & Advanced usage
#
#import platform as _platform
#import msvcrt as _msvcrt
#import shutil as _shutil
#import subprocess as _subprocess
from typing import Union as _Union
import time as _time

#
#	Internals
#
from AspireTUI import _settings_console as _settings
from AspireTUI import _MSG
from AspireTUI.__core import _internal
from AspireTUI.__core import _PrintUtils as _put
from AspireTUI.__core import _theme as _Theme
import AspireTUI.strings as _stew

################################################################################################################
#####                                           Public Functions                                           #####
################################################################################################################
def header(*args, end='\n'):
	"""
	Expects:
		Up to 3 strings.
	Usage:
		tui.header("left", "right")
		tui.header("left", "center", "right")
		tui.header("", "", "right")
	Prints up to 3 strings, L, L+R, LCR.
	Theme:Default = White font and blue background.
	"""
	_put._update(forced=True)
	style="header"
	_put.border(style=style)
	_put.text(*args, style=style, end=end)

def title(text="", end='\n'):
	"""
	Prints 1 (one) string in the center.
	Theme:Default = Blue font and white background.
	"""
	_put._update()
	style="title"
	_put.border(style=style)
	_put.text(text, style=style, end=end)

def print(*args, end='\n'):
	"""
	Default output method.
	Prints up to 3 strings, L, L+R, LCR.
	Theme:Default = Blue font and white background for borders, default console colors for output.
	"""
	# Implementation for printe method
	_put._update()
	if len(args) == 1:
		single_arg = args[0]
		if isinstance(single_arg, str) and '\n' in single_arg:
			lines = single_arg.strip().split('\n')
			for line in lines:
				_put.border()
				_put.text(line, end='\n')
		elif _stew.isList(single_arg):
			for line in single_arg:
				_put.border()
				_put.text(line, end='\n')
		else:
			_put.border()
			_put.text(single_arg, end=end)
	else:
		_put.border()
		_put.text(*args, end=end)

def press(text=None):
	"""
	Theme conform wrapper for _os.system("pause").
	If no text is passed, "Please press any key to continue." is used.
	If passed or default text fits twice on the line, it will do so, otherwise center.
	"""
	_put._update()
	if text is None or text == "":
		text = _MSG.tui_press
	_put.border()
	if _settings["inner"] >= 2 * (len(text) + 1):
		# Fits twice
		_put.text(text, text)
	else:
		# Fits only once
		_put.text(text)
	# Workaround to hide the default message
	stdout = _os.dup(1)
	_os.dup2(_os.open(_os.devnull, _os.O_WRONLY), 1)
	_os.system("pause")
	_os.dup2(stdout, 1)

def yesno(question: str, yesno_option="yn") -> bool:
	"""
	Ask the user a simple yes/no question.
	Pass an optional 2 character-string, of which 1. is positive and 2. is negative.
	"""
	_put._update()
	style = _Theme.get()
	answer = ""
	question_string = f"{question} ({yesno_option}) {style.prompt_read} "
	yes = yesno_option[:1]
	no = yesno_option[1:]
	
	# Default Aspire / TUI output
	_put.border()
	_put.text(question_string, end="")

	# Loop for proper input:
	while True:
		# Make input ready to be checked
		answer = _internal.get_input_charcount(1) 
		#answer = input()
		if answer in yesno_option:
			break
	# Print answer
	_put._right(answer)
	# Return the according bool
	if answer in yes and "" != answer:
		return True
	elif answer in no and "" != answer:
		return False

def status(ID: _Union[int, bool], *args, align_right=True, end='\n'):
	"""
	Requires ID to be int or bool, and 1 additional string as message for the status.					\n
	By default (orientation=right), text is printed left, center, and the actual status on the right.	\n

	Change orientation=left to have status on the left, main text on the right. If an optional text is passed,
	main text will be in the center and the optional text on the right.
	"""
	if len(args) > 2:
		msg_status_many_args = _MSG.args_2_status
		raise SyntaxError(msg_status_many_args)

	_put._update()
	_put.border()

	if len(args) == 0:
		if align_right:
			_put.text("", _put.status(ID), end=end)
		else:  # left
			_put.text(_put.status(ID),  "", end=end)
	else:
		if align_right:
			_put.text(*args, _put.status(ID), end=end)
		else:  # left
			_put.text(_put.status(ID), *args, end=end)

def progress( text: str, cur: float, max: float, style: str = "bar", cut_from_end: bool = True, reverse: bool = False):
	"""
	Prints a leading 'text' with a progress indicator according to passed style.	\n
	If no 'text' is passed (read: empty-string=""), the progress bar fills all of the screen, otherwise its 50/50.
	Default style is 'bar'.		\n
	Valid styles are: bar, num	\n
	"""
	_put._update()	# DEBUG=text
	if text:
		width = _settings["inner"] / 2
	else:
		# TODO: Why do i need " - 12" for this value???
		width = _settings["inner"] - 12
	# Styles
	if "num" == style:
		prog_out = f"[ {cur} / {max} ]"
		#return True
	elif "bar" == style:
		prog_out = f"{_put.bar(cur,max,width,reverse=reverse)}"
	else:
		msg_progress_style = _MSG.tui_progress_bar
		raise ValueError(msg_progress_style)
	
	if text == "":
		text_new = ""	# There is no text anyway... idk...
	else:
		# Send to shorten anyway, 
		# this should avoid the split test in _put.text().
		if cut_from_end:
			text_new = _internal.shorten(text, width)
		else:
			text_new = _internal.shorten(text, width, True)
	_put.border()
	_put.text(text_new, prog_out, end="")
	if cur == max:
		print()
	return True

def wait(Time: _Union[float, int] ,  msg=None, unit="s",hidden=False, bar=False, iIntervall=1):
	"""
	If just used as: tui.wait(1), it waits for 1 second before it continues. \n
	To save effort, you can change unit="h" if you want to wait 1 hour instead,
	or use unit="m" to wait the passed number in minutes.

	"""
	# Init final vars:
	output = ""
	# Get measurement
	secs = Time
	org = Time
	if not unit == "s":
		secs = _stew.sec2time(secs)
		print(secs, "TODO work with other time units for wait")
		# TODO: sec2time , min2sec, hour2sec
	
	# Prepare strings:
	if msg is None:
		msg = _MSG.tui_wait_continue_in
	
	cur = secs
	while cur > 0:
		print(msg,f"{stew.sec2time(cur)} / {Time}{unit}")
		cur -= 1
		## https://realpython.com/python-sleep/
		## Async? or time.wait instead ??
		_time.sleep(iIntervall)
	

def msgbox(*args, bOutside=False):
	"""
	
	"""
	# Print "border"
	_put._update()
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

def list(*args, bRoman=False, bMenu=False, sSeperator=")"):
	"""
	Prints a list 
	"""
	if bMenu:
		list_entries = [ _MSG.tui_list_back ] *args

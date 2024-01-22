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
from collections import namedtuple as _namedtuple
#
#	Prepare data structures
#
from enum import Enum as _Enum
#
#	Internals
#
from . import _settings_console as _settings
from ._MESSAGES import current as _MSG
from . import Strings as _stew
from . import _internal
from . import _PrintUtils as _put
from . import _theme as _Theme


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
	style="header"
	_put._update(forced=True)
	_put.border(style=style)
	_count = len(args)
	if 0 == _count:
		_put.text("",style=style, end=end)
	elif 3 < _count:
		raise IndexError(_MSG.args_max3, *args)
	elif 1 <= _count:
		_put.text(*args, style=style, end=end)

def title(*args, end='\n'):
	"""
	Prints 1 (one) string in the center.
	Theme:Default = Blue font and white background.
	"""
	_put._update()
	style="title"
	_count = len(args)
	_put.border(style=style)
	if 1 == _count:
		# As expected
		_put.text(args[0], style=style, end=end)
	if 3 < _count:
		raise IndexError(_MSG.args_title, _count, args)
	elif _count == 0 or args is None or args[0] == "":
		# Probably empty
		_put.text("", style=style, end=end)

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
	elif len(args) == 0:
		_put.border()
		_put.text("", end=end)
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

def yesno(question: str, yesno_option="yn", bDual=False, msg_yes=None, msg_no=None) -> bool:
	"""
	Ask the user a simple yes/no question. \n
	Pass an optional 2 character-string, of which 1. is positive and 2. is negative. \n

	If bDual is enabled, you MUST provide: 'msg_yes' and 'msg_no'!
	"""
	# Sanity check
	if bDual:
		if msg_yes is None or msg_no is None:
			raise ValueError(_MSG.tui_yesno_bDual_missing_msg)
	# Init
	_put._update()
	style = _Theme.get()
	answer = ""
	question_string = f"{question} ({yesno_option}) {style.prompt_read} "
	yes = yesno_option[:1]
	no = yesno_option[1:]
	# Default Aspire / TUI output
	_put.border()
	str_ret =  _put.status(_put.STATUS.Work)
	_put.text(question_string, str_ret, end="")
	_put._cursor2pos(len(question_string) + 5)
	# Loop for proper input:
	while True:
		# Make input ready to be checked
		answer = _internal.get_input_charcount(1)
		if answer in yesno_option:
			break
	# Prepare for output
	if answer in yes and "" != answer:
		ret = True
		msg = msg_yes
	elif answer in no and "" != answer:
		ret = False
		msg = msg_no
	# Print answer and return the according value/s
	answer = _put.status(ret)
	if bDual:
		print(question_string, _put._right(answer), end="\n")
		return ret, msg
	else:
		print(question_string, _put._right(answer))
		return ret

def status(ID: _Union[int, bool, _namedtuple], *args, align_right=True, end='\n', bDual=False):
	"""
	Requires ID to be int or bool, and 1 additional string as message for the status.					\n
	By default (orientation=right), text is printed left, center, and the actual status on the right.	\n

	Change orientation=left to have status on the left, main text on the right. If an optional text is passed,
	main text will be in the center and the optional text on the right.
	"""
	# init
	ret_status = None
	ret_value = None
	# Check arg count
	if len(args) > 2:
		raise SyntaxError(_MSG.args_2_status)
	# Check arg type
	if isinstance(ID, _Union[bool, int]):
		# It is bool or int, easy
		ret_value = int(ID)
	elif isinstance(ID, _put._Entry):
		# It is an enum
		#print(f"# TODO: put status instance, ID = {ID} // ID.id = {ID} -- this might not work properly")
		ret_value = ID.id
	else:
		raise TypeError(_MSG.args_status_first)
	#print(f"DEBUG ret_val: {ret_value}")
	# Checks passed, basic output
	_put._update()
	_put.border()
	# How to present main output?
	if len(args) == 0:
		# Nothing else passed,
		# so we have to make sure its all on the right
		if align_right:
			_put.text("", _put.status(ret_value), end=end)
		else:  # left
			_put.text(_put.status(ret_value),  "", end=end)
	else:
		if align_right:
			_put.text(*args, _put.status(ret_value), end=end)
		else:  # left
			_put.text(_put.status(ret_value), *args, end=end)
	# Do the dual output?
	if bDual:
		msg = args[0]
		message = msg % args[1:]
		return ret_value, message

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
		print(msg,f"{_stew.sec2time(cur)} / {Time}{unit}")
		cur -= 1
		## https://realpython.com/python-sleep/
		## Async? or time.wait instead ??
		_time.sleep(iIntervall)
	

def msgbox(*args, bOutside=False):
	"""
	Attempts to mimick a message box -> planned WIP
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

def clear():
	"""
	Clears the console screen and moves text cursors to top left corner.
	"""
	print(_stew.cat.clear)

def list(*args, bRoman=False, bMenu=False, sSeperator=")"):
	"""
	Prints a list 
	"""
	# Init / get vars
	max = _settings["inner"]
	cur = 0
	count = len(args)
	COL = None
	# Get longest item
	for item in args:
		_tmp_cur = len(item)
		if cur < _tmp_cur:
			cur = _tmp_cur
	# decide colum count
	if cur < max / 3:
		COL = 3
	elif cur < max / 2:
		COL = 2
	else:
		# Lets hope each item fits on a single line...
		COL = 1
	# Lets "Debug" here
	if COL is None:
		# No args detected:
		# TODO : Decide wether I want to abort here, or be error prone and just return nothing....
		raise ValueError(_MSG.args_missing , args)
	# cur is no longer used, lets reuse it
	# Also, prepare list to be shown
	if bMenu:
		# The menu entry is always on 0
		cur = 0
		list_entries = [ _MSG.tui_list_back , *args ]
	else:
		cur = 1
		list_entries = args
	#
	#	List Loop
	#
	#for entry in list_entries:
		# TODO
	entries_per_row = COL
	for i in range(0, count, entries_per_row):
		current_entries = list_entries[i:i + entries_per_row]
		formatted_entries = []
		for j, entry in enumerate(current_entries, start=cur):
			if bRoman:
				count = _stew.num2roman(j)
			else:
				count = str(j)
			formatted_entries.append(f"{count}{sSeperator} {entry}")
		print(*formatted_entries)

def pick(*args, bDual=False, bMenu=False):
	"""
	"""
	list(*args)
	return 0, "testing"


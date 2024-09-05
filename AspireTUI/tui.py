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
import platform as _platform
#import msvcrt as _msvcrt
#import shutil as _shutil
import subprocess as _subprocess
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
print_org = print	# Save original print
from . import _settings_console as _settings
from ._MESSAGES import current as _MSG
from . import Strings as _stew
from . import _internal
from . import _PrintUtils as _put
from ._PrintUtils import STATUS
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
	str_ret =  _put.status(_put.STATUS.Work.value)
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

def status(ID: _Union[int, bool, _put._Entry, STATUS], *args, align_right=True, end='\n', bDual=False):
	"""
	Requires ID to be int, bool, STATUS or _Entry, and 1 additional string as message for the status.

	By default (orientation=right), text is printed left, center, and the actual status on the right.

	Change orientation=left to have status on the left, main text on the right. If an optional text is passed,
	main text will be in the center and the optional text on the right.
	"""
	#
	#	Init
	#
	ret_status = None
	ret_value = None
	# Check arg count
	if len(args) > 2:
		raise SyntaxError(_MSG.args_2_status)
	# Check arg type
	if isinstance(ID, _Union[bool, int, _put._Entry]):
		# It is valid
		ret_value = ID
	elif isinstance(ID, STATUS):
		ret_value = ID.value
	else:
		# Invalid, most likely
		try:
			ret_value = ID._value_.id
			print(f"# TODO: tui status instance, ID = {ID} // ID.id = {ID._value_.id} // ret_value = {ret_value} this might not work properly")
		except TypeError:
			raise TypeError(_MSG.args_status_first)
	#
	# 	Checks passed, basic output
	#
	_put._update()
	_put.border()
	# Double check alignment:
	theme = _Theme.get()
	bInversedStatus = theme.bInversedStatus
	if bInversedStatus: align_right=False

	# How to present main output?
	if len(args) == 0:
		# Nothing else passed,
		# so we have to make sure its all on the right
		if align_right:
			_put.text("", _put.status(ret_value), end=end)
		else:  # left
			_put.text(_put.status(ret_value), end=end)
	else:
		if align_right:
			_put.text(*args, _put.status(ret_value), end=end)
		else:  # left
			if len(args) == 1:
				_put.text(f"{_put.status(ret_value)} {args[0]}", end=end)
			else:
				_put.text(_put.status(ret_value), *args, end=end)
	#
	#	Do the dual output?
	#
	if bDual:
		messasge = None
		try:
			msg = args[0]
			message = msg % args[1:]
		except TypeError:
			message = args
		return ret_value, message
	else:
		return ret_value

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
	if unit == "s":
		secs = Time
	elif unit == "m":
		secs = 60 * Time
	elif unit == "h":
		secs = 60 * 60 * Time
	
	
	# Prepare strings:
	if msg is None:
		msg = _MSG.tui_wait_continue_in
	
	cur = secs
	while cur > 0:
		print(msg,f"{_stew.sec2time(cur)} / {Time}{unit}", end="\r")
		cur -= 1
		## https://realpython.com/python-sleep/
		## Async? or time.wait instead ??
		_time.sleep(iIntervall)
	status(STATUS.Next.value, msg)
	

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

def list(*args, bRoman=False, bAlpha=False, bMenu=False, sSeperator=")"):
	"""
	Prints a list \n
	bMenu=True 		= Shows "Back" (translated) to user as option 0. \n
	bRoman=True 	= Use roman numbering instead of int values. \n
	bAlpha=True 	= Use letters for numbering. \n
	sSeperator="." 	= Use a custom numbering sperator... 1.
	"""
	# Init / get vars
	max_len = _settings["inner"]
	count_args = len(args)
	COL = None
	# decide column count
	if count_args < max_len / 3:
		COL = 3
	elif count_args < max_len / 2:
		COL = 2
	else:
		# Let's hope each item fits on a single line...
		COL = 1
	# Let's "Debug" here
	if COL is None:
		# No args detected:
		# TODO: Decide whether I want to abort here or be error-prone and just return nothing....
		raise ValueError(_MSG.args_missing, *args)
	# Also, prepare list to be shown
	if bMenu:
		# The menu entry is always on 0
		list_entries = [_MSG.tui_list_back, *args]
		visual_index_mod = 0
		count_args += 1
	else:
		list_entries = args
		visual_index_mod = 1
	#
	#	List Loop
	#
	entries_per_row = COL
	for i in range(0, count_args, entries_per_row):
		current_entries = list_entries[i:i + entries_per_row]
		formatted_entries = []
		for j, entry in enumerate(current_entries, start=i):
			if bRoman:
				entry_count = _stew.num2roman(j+visual_index_mod)
			elif bAlpha:
				entry_count = _stew.num2alpha(j+visual_index_mod)
			else:
				entry_count = str(j+visual_index_mod)
			formatted_entries.append(f"{entry_count}{sSeperator} {entry}")
		print(*formatted_entries, end="\n")

def pick(*args, text: str =_MSG.tui_pick_please_pick, bDual=False, bMenu=False, bVerbose=False) -> _Union[int, tuple[int, str]]:
	"""
	Prints passed 'args' as list and allows user to pick a choice

	Parameters:
	- text: 		Text so show instead of default text
	- bDual:		Returns 'selected_index' and 'list_item' 
	- bMenu:		Always show "Back" (translated) to user as first option (always: 0)
					When user selects 0 for "Back" (translated), it will return "Back" (hardcoded) as "list_item".
	- bTranslated:	Return translated "Back" as "list_item", requires bMenu=True. (only visual to user, coding is hardcoded english "back")
	- bVerbose:		Use 'tui.status' for "pick-feedback".

	Examples:
	- ret_index, ret_string = pick(*LIST, bDual=True)
	- index_picked = pick(*LIST)
	"""
	
	# init
	_theme = _Theme.get()
	
	# This many options
	_count = len(args)
	
	# Length of option count (character count or arg count : 12 args = 2 digits/chars)
	_len = len(str(_count))
	
	# Show options
	list(*args, bMenu=bMenu)
	print()
	
	# Show text ?
	text = f"{text} {_theme.prompt_select} "
	
	# Counting starts at
	if bMenu:
		range_min = 0
		list_entries = [_MSG.tui_list_back, *args]
	else:
		range_min = 1
		list_entries = args
	
	# Prepare user input
	index_input = None
	
	# Loop basic output until valid input is detected
	while True:
		# Print basic output
		_put.border()
		_put.text(text, end="")
		# TODO: 5 should become dynamic for any possile custom themes (but works perfectly with all default themes)
		_put._cursor2pos(len(text) + 5)

		# Read actual user input
		index_input = _internal.get_input_charcount(_len)

		# Make sure it is int (to work with)
		selected_index = int(index_input)
		
		# Zero is only allowed if Menu -> check range_min
		if selected_index >= range_min:
			# its valid min range
			if selected_index <= len(list_entries):
				# Its valid max range
				break
	
	# Prepare output
	if bMenu and selected_index == 0:
		str_ret = "Back"	# This must be hardcoded for easier/consistent coding
	else:
		str_ret = args[selected_index - 1]
	
	# How to show?
	if bVerbose:
		msg = f"{_MSG.word_picked}: {index_input} ({str_ret})"
		if str_ret == "Back":
			status(_put.STATUS.Prev.value , msg)
		else:
			status(True, msg)
	else:
		print(text, f"{index_input} ({str_ret})")
	
	# Return the result based on bDual
	if bDual:
		return selected_index, str_ret
	else:
		return selected_index

def open(filename: str=None): #, doWait: bool=False):
	"""
	Opens passed 'filename' with default application.
	"""
	#doWait: \tWIP - Waits until task is closed.
	#"""

	# Determine the operating system
	current_os = _platform.system()

	if current_os == "Windows":
		# Windows
		_os.startfile(filename)
	elif current_os == "Darwin":
		# macOS
		_subprocess.call(["open", filename])
	else:
		# Linux and other Unix-like systems
		#import OS as _OS
		DESKTOP = _platform.freedesktop_os_release
		if DESKTOP == "Wayland":
			status(STATUS.Todo.value, f"TODO: Handling for {DESKTOP}")
			_subprocess.call(["xdg-open", filename])
		else:
			_subprocess.call(["xdg-open", filename])

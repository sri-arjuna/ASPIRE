"""
Created on:		2023 Nov. 09
Created by:		Simon Arjuna Erat
License:		MIT
URL:			https://www.github.com/sri-arjuna/ASPIRE
PyPi:			https://pypi.org/project/AspireTUI/
Based on my TUI & SWARM for the BASH shell © 2011
"""
################################################################################################################
#####                                            Shared Imports                                            #####
################################################################################################################
#
#	Essential imports
#
import os as _os
import sys as _sys

#
#	Set True during local testing
#	Only commit with False
#
if False: _sys.dont_write_bytecode = True

#
#	Simplify language access
#
from ._MESSAGES import current as _MSG 			# This is not used here, but eases the import
################################################################################################################
#####                                            One time constants                                        #####
################################################################################################################
#
#	Simplify OS access
#	Get OS specific FileDescriptor (if possible, seperate output for the TUI)
#
if _os.name == 'nt':
	# Basicly, detect if OS is Windows based
	IS_WINDOWS=True
	# Windows does need the terminal to be... "initialized"... by this for the colors to work.
	# No, subprocess.popen("", shell=True) does not work.
	_os.system("")
	# Windows does not support custom FileDescriptors
	FD_BORDER=_sys.stderr
else:
	# Or *nix based
	IS_WINDOWS=False
	# *nix based Systems on the other hand, do support FIFO FD's
	FD_BORDER=_os.fdopen(_os.dup(_sys.stderr.fileno()), 'w')
################################################################################################################
#####                                            Default Values                                            #####
################################################################################################################
#
#	Set default settings:
#
_settings_console = {
	"full": 		120,
	"inner": 		112,
	"lang":			"english",
	"theme":		"Default",
	"theme_color":	None,
	"theme_style":	None,
	"due":			12,
}

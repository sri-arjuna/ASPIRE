"""
Created on:		2023 Nov. 09
Created by:		Simon Arjuna Erat
License:		MIT
URL:			https://www.github.com/sri-arjuna/ASPIRE
PyPi:			
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
#	Simplify language access
#
from AspireTUI.__core._MESSAGES import current as _MSG 			# This is not used here, but eases the import

################################################################################################################
#####                                            One time constants                                        #####
################################################################################################################
#
#	Simplify OS access
#
if _os.name == 'nt':
	# Basicly, detect if OS is Windows based
	IS_WINDOWS=True
else:
	# Or *nix based
	IS_WINDOWS=False
#
#	Get OS specific FileDescriptor (if possible, seperate output for the TUI)
#
if IS_WINDOWS:
	# Windows does need the terminal to be... "initialized"... by this for the colors to work.
	# No, subprocess.popen("", shell=True) does not work.
	_os.system("")
	# Windows does not support custom FileDescriptors
	FD_BORDER=_sys.stderr
else:
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
	"lang":			"en",
	"theme":		"Default",
	"due":			0,
}
_settings_self = {
	"isDEBUG":		True,
	"log_file":		"AspireTUI.log",
	"log_conf":		"AspireTUI-log.ini"
}
################################################################################################################
#####                                            Initialize & Update                                       #####
################################################################################################################
def _log(doLog: bool, ):
	"""
	Handles internal logging / verbose'ity according to _settings
	"""
	if _settings["log_self"] == True:
		# Let 
		# Prepare work
		from .Classes import Conf as _Conf
		# Check if log-conf exists
		_check_log_conf =_settings["log_conf"]
		_check_log = _settings["log_file"]

		_conf = _Conf()

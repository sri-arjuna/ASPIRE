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
#	Simplify language access
#
from .__core._MESSAGES import current as _MSG 			# This is not used here, but eases the import
from .__core._PrintUtils import _update
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
	"lang":			"english",
	"theme":		"Default",
	"due":			0,
}
_settings_self = {
	"isDEBUG":		True,
	"conf_file":	"AspireTUI.ini",
	"log_file":		"AspireTUI.log",
	"log_conf":		"AspireTUI-log.ini"
}
_update()
################################################################################################################
#####                                            Initialize & Update                                       #####
################################################################################################################
"""
def _fLog(doLog: bool, ):
	""
	# Handles internal logging / verbose'ity according to _settings
	""
	if _settings_self["log_self"] == True:
		# Let 
		# Prepare work
		from .Classes import Conf as _Conf
		# Check if log-conf exists
		_check_log_conf =_settings_self["log_conf"]
		_check_log = _settings_self["log_file"]
		_check_conf = _settings_self["conf_file"]

		_conf = _Conf(_check_conf, LOGFILE=_check_log_conf)
		#_conf.settings.LOGFILE

#from AspireTUI.__core import _log
from .strings import now as _now
from .Classes import _Log
from . import _settings_self
log = _Log.Log( _settings_self["log_conf"] )
log.settings.Title = f"Created with: AspireTUI (TODO VER), {_now()}"
# For debugging purposes this extreme
if True == _settings_self["isDEBUG"]:
	log.settings.LogLevel_ShowUser = 0
	log.settings.LogLevel_SaveLog = 0
log.DEBUG(f"Logging Enabled: {_os.path.abspath(_os.path.curdir)} // {log.settings.filename}")
log.INFO(f"Yay! Another log entry! -- %r -- %s", "Just here", "for testing!")

"""

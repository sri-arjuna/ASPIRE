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
################################################################################################################
#####                                            One time constants                                        #####
################################################################################################################
#
#	Simplify OS access
#
if os.name == 'nt':
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
	os.system("")
	# Windows does not support custom FileDescriptors
	FD_BORDER=sys.stderr
else:
	# *nix based Systems on the other hand, do support FD's
	FD_BORDER=os.fdopen(os.dup(sys.stderr.fileno()), 'w')
################################################################################################################
#####                                            Default Values                                            #####
################################################################################################################
#
#	Set default settings:
#
settings = {
    "full": 		120,
	"inner": 		112,
	"lang":			"en",
	"theme":		"Default",
	"due":			0
}
################################################################################################################
#####                                            Initialize & Update                                       #####
################################################################################################################


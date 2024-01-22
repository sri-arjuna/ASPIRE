"""
	Description:
					Provides all the translated default MESSAGES, basicly all text output.
	Provides:
					from AspireTUI import MESSAGES as MSG
					tui.status(False, MSG.file_not_found)
					
	========================================================
	Created on:		2023 Dec. 26
	Created by:		Simon Arjuna Erat
	License:		MIT
	URL:			https://www.github.com/sri-arjuna/ASPIRE

	Based on my TUI & SWARM for the BASH shell © 2011
"""
#
#	Prepare for multi language support
#
import gettext as _gettext
from gettext import gettext as _

from pathlib import Path as _Path
# Lang setup
translation_directory = _Path("locales")
translation = _gettext.translation("AspireTUI", translation_directory, fallback=True)
translation.install()
################################################################################################################
#####                                            Words                                                     #####
################################################################################################################
#
#
#
word_error 			= _("Error")
word_fatal			= _("Fatal")
word_name			= _("Name")
word_working		= _("Working")
word_found 			= _("Found")
word_picked			= _("Picked")
#
#	FileSystem
#
word_filesystem_dir = _("Directory")
word_filesystem_file =_("File")
word_filesystem_link =_("Link")
word_filesystem_mount =_("Mount")


################################################################################################################
#####                                            Status                                                    #####
################################################################################################################
#from AspireTUI.lists import StatusEnum # as StatusEnum
status_done			= _("DONE")
status_fail			= _("FAIL")
status_todo			= _("TODO")
status_work			= _("WORK")
status_skip			= _("SKIP")
status_next			= _("NEXT")
status_prev			= _("PREV")
status_info			= _("INFO")
status_on			= _(" ON ")
status_off			= _("Off ")
status_			= _("")

################################################################################################################
#####                                            FileSystem                                                #####
################################################################################################################



################################################################################################################
#####                                            Errors                                                    #####
################################################################################################################
err_PERM_word		= _("Permission")
err_PERM_word_short = _("PERM")
err_PERM_sentence	= _("No permission in/for:")
err_ERROR_word		= _("Error")
err_ERROR_word_short = _("ERR ")
err_ERROR_sentence	= _("An error occoured.")
err_WARN_word		= _("Warning")
err_WARN_word_short = _("WARN")
err_WARN_sentence	= _("")
err_CRIT_word		= _("Critical")
err_CRIT_word_short = _("CRIT")
err_CRIT_sentence	= _("")
err_FATAL_word		= _("Fatal")
err_FATAL_word_short = _("FATL")
err_FATAL_sentence	= _("")

err__word		= _("")
err__word_short = _("")
err__sentence	= _("")

err__word		= _("")
err__word_short = _("")
err__sentence	= _("")

################################################################################################################
#####                                            Database                                                  #####
################################################################################################################




################################################################################################################
#####                                            Internal Values                                           #####
################################################################################################################
args_too_many 		= _("Too many arguments!")
args_2_status		= _("Too many arguments, max 2 strings allowed after ID (int/bool)!")
args_status_first	= _("The first argument to 'status' must be INT or BOOL.")
args_max3 			= _("Too many arguments, max 3 allowed!")
args_missing 		= _("Missing arguments!")
args_title			= _("Title accepts only 1 string argument!")

################################################################################################################
#####                                            Files and Folders                                         #####
################################################################################################################
file_not_found 		= _("File/Directory not found.")
file_exists 		= _("File/Directory exists.")
dir_not_found 		= _("Directory not found.")

################################################################################################################
#####                                            Files and Folders                                         #####
################################################################################################################
os_not_found_python	= _("Could not detect python, weird...")

################################################################################################################
#####                                            Database                                                  #####
################################################################################################################
registry_hkey		= _("Invalid or missing HKEY")
registry_success	= _("Successfully changed variable to value.")

################################################################################################################
#####                                            Theme                                                     #####
################################################################################################################
theme_none 			= _("You have not provided a proper theme.")
theme_cant_read 	= _("Cant read theme.")
theme_empty_var 	= _("The provided theme contains empty variables and can not be used!")
theme_color_invalid	= _("Cant read color code, please use plain text, not console code.")

################################################################################################################
#####                                            List                                                      #####
################################################################################################################
tui_list_back		= _("Back")


################################################################################################################
#####                                            TUI                                                       #####
################################################################################################################
tui_press			= _("Press any key to continue.")
tui_progress_bar	= _("Wrong style for progress, only 'bar' and 'num' are supported.")
tui_style_invalid	= _("Invalid style argument. Expected 'print', 'header', or 'title'. // passed:")
tui_wait_continue_in = _("Continue in:")
tui_yesno_bDual_missing_msg = _("When bDual is enabled, you must provided both, 'msg_yes' and 'msg_no'!")
tui_pick_please_pick	= _("Please pick")
################################################################################################################
#####                                            Class Log                                                 #####
################################################################################################################
cl_log_severity0	= _("DEBUG")
cl_log_severity1	= _("INFO")
cl_log_severity2	= _("WARNING")
cl_log_severity3	= _("ERROR")
cl_log_severity4	= _("CRITICAL")
cl_log_severity5	= _("FATAL")
#
#	Severity
#
_SEVERITY_TRANSLATED = [
	cl_log_severity0,
	cl_log_severity1,
	cl_log_severity2,
	cl_log_severity3,
	cl_log_severity4,
	cl_log_severity5
]
#
# 	More Strings
#
cl_log_fatal_no_file 			= _("No file provided, can not create class!")
cl_log_warn_file_without_path	= _("Logfile does not contain any path information.\nThis could lead to unexpected behaviour")
cl_log_err_must_bool		= _("Provided argument must be: bool")
cl_log_err_must_float		= _("Provided argument must be: float")
cl_log_err_must_list		= _("Provided argument must be: list")
cl_log_err_must_int			= _("Provided argument must be: int")
cl_log_err_must_str			= _("Provided argument must be: str")

################################################################################################################
#####                                            Class Conf                                                #####
################################################################################################################
cl_conf_ui_saving			= _("Saving")
cl_conf_ui_saved			= _("Saved")
cl_conf_ui_reading			= _("Reading")
cl_conf_ui_read				= _("Read")
cl_conf_				= _("")
cl_conf_				= _("")
cl_conf_				= _("")

cl_conf_				= _("")
#tui_press			= _("")

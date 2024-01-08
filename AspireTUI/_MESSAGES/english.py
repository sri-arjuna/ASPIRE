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
#####                                            Database                                                  #####
################################################################################################################
word_error 			= _("Error")
word_fatal			= _("Fatal")
word_name			= _("Name")
word_working		= _("Working")



################################################################################################################
#####                                            Internal Values                                           #####
################################################################################################################
args_too_many 		= _("Too many arguments!")
args_2_status		= _("Too many arguments, max 2 strings allowed after ID (int/bool)!")
args_status_first	= _("The first argument to 'status' must be INT or BOOL.")
args_max3 			= _("Too many arguments, max 3 allowed!")
args_missing 		= _("Missing arguments!")


################################################################################################################
#####                                            Files and Folders                                         #####
################################################################################################################
file_not_found 		= _("File/Directory not found.")
file_exists 		= _("File/Directory exists.")
dir_not_found 		= _("Directory not found.")

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
################################################################################################################
#####                                            Class Log                                                 #####
################################################################################################################
cl_log_severity0	= _("DEBUG")
cl_log_severity1	= _("INFO")
cl_log_severity2	= _("WARNING")
cl_log_severity3	= _("ERROR")
cl_log_severity4	= _("CRITICAL")
cl_log_severity5	= _("FATAL")
cl_log_fatal_no_file 			= _("No file provided, can not create class!")
cl_log_warn_file_without_path	= _("Logfile does not contain any path information.\nThis could lead to unexpected behaviour")
cl_log_err_must_bool		= _("Provided argument must be: bool")
cl_log_err_must_float		= _("Provided argument must be: float")
cl_log_err_must_int			= _("Provided argument must be: int")
cl_log_err_must_str			= _("Provided argument must be: str")



#tui_press			= _("")

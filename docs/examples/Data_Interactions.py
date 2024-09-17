"""
	Created on:		2023.July.02
	Created by:		Simon Arjuna Erat
	License:		MIT
	URL:			https://www.github.com/sri-arjuna/ASPIRE
"""
#
# 	Imports
#
from AspireTUI import tui
from AspireTUI._PrintUtils import STATUS


tui.header("Simple Data Presentation")

#
#   tui.progress
#
tui.title("Progress Bar")
tui.progress("Shows a bar: 1/10", 0.1, 1)   ; print()   # progress would go on new line automaticly on "max" aka 1/1
tui.progress("Shows a bar: 1/3", 1, 3)      ; print()   # progress would go on new line automaticly on "max" aka 3/3
tui.progress("Shows a bar: 1/2", 1, 2)      ; print()   # progress would go on new line automaticly on "max" aka 2/2

#
#   tui.yesno
#
tui.title("User Interactions")
yesno = tui.yesno("Are you happy?")
if yesno:
    tui.status(STATUS.Done, "Yes you are")
else:
    tui.status(STATUS.Fail,  "No, you are not happy.")
tui.print()

#
#   tui.status
#
tui.title("Does also work with base bool / and + INT ")
tui.status(yesno, "Bool result")
tui.status(10 + int(yesno), "Int result: On/Off = 10+Bool")
tui.print()

#
#   tui.status, again
#
tui.title("Call by Enum")
for es in STATUS:
    tui.status(es, f"tui.status({es}, 'Message to user')")

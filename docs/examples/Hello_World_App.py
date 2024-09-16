"""
	Created on:		2023.July.02
	Created by:		Simon Arjuna Erat
	License:		MIT
	URL:			https://www.github.com/sri-arjuna/ASPIRE
"""
#
# 	Imports
#
from AspireTUI.Classes import AppManager
from AspireTUI import Strings as stew

#
# 	Init HelloWorld as HW
#
# This ill create a config file and logfile named: HelloWorld.{cfg|log} and use the Elegance theme as default.
HW = AppManager("HelloWorldApp", theme="Elegance", iSaveLog=0)


# Basic "Hello World"
HW.tui.header("ASPIRE by (sea/sri-arjuna)", f"{stew.now()}")
HW.tui.title("Hello World")
HW.tui.print("Left String", "Center String", "Right String")
HW.tui.print()

HW.tui.title("Lets see some error level for the log")
HW.DEBUG("Debug Level -> 0")
HW.INFO("Info level -> 1")
HW.WARNING("Warning level -> 2")
HW.ERROR("Error Level -> 3")
HW.FATAL("Fatal Level -> 4")
HW.CRITICAL("Critical Level -> 5")
HW.tui.print()

HW.tui.title("Lets work with the config file")
val = HW.get_custom("Theme", "THEME")
HW.tui.print("Current theme is:", val)
newTheme = "Default"
ret_set = HW.set_custom("Theme", "THEME", newTheme, bVerbose=True)
HW.save()

HW.tui.status(ret_set, f"Changed theme to: {newTheme}, applied on next start")
# And exit
HW.tui.wait(3,"Wait for it...")
HW.tui.print()
HW.tui.press()

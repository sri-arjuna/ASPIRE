"""
This is just a very basic example program so you're able to "get the drift".
"""
#
#	Imports
#
from AspireTUI import tui
from AspireTUI import Strings as stew
# Not used yet
from AspireTUI.Strings import cat
from AspireTUI import OS
#
#	Variables
#
mnu_status = "Show different Status"
mnu_conf = "Test: Configurations"
mnu_log = "Test: Log"
mnu_endless = "Menu - Endless Mania"
# Make it a list
MENU = [
	mnu_status,
	mnu_conf,
	mnu_log,
	mnu_endless
]
#
#	Functions
#
def test_configuration():
	"""
	Sample usage of the conf class
	"""
	tui.title("Test with configuration files")
	# TODO

def test_log():
	"""
	Sample usage of the log class
	"""
	tui.title("Test with log files")
	# TODO

def show_status():
	"""
	Sample usage of the status function
	"""
	tui.title("Show Status")
	for item in tui._put.STATUS:
		tui.status(item.value, item.name)
	tui.print()
	tui.status(True, "You've successfully seen the status variations!")
	tui.status(tui._put.STATUS.Todo.value, "TODO: Fix UNI coded and/or add 'gui' attribute to STATUS_STRINGS")

def menu_endless():
	"""
	Loops endlessly through a menu without doing anything, other than "Back".
	"""
	c = 0
	while True:
		c += 1
		tui.title(f"Endless Mania: {c}")
		id, msg = None, None
		id, msg =  tui.pick(*MENU, bMenu=True, bDual=True)
		if id == 0:
			# With bMenu = True, id 0 is always "Back"
			break
		else:
			# Handle menu
			tui.print()
			tui.status(2, f"Selected id({id}):", msg)
	
	tui.print()
	tui.status(True, "Gratulations, you've escaped the endless mania!")

def main():
	"""
	Main loop function
	"""
	msg = ""
	while True:
		#
		#	Default output for menu
		#
		tui.clear()
		tui.header(" AspireTUI - DEMO ", f" {stew.now()} ")
		tui.title("Lets get started")
		tui.print("Some regular text, could be longer or shorter, but of course either way would be handled. I mean, I'm providing a good quality service, swiss standards apply!")
		#
		#	Main menu
		#
		index, msg = tui.pick(*MENU, bDual=True, bVerbose=True, bMenu=True)
		#
		#	Work with returned values
		#
		if msg == "Back":
			break
		elif msg == mnu_status:
			show_status()
		elif msg == MENU[1]:
			test_configuration()
		elif msg == "Test: Log":
			test_log()
		elif msg == mnu_endless:
			menu_endless()
		tui.press()

#
#	Start Loop
#
main()

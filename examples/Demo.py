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
# Make it a list
MENU = [
	mnu_status,
	mnu_conf,
	mnu_log
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
		tui.press()
#
#	Start Loop
#
main()

"""
	Created on:		2024.September.16
	Created by:		Simon Arjuna Erat
	License:		MIT
	URL:			https://www.github.com/sri-arjuna/ASPIRE
"""
#
# 	Imports
#
from AspireTUI import tui

#
#	Variables
#
str_Header = " Demo for Menu "
created_on = "2024.September.16"
str_Title = "Pick your menu"

# Pseudo menu entries
lst_menu = [
	"Entry A",
	"Entry B",
	"Entry C",
	"Entry D",
]

#
#	Main Loop
#
tui.header(str_Header, created_on)
while True:
	#
	# Actual Menu
	#
	tui.title(str_Title)

	# You can set bMenu to false (or just remove it) if you dont want to "go back"
	action_id, action_str = tui.pick( *lst_menu, bMenu=True, bVerbose=True, bDual=True )

	# Do action based on pick
	if action_id == 0:
		# Back Exit / is always 0
		break

	elif action_id == 1:
		# This is how you would do things
		tui.title( action_str)
		tui.print("Stuff in A")
		tui.print()

	else:
		# Lazy approach for the menu demo
		# You could also check for the "action_str" instead of the "action_id"
		tui.title( action_str)
		tui.print("Selected id:", action_id)
		tui.print("Selected str:", action_str)
		tui.print()

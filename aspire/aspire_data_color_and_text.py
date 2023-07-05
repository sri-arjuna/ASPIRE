"""
	Created on:		2023.July.02
	Created by:		Simon Arjuna Erat
	License:		MIT
	URL:			https://www.github.com/sri-arjuna/ASPIRE
"""


# Imports
from collections import namedtuple


# Top level container
CaT = namedtuple('CaT', ['colors', 'text', 'line' , 'codes', 'reset'])

# Name grouping for colors
ColorGroup = namedtuple('ColorContainer', ['front', 'back'])

# Name 'list' for both: front and back
ColorList = namedtuple('Color', ['black', 'red', 'green', 'yellow', 'blue', 'magenta', 'cyan', 'light_gray',
                                'dark_gray', 'light_red', 'light_green', 'light_yellow', 'light_blue', 
                                'light_magenta', 'light_cyan', 'white'])

# Container for text
Text = namedtuple('Text', ['bold', 'italic', 'underline'])

# Container for line
Line = namedtuple('Line', ['up', 'down'])

# Container for various codes
Codes = namedtuple('Codes', ['beep', 'blink', 'invert'])

################################################################################################################
#####                                              Data Structures                                         #####
################################################################################################################
cat = CaT(
    reset='\033[0m',
    # This might be expaned in the future with more codes.
    codes = Codes(
        beep='\a',
        blink='blink',
        invert='invert',
    ),
    # Group color access
	colors = ColorGroup(
        front = ColorList(
            black='\033[30m',
            red='\033[31m',
            green='\033[32m',
            yellow='\033[33m',
            blue='\033[34m',
            magenta='\033[35m',
            cyan='\033[36m',
            light_gray='\033[37m',
            dark_gray='\033[90m',
            light_red='\033[91m',
            light_green='\033[92m',
            light_yellow='\033[93m',
            light_blue='\033[94m',
            light_magenta='\033[95m',
            light_cyan='\033[96m',
            white='\033[97m',
		),
        back = ColorList(
            black= '\033[40m',
            red= '\033[41m',
            green= '\033[42m',
            yellow= '\033[43m',
            blue= '\033[44m',
            magenta= '\033[45m',
            cyan= '\033[46m',
            light_gray= '\033[47m',
            dark_gray= '\033[100m',
            light_red= '\033[101m',
            light_green= '\033[102m',
            light_yellow= '\033[103m',
            light_blue= '\033[104m',
            light_magenta= '\033[105m',
            light_cyan= '\033[106m',
            white= '\033[107m',
            ),
		),
    # only 3 text attributes are known on console
    text = Text(
        bold='\033[1m',
        italic= '\033[3m',
        underline='\033[4m',
	),
    # Maybe expanded later
    line = Line(
        up='\033[1A',
        down='\033[1B',
	)        
)
"""
	Description:
			Contains various dicts, lists and enums
	Usage:
			from AspireTUI import Lists as _Lists

	========================================================
	Created on:		2024 Jan. 08
	Created by:		Simon Arjuna Erat
	License:		MIT
	URL:			https://www.github.com/sri-arjuna/ASPIRE

	Based on my TUI & SWARM for the BASH shell © 2011
"""
################################################################################################################
#####                                            Imports                                                   #####
################################################################################################################
#
#	Prepare data structures
#
from enum import Enum as _Enum
from dataclasses import dataclass as _dataclass
from AspireTUI.__core.ColorAndText import cat as _cat
#################################################################################################################
#####                                           Class: LOG & Status                                         #####
#################################################################################################################
class LOG_LEVEL(_Enum):
	DEBUG = 0,
	INFO = 1,
	WARNING = 2,
	ERROR = 3,
	CRITICAL = 4,
	FATAL = 5

LOG_SEVERITY = []
LOG_SEVERITY[0] = "DEBUG"
LOG_SEVERITY[1] = "INFO"
LOG_SEVERITY[2] = "WARNING"
LOG_SEVERITY[3] = "ERROR"
LOG_SEVERITY[4] = "CRITICAL"
LOG_SEVERITY[5] = "FATAL"
#
#	Status
#
class StatusEnum(_Enum):
	# Default: bool
	class Fail(_Enum):
		id = False
		string = f"{_cat.front.red}{_cat.text.bold} X {_cat.reset}"
	class Done(_Enum):
		id = True
		string = f"{_cat.front.green}{_cat.text.bold} √ {_cat.reset}"
	# Log Level
	class DEBUG(_Enum):
		id = 1000 + LOG_LEVEL.DEBUG
		string = f" 🐞 "
	class INFO(_Enum):
		id = 1000 + LOG_LEVEL.INFO 
		string = f"ℹ️ℹ️ℹ️"
	class Warning(_Enum):
		id = 1000 + LOG_LEVEL.WARNING
		string = f" ⚠️ "
	class ERROR(_Enum):
		id = 1000 + LOG_LEVEL.ERROR
		string = f" ❌ "
	class CRITICAL(_Enum):
		id = 1000 + LOG_LEVEL.CRITICAL
		string = f" 🔴 "
	class FATAL(_Enum):
		id = 1000 + LOG_LEVEL.FATAL
		string = f" ☠️ "
	# Default: Pseudo-Bool
	class Off(_Enum):
		id = int(False) + 10
		string = f"{_cat.front.red}{_cat.text.bold} ○ {_cat.reset}"
	class On(_Enum):
		id = int(True) + 10
		string = f"{_cat.front.green}{_cat.text.bold} ● {_cat.reset}"
	# Job related
	class Todo(_Enum):
		id = 2
		string = f"{_cat.front.cyan}{_cat.text.bold} ≡ {_cat.reset}"
	class Work(_Enum):
		id = 3
		string = f"{_cat.front.yellow}{_cat.text.bold} ∞ {_cat.reset}"
	# Menu
	class Skip(_Enum):
		id = 4
		string = f""
	class Next(_Enum):
		id = 5
		string = f""
	class Prev(_Enum):
		id = 6
		string = f""
	class Info(_Enum):
		id = 111
		string = f""
#STATUS_WORDS = []

#################################################################################################################
#####                                           Lib: StringUtils                                            #####
#################################################################################################################
roman_roman2num = {
		'I': 1, 'V': 5, 'X': 10, 'L': 50,
		'C': 100, 'D': 500, 
		'M': 1000, 'V̅': 5000, 
		'X̅': 10000, 'L̅': 50000, 
		'C̅': 100000
	}

roman_num2roman = {
		10000: 'X̅', 9000: 'IX̅', 5000: 'V̅', 4000: 'IV̅',
		1000: 'M', 900: 'CM', 500: 'D', 400: 'CD',
		100: 'C', 90: 'XC', 50: 'L', 40: 'XL',
		10: 'X', 9: 'IX', 5: 'V', 4: 'IV',
		1: 'I'
	}

morse_code = {
    'A': '.-', 'B': '-...',
    'C': '-.-.', 'D': '-..', 'E': '.',
    'F': '..-.', 'G': '--.', 'H': '....',
    'I': '..', 'J': '.---', 'K': '-.-',
    'L': '.-..', 'M': '--', 'N': '-.',
    'O': '---', 'P': '.--.', 'Q': '--.-',
    'R': '.-.', 'S': '...', 'T': '-',
    'U': '..-', 'V': '...-', 'W': '.--',
    'X': '-..-', 'Y': '-.--', 'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---',
    '3': '...--', '4': '....-', '5': '.....',
    '6': '-....', '7': '--...', '8': '---..',
    '9': '----.',
    '.': '.-.-.-', ',': '--..--', '?': '..--..',
    "'": '.----.', '!': '-.-.--', '/': '-..-.',
    '(': '-.--.', ')': '-.--.-', '&': '.-...',
    ':': '---...', ';': '-.-.-.', '=': '-...-',
    '+': '.-.-.', '-': '-....-', '_': '..--.-',
    '"': '.-..-.', '$': '...-..-', '@': '.--.-.',
    ' ': '/'
}

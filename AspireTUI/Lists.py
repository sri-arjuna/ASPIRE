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
#from dataclasses import dataclass as _dataclass
#from AspireTUI.__core.ColorAndText import cat
#################################################################################################################
#####                                           Class: LOG & Status                                         #####
#################################################################################################################
#from AspireTUI.__core._PrintUtils import STATUS
class LOG_LEVEL(_Enum):
	DEBUG = 0
	INFO = 1
	WARNING = 2
	ERROR = 3
	CRITICAL = 4
	FATAL = 5

LOG_SEVERITY = [ 
	"DEBUG" , 
	"INFO", 
	"WARNING", 
	"ERROR", 
	"CRITICAL", 
	"FATAL" 
]
#
#	Status
#

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

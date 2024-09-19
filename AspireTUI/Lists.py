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

encodings = [
    'utf-8',        # UTF-8 (most common and default encoding in Python)
    'utf-16',       # UTF-16 encoding
    'utf-32',       # UTF-32 encoding
    'ascii',        # ASCII encoding (7-bit)
    'latin-1',      # Latin-1 (ISO-8859-1)
    'iso-8859-1',   # Another name for Latin-1
    'iso-8859-2',   # ISO Latin-2 (Central and Eastern European languages)
    'iso-8859-3',   # ISO Latin-3 (South European and miscellaneous languages)
    'iso-8859-4',   # ISO Latin-4 (North European languages)
    'iso-8859-5',   # ISO Latin/Cyrillic alphabet
    'iso-8859-6',   # ISO Latin/Arabic alphabet
    'iso-8859-7',   # ISO Latin/Greek alphabet
    'iso-8859-8',   # ISO Latin/Hebrew alphabet
    'iso-8859-9',   # ISO Latin-5 (Turkish)
    'iso-8859-10',  # ISO Latin-6 (Nordic languages)
    'windows-1250', # Windows Central and Eastern European
    'windows-1251', # Windows Cyrillic
    'windows-1252', # Windows Latin-1 (Western European)
    'windows-1253', # Windows Greek
    'windows-1254', # Windows Turkish
    'windows-1255', # Windows Hebrew
    'windows-1256', # Windows Arabic
    'windows-1257', # Windows Baltic
    'windows-1258', # Windows Vietnamese
    'cp437',        # DOS Latin US (Code Page 437)
    'cp850',        # DOS Western European (Code Page 850)
    'cp852',        # DOS Central European (Code Page 852)
    'cp866',        # DOS Cyrillic (Code Page 866)
    'shift_jis',    # Shift JIS (Japanese)
    'euc-jp',       # Extended Unix Code (Japanese)
    'gb2312',       # Simplified Chinese (Mainland China)
    'big5',         # Traditional Chinese (Taiwan, Hong Kong)
    'koi8-r',       # KOI8-R (Cyrillic script)
    'koi8-u',       # KOI8-U (Ukrainian)
    'mac-roman',    # Macintosh Roman
    'mac-cyrillic', # Macintosh Cyrillic
    'cp037',        # IBM EBCDIC US/Canada
    'cp500',        # IBM EBCDIC International
]


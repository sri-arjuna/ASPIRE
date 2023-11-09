# Default Header
"""
	Created on:		2023.July.06
	Created by:		Simon Arjuna Erat
	License:		MIT
	URL:			https://www.github.com/sri-arjuna/ASPIRE
"""

# Description
"""
	Just a basic Error handling fucntionality
	
"""



from enum import Enum


class AspireErrorEnum(Enum):
	THEME_NONE 			= "You have not provided a proper themre.",
	THEME_CANT_READ 	= "Cant read theme.",
	THEME_EMPTY_VAR		= "The provided theme contains empty variables and can not be used!",
	COLOR_CANT_READ		= "Cant read color code, please use plain text, not console code.",
	PRINT_COUNT			= "You can only pass up to 3 strings as argument.",
	STATUS_ID			= "The first argument to 'status' must be INT."
	STATUS_COUNT		= "You can only pass 2 string arguments to 'status' (= 3 with id)."



def ErrMsg(id: AspireErrorEnum) -> str:
	str_type = "Fatal"
	print(str_type + "\n" + id)
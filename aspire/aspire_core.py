# Basic header:
"""
	Created on:		2023.July.02
	Created by:		Simon Arjuna Erat
	License:		MIT
	URL:			https://www.github.com/sri-arjuna/ASPIRE
"""


# General information for possible contributors
"""
PEP8:
    Lines:
        While 80 is the official chars per line limiter, this projects uses a limit of 90'ish.
        Furthermore, this projects uses tabs: 4, and should enforce a hard warped linebreak at 120.
    
    Camel_And_Snake_Cases:
        * PEPE8 > uncertain
        * Convenience > PEP8
        * Logic > convenience
        
Internal / Public:
    * Leading spaces:
        1.  One means: 
            While designed for internal use only, they might be of help to non-contributing authors as well

        2.  Two means:
            This really should only be used internaly (contributors)

        3.  Three means:
            These are designed to improve internal performance and should never be changed or accessed by others!
    * Aliases:
        * should be 2-4 chars long
        * should aim for humoristic interpreted abreviations
            * ac = Aspire Core
            * cat = Color And Text codes    (catc = cat)
            * put = Print UTilities         (pu = put)
            * stew = STring Utilities       (stu = stew)
"""


# Essential imports
import os
import platform
import re
import shutil
import sys

# Prepare data structures
from collections import namedtuple
from dataclasses import dataclass
from enum import Enum

# Import internal tools
from .aspire_data_color_and_text import cat
from .aspire_data_themes import ThemeAttributes
from .aspire_data_themes import ThemesList


################################################################################################################
#####                                              Top Class / Definitions                                 #####
################################################################################################################
class AspireCore:
    _console_width = None
    _is_Windows = None
    _border_fd = None
    
    def __init__(self):
        self._is_Windows = self.__is_Windows()
        self._border_fd = self._create_custom_fd()
        self._console_width = self._get_terminal_width()
        print("DEBUG : " + self._console_width)

	
    @classmethod
    def __is_Windows(cls):
        # Checks class attribute, if empty assign a bool to it
        if cls.__is_Windows is None:
            if os.name == 'nt':  # Windows
                cls.__is_Windows = True
            else:  # Unix-like
                cls.__is_Windows = False
        return cls.__is_Windows
    
    @classmethod
    def _create_custom_fd(cls):
        # This aims to create a FileDescriptor to display the borders
        # so stdout for text, and stderr is used for errors.
        if cls.__is_Windows:
            # Does not support custom FileDescriptors
            return sys.stderr
        else:
            # *nix based Systems on the other hand, do support FD's
            return os.fdopen(os.dup(sys.stderr.fileno()), 'w')
    
    @staticmethod
    def _get_terminal_width() -> int:
        terminal_size = shutil.get_terminal_size((80, 20))  # Default size if terminal size cannot be determined
        return int(terminal_size.columns)
    
    



#################################################################################################################
#####                                           Theme Stuff                                                 #####
#################################################################################################################
class Theme:
    def __init__(cls):
        cls._selected = cls.get()
    
    available_themes = {
        'Default': ThemesList.Default,
        'Classic': ThemesList.Classic,
        'Float': ThemesList.Float,
        'Mono': ThemesList.Mono,
    }
    _default = 	"Default"
    _selected = None

    @staticmethod
    def _check_empty_variables(theme):
        empty_variables = []
        var_skip = ["border_left", "border_right", "filler", ]
        for variable_name, variable_value in theme.__dict__.items():
            if variable_name not in var_skip and variable_value == "":
                empty_variables.append(variable_name)
        return empty_variables

    @staticmethod
    def _get_color_code(foreground=None, background=None):
        # TODO FIX: for some reason it may happen that console codes are passed
        if "[" in foreground:
            fg_code = foreground
        else:
            fg_code = getattr(cat.colors.front, foreground) if foreground else ""
        if "[" in background:
            bg_code = background
        else:
            bg_code = getattr(cat.colors.back, background) if background else ""
        return fg_code, bg_code

    @classmethod
    def list(cls):
        return cls.available_themes.keys()

    @classmethod
    def set(cls, new_theme):
        if new_theme in cls.available_themes:
            cls.current_theme = cls.available_themes[new_theme]
        else:
            print(f"Theme '{new_theme}' is not available.")

    @classmethod
    def set_custom(cls, custom):
        cls.current_theme = custom

    @classmethod
    def get(cls):
        # Get the right theme:
        if cls._selected:
            current_theme = cls.available_themes[cls._selected]
        else:
            current_theme = cls.available_themes[cls._default]
        # Check for empty variables and fill if required:
        empty_variables = cls._check_empty_variables(current_theme.value)
        variables_to_remove = []
        if empty_variables:
            for ev in empty_variables:
                # Try to fill required variables with "default" values, aka regular border
                if "header_left" == ev:
                    current_theme._value_.header_left = current_theme._value_.border_left
                    variables_to_remove.append(ev)
                if "header_right" == ev:
                    current_theme._value_.header_right = current_theme._value_.border_right
                    variables_to_remove.append(ev)
                if "title_left" == ev:
                    current_theme._value_.title_left = current_theme._value_.title_left
                    variables_to_remove.append(ev)
                if "title_right" == ev:
                    current_theme._value_.title_right = current_theme._value_.title_right
                    variables_to_remove.append(ev)
        # But we always need to encode color:
        current_theme._value_.color_fg, current_theme._value_.color_bg = cls._get_color_code(current_theme._value_.color_fg, current_theme._value_.color_bg)
        for vrt in variables_to_remove:
            empty_variables.remove(vrt)
        if empty_variables:
            print(f"Warning: The following theme variables are still empty: --> {', '.join(empty_variables)}")
        return current_theme.value
        
#################################################################################################################
#####                                           Print Utils (put                                            #####
#################################################################################################################
class  PrintUtils:
    theme = None
    def _calc_pos_left(text) -> int:
        theme = Theme.get()
        # Calculate the indentation based on the length of the text
        return abs(1 + len(theme.border_right))

    @staticmethod
    def remove_console_codes(text):
        # Remove color codes from text
        if text is None:
            return ""
        return re.sub(r'\033\[[0-9;]+m', '', text)
    
    def _calc_pos_center(cls, text) -> int:
        # Calculate the indentation based on the length of the text
        return abs(AspireCore._get_terminal_width() // 2 * 2 - (len(cls.remove_console_codes(text)) // 2) )

    def _calc_pos_right(cls, text) -> int:
        # Calculate the indentation based on the length of the text
        theme = Theme.get()
        return abs(AspireCore._get_terminal_width() - len(cls.remove_console_codes(text)) - 1 - len(theme.border_right))

    def cursor2pos(pos: int):
        # Move the cursor to column 0
        sys.stdout.write('\r')
        # Get width of terminal window
        width = AspireCore._get_terminal_width()
        # Move the cursor to the desired column
        if pos > width:
            sys.stderr.write(f"pos: {pos} is longer than width: {width}.")
            return False
        if pos < 0:
            sys.stderr.write(f"pos: {pos} must be 0 or larger.")
            return False
        else:
            sys.stdout.write('\033[{}D'.format(pos))
        sys.stdout.flush()
        return #True

    @classmethod
    def _left(cls, text, end='\n'):
        # Print text aligned to the left with specified indention and end character
        theme = Theme.get()
        pos = cls._calc_pos_left(text)
        cls.cursor2pos(pos)
        if AspireCore._is_Windows:
            os.system(f"{theme.color_fg}{text}{cat.reset}")
        else:
            print(f"{theme.color_fg}{text}{cat.reset}", flush=True, end=end)

    @classmethod
    def _right(cls, text, end='\n'):
        # Print text aligned to the right with specified indention and end character
        theme = Theme.get()
        if text != "":
            pos = cls._calc_pos_right(cls, text)
            cls.cursor2pos(pos)
            if AspireCore._is_Windows:
                os.system(f"{theme.color_fg}{text}{cat.reset}")
            else:
                print(f"{theme.color_fg}{text}{cat.reset}", flush=True, end=end)
        else:
            pass

    @classmethod
    def _center(cls, text, end='\n'):
        # Print text centered with specified indention and end character
        theme = Theme.get()
        if text != "":
            pos = cls._calc_pos_center(cls,text)
            cls.cursor2pos(pos)
            if AspireCore._is_Windows:
                os.system(f"{theme.color_fg}{text}{cat.reset}")
            else:
                print(f"{theme.color_fg}{text}{cat.reset}", flush=True, end=end)
        else:
            pass

    @classmethod
    def text(cls, *args, end='\n'):
        # Print text based on the number of arguments
        if len(args) == 0:
            return
        elif len(args) == 1:
            cls._left(args[0], end=end)
        elif len(args) == 2:
            cls._left(args[0], end='')
            cls._right(args[1], end=end)
        elif len(args) == 3:
            cls._left(args[0], end='')
            cls._center(args[1], end='')
            cls._right(args[2], end=end)

    @classmethod
    def border(cls, style='print'):
        theme = Theme.get()
        width = AspireCore._console_width
        if width is None:
            width = 80
        # For border, left alignment is fix
        pos_l = cls.cursor2pos(0)
        if style == 'print':
            left_border = f"{theme.color_fg}{theme.color_bg}{theme.border_left} {cat.reset}"
            center = ""
            right_border = f" {theme.color_fg}{theme.color_bg}{theme.border_right}{cat.reset}"
        elif style == 'header':
            left_border = f"{theme.color_fg}{theme.color_bg}{theme.header_left}"
            right_border = f"{cat.reset}{theme.color_fg}{theme.color_bg}{theme.header_right}"
            center = theme.filler * (width - 2*len(right_border))
        elif style == 'title':
            left_border = f"{theme.color_fg}{theme.color_bg}{theme.title_left} {cat.invert}{theme.color_fg}"
            right_border = f"{cat.reset}{theme.color_fg}{theme.color_bg} {theme.title_right}"
            center = theme.filler * (width - 2*len(right_border))
        else:
            raise ValueError("Invalid style argument. Expected 'print', 'header', or 'title'.")

        if AspireCore._is_Windows:
            os.system(f"{pos_l}{left_border}{center}{cls.cursor2pos(cls._calc_pos_right(right_border))}{right_border}")
        else:
            print(f"{pos_l}{left_border}{center}{right_border}", flush=True, file=AspireCore._border_fd)
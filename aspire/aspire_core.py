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
from aspire_data_color_and_text import cat
from aspire_data_themes import ThemeAttributes
from aspire_data_themes import ThemesList
from aspire_data_themes import 


################################################################################################################
#####                                              Top Class / Definitions                                 #####
################################################################################################################
class AspireCore:
    @staticmethod
    def _isWindows(cls):
        # Checks class atribute, if empty assign a bool to it
        if cls.___isWindows is None:
            if os.name == 'nt':  # Windows
                cls.___isWindows = True
            else:  # Unix-like
                cls.___isWindows = False
        return cls.___isWindows
    
    @staticmethod
    def __create_custom_fd(cls):
        # This aims to create a FileDescriptor to display the borders
        # so stdout for text, and stderr is used for errors.
        if cls.___isWindows:
            # Does not supporte custom FileDescriptors
            return sys.stderr
        else:
            # *nix based Systems on the other hand, do support FD's
            return os.fdopen(os.dup(sys.stderr.fileno()), 'w')
    
    def _get_terminal_width() -> int:
        terminal_size = shutil.get_terminal_size((80, 20))  # Default size if terminal size cannot be determined
        return int(terminal_size.columns)
    
    
    _console_width = _get_terminal_width()
    ___border_fd = __create_custom_fd()
    ___isWindows = _isWindows()


    #################################################################################################################
    #####                                           Theme Stuff                                                 #####
    #################################################################################################################
    class Theme:
        available = {
            'Default': ThemesList.Default,
            'Classic': ThemesList.Classic,
            'Float': ThemesList.Float,
            'Mono': ThemesList.Mono,
        }
        _default = 	"Default"
        _selected = None

        def _check_empty_variables(theme):
            empty_variables = []
            var_skip = ["border_left", "border_right", "filler", ]
            for variable_name, variable_value in theme.__dict__.items():
                if variable_name not in var_skip and variable_value == "":
                    empty_variables.append(variable_name)
            return empty_variables

        @staticmethod
        def _get_color_code(foreground=None, background=None):
            cat = AspireCore.codes
            fg_code = getattr(cat.color.fg, foreground) if foreground else ""
            bg_code = getattr(cat.color.bg, background) if background else ""
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
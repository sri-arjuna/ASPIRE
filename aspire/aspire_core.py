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
#####                                              One time constants                                 #####
################################################################################################################

# Used to set Constanst
def __detect_OS():
    # One time use to detect if MS Winodws or *nix based system like iOS or any GNU+Linux variant.
    if os.name == 'nt':
        # Basicly, detect if OS is Windows based
        return True
    else:
        # Or *nix based
        return False
def __create_custom_fd():
    # This aims to create a FileDescriptor to display the borders
    # so stdout for text, and stderr is used for errors.
    if IS_WINDOWS:
        # Windows does need the terminal to be... "initialized"... by this for the colors to work.
        # No, subprocess.popen("", shell=True) does not work
        os.system("")
        # Windows does not support custom FileDescriptors
        return sys.stderr
    else:
        # *nix based Systems on the other hand, do support FD's
        return os.fdopen(os.dup(sys.stderr.fileno()), 'w')

# Assign value to constant
IS_WINDOWS = __detect_OS()
FD_BORDER = __create_custom_fd()

################################################################################################################
#####                                              Top Class / Definitions                                 #####
################################################################################################################
class AspireCore:
    _console_width = None
    IS_WINDOWS = None
    FD_BORDER = None
    
    def __init__(self):
        self._console_width = self._get_terminal_width()

    @classmethod
    def _IS_WINDOWS(cls):
        # Checks class attribute, if empty assign a bool to it
        if cls._IS_WINDOWS is None:
            if os.name == 'nt':  # Windows
                cls._IS_WINDOWS = True
            else:  # Unix-like
                cls._IS_WINDOWS = False
        return 
    
    @classmethod
    def _create_custom_fd(cls):
        # This aims to create a FileDescriptor to display the borders
        # so stdout for text, and stderr is used for errors.
        if cls._IS_WINDOWS:
            # Does not support custom FileDescriptors
            return sys.stderr
        else:
            # *nix based Systems on the other hand, do support FD's
            return os.fdopen(os.dup(sys.stderr.fileno()), 'w')
    
    @staticmethod
    def _get_terminal_width() -> int:
        terminal_size = shutil.get_terminal_size((80, 20))  # Default size if terminal size cannot be determined
        return int(terminal_size.columns // 2 * 2)

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
        elif foreground is not None:
            fg_code = getattr(cat.colors.front, foreground) if foreground else ""
        if "[" in background:
            bg_code = background
        elif background is not None:
            bg_code = getattr(cat.colors.back, background) if background else ""
        if fg_code is None:
            fg_code = ""
        if bg_code is None:
            bg_code = ""
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
    @staticmethod
    def remove_console_codes(text):
        # Remove color codes from text
        if text is None:
            return ""
        return re.sub(r'\033\[[0-9;]+m', '', text)
    
    def _calc_pos_left() -> int:
        theme = Theme.get()
        # Calculate the indentation based on the length of the text
        return abs(2 + len(theme.border_right))

    def _calc_pos_center(cls, text) -> int:
        # Calculate the indentation based on the length of the text
        return abs(AspireCore._get_terminal_width() // 2 - (len(cls.remove_console_codes(text)) // 2) )

    def _calc_pos_right(cls, text) -> int:
        # Calculate the indentation based on the length of the text
        theme = Theme.get()
        return abs(AspireCore._get_terminal_width() - len(cls.remove_console_codes(text)) - len(theme.border_right))

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
            #sys.stdout.write('\033[{}D'.format(pos))
            sys.stdout.write(f'\033[{pos}G')
        sys.stdout.flush()
        return #True

    @classmethod
    def _left(cls, text, style='print', end='\n'):
        # Print text aligned to the left with specified indention and end character
        theme = Theme.get()
        pos = cls._calc_pos_left()
        cls.cursor2pos(pos)
        #if AspireCore.IS_WINDOWS:
        #    os.system(f"{theme.color_fg}{theme.color_bg}{text}{cat.reset}")
        #else:
        #    print(f"{theme.color_fg}{text}{cat.reset}", flush=True, end=end)

        if "header" == style:
            print(f"{theme.color_fg}{theme.color_bg}{text}", flush=True, end=end)
        else:
            print(f"{theme.color_fg}{text}{cat.reset}", flush=True, end=end)

    @classmethod
    def _right(cls, text, style='print', end='\n'):
        # Print text aligned to the right with specified indention and end character
        theme = Theme.get()
        if text != "":
            pos = cls._calc_pos_right(cls, text)
            cls.cursor2pos(pos)
            #if AspireCore.IS_WINDOWS:
            #    os.system(f"{theme.color_fg}{text}{cat.reset}")
            #else:
            #    print(f"{theme.color_fg}{theme.color_bg}{text}{cat.reset}", flush=True, end=end)
            if "print" == style:
                # Default, just font
                print(f"{theme.color_fg}{text}{cat.reset}", flush=True, end=end)
            elif "header" == style:
                # Regular bg, full
                print(f"{theme.color_fg}{theme.color_bg}{text}{cat.reset}", flush=True, end=end)
            elif "title" == style:
                # TODO fix: Invert colors
                inv_BG, inv_FG = Theme._get_color_code(theme.color_bg, theme.color_fg)
                print(f"{inv_BG}{inv_FG}{text}{cat.reset}", flush=True, end=end)
        else:
            pass

    @classmethod
    def _center(cls, text, style='print', end='\n'):
        # Print text centered with specified indention and end character
        theme = Theme.get()
        if text != "":
            pos = cls._calc_pos_center(cls,text)
            cls.cursor2pos(pos)
            #if AspireCore.IS_WINDOWS:
            #    os.system(f"{theme.color_fg}{text}{cat.reset}")
            #else:
            #    print(f"{theme.color_fg}{theme.color_bg}{text}{cat.reset}", flush=True, end=end)
            if "print" == style:
                # Default, just font
                print(f"{theme.color_fg}{text}{cat.reset}", flush=True, end=end)
            elif "header" == style:
                # Regular bg, full
                print(f"{theme.color_fg}{theme.color_bg}{text}{cat.reset}", flush=True, end=end)
            elif "title" == style:
                # TODO fix: Invert colors
                print(f"{theme.color_fg}{theme.color_bg}{cat.codes.invert}{text}{cat.reset}", flush=True, end=end)
        else:
            pass

    @classmethod
    def text(cls, *args, **kwargs):
        style = kwargs.get("style", "print")
        end = kwargs.get("end", "\n")
        # Print text based on the number of arguments
        if "title" == style:
                cls._center(args[0], style=style, end=end)
                return
        
        if len(args) == 0:
            return
        elif len(args) == 1:
            if "title" == style:
                print("------  testing+")
                cls._center(args[0], style=style, end=end)
            else:
                cls._left(args[0], style=style, end=end)
                print("------  testing+ baldfkjabdlskfasdlbkf ------------------")
        elif len(args) == 2:
            cls._left(args[0], style=style, end='')
            cls._right(args[1], style=style, end=end)
        elif len(args) == 3:
            cls._left(args[0], style=style, end='')
            cls._center(args[1], style=style, end='')
            cls._right(args[2], style=style, end=end)

    @classmethod
    def border(cls, style='print'):
        theme = Theme.get()
        width = AspireCore._get_terminal_width()
        
        if style == 'header':
            left_border = f"{theme.color_fg}{theme.color_bg}{theme.header_left}"
            right_border = f"{theme.color_fg}{theme.color_bg}{theme.header_right}{cat.reset}"
            #center = theme.filler * (width - 2*len(right_border))
        elif style == 'title':
            left_border = f"{theme.color_fg}{theme.color_bg}{theme.title_left}{cat.codes.invert}" #{inv_BG}{inv_FG}"
            right_border = f"{cat.reset}{theme.color_fg}{theme.color_bg}{theme.title_right}{cat.reset}"
            #center = theme.filler * (width - 2*len(right_border))
        elif style == 'print':
            left_border = f"{theme.color_fg}{theme.color_bg}{theme.border_left}{cat.reset}"
            #center = (width - 2 * len(theme.border_left)) // 2 * 2  * " "
            right_border = f"{theme.color_fg}{theme.color_bg}{theme.border_right}{cat.reset}"
        else:
            raise ValueError("Invalid style argument. Expected 'print', 'header', or 'title'.")

        #if AspireCore.IS_WINDOWS:
        #    os.system(f"{pos_l}{left_border}{center}{cls.cursor2pos(cls._calc_pos_right(right_border))}{right_border}")
        #else:
        #print(f"{left_border}{center}{right_border}", flush=True, file=AspireCore.FD_BORDER, end="")

        if theme.filler == "":
            fill = " "
        else:
            if "print" == style:
                fill = " "
            else:
                fill = theme.filler
        center = (width - 2 * len(theme.border_left)) // 2 * 2  * fill

        # Print Border Left
        cls.cursor2pos(0)
        print(f"{left_border}", flush=True, file=AspireCore.FD_BORDER, end="")

        #if style == "title":
        #    cls.cursor2pos(width - len(theme.border_right) )
        #else:
        #    print(f"{center}", flush=True, file=AspireCore.FD_BORDER, end="")
        
        print(f"{center}", flush=True, file=AspireCore.FD_BORDER, end="")
        print(f"{right_border}", flush=True, file=AspireCore.FD_BORDER, end="")


        
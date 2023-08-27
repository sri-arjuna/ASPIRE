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
#import platform
import msvcrt
import re
import shutil
import subprocess
import sys
import string

# Prepare data structures
from collections import namedtuple
from dataclasses import dataclass
from enum import Enum

# Import internal tools
from .aspire_data_color_and_text import cat
#from .aspire_data_themes import ThemeAttributes
from .aspire_data_themes import ThemesList
from .aspire_string_utils import StringUtils as stew

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
    #_console_width = None
    IS_WINDOWS = None
    FD_BORDER = None
    width_line_full = 0
    width_line_inner = 0

    def __init__(self):
        # TODO remove, this one is old now -- just as fallback
        #self._console_width = self._get_terminal_width()
        # Get 'static' workspace for this call
        theme = Theme.get()
        self.width_line_full = self._get_terminal_width()
        self.width_line_inner = self.width_line_full - len(theme.border_left) - len(theme.border_right) - 2
        
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
        try:
            terminal_size = shutil.get_terminal_size((80, 20))
            return int(terminal_size.columns // 2) * 2
        except (AttributeError, KeyError):
            # Fallback for cases where terminal size cannot be determined
            return 80  # Default width
    
    @staticmethod
    def get_input_charcount(count:int) -> str:
        # Use the subprocess module to invoke the shell and read a single character
        if IS_WINDOWS:
            chars = []
            while len(chars) < count:
                char = msvcrt.getch()
                # Check if char is printable
                if char in string.printable.encode():
                    char_str = char.decode()
                    chars.append(char_str)
                    # Check for Enter key press
                    if char_str == '\r' and len(chars) >= 1:
                        break
            return ''.join(chars)
        else:
            # Expecting a linux based system
            result = subprocess.run(["read", "-n", count], capture_output=True, text=True, shell=True)
            chars = result.stdout.strip()
            return chars

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
        'Admin': ThemesList.Admin,
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
            sys.stdout.write(f'\033[{pos}G')
        sys.stdout.flush()
        return

    @classmethod
    def _left(cls, text, style='print', end='\n'):
        # Print text aligned to the left with specified indention and end character
        theme = Theme.get()
        pos = cls._calc_pos_left()
        cls.cursor2pos(pos)
        if "header" == style:
            print(f"{theme.color_fg}{theme.color_bg}{text}{cat.reset}", flush=True, end=end)
        else:
            print(f"{text}{cat.reset}", flush=True, end=end)

    @classmethod
    def _right(cls, text, style='print', end='\n'):
        # Print text aligned to the right with specified indention and end character
        theme = Theme.get()
        if text != "":
            pos = cls._calc_pos_right(cls, text)
            cls.cursor2pos(pos)
            if "print" == style:
                # Default, just font
                print(f"{text}{cat.reset}", flush=True, end=end)
            elif "header" == style:
                # Regular bg, full
                print(f"{theme.color_fg}{theme.color_bg}{text}{cat.reset}", flush=True, end=end)
            #elif "title" == style:
                # TODO fix: Invert colors
            #    print(f"{theme.color_bg}{theme.color_fg}{text}{cat.reset}", flush=True, end=end)
        else:
            pass

    @classmethod
    def _center(cls, text, style='print', end='\n'):
        # Print text centered with specified indention and end character
        theme = Theme.get()
        pre = ""
        if text != "":
            if "title" in style:
                text = f" {text} "
                pos = cls._calc_pos_center(cls,text)
                if theme.title_bold:
                    pre += f"{cat.text.bold}"
                if theme.title_underline:
                    pre += cat.text.underline
                if theme.title_italic:
                    pre += cat.text.italic
            else:
                pos = cls._calc_pos_center(cls,text)
            cls.cursor2pos(pos)
            if "print" == style:
                # Default, just font
                print(f"{text}{cat.reset}", flush=True, end=end)
            elif "header" == style:
                # Regular bg, full
                print(f"{theme.color_fg}{theme.color_bg}{text}{cat.reset}", flush=True, end=end)
            elif "title" == style:
                # TODO fix: Invert colors
                print(f"{theme.color_fg}{theme.color_bg}{cat.codes.invert}{pre}{text}{cat.reset}", flush=True, end=end)
        else:
            pass

    @classmethod
    def text(cls, *args, **kwargs):
        # Get key arguments
        style = kwargs.get("style", "print")
        end = kwargs.get("end", "\n")
        LineLength = kwargs.get("LineLength", 80)
        theme = Theme.get()
        #LineLengthOutter = int(AspireCore._get_terminal_width())
        #LineLength = LineLengthOutter - len(theme.border_left) - len(theme.border_right) - 2
        #AC = AspireCore()
        #LineLength = AC.width_line_inner
        
        # Init variable to represent passed text
        len_arg = 0
        for a in args:
            # Just take printable chars into account
            len_arg += len(cls.remove_console_codes(a))

        # Print text based on the number of arguments
        # Start with the exception
        if "title" == style:
            if stew.split_needed(len_arg, LineLength, 50, style=style):
                pos = stew.split_calc_char_pos(LineLength, 50)
                lines = stew.split_string_preserve_words(args[0], pos)
                cls._center(lines[0], style=style, end="\n")
                cls.text(lines[1], style=style, end="\n")
                return
            else:
                cls._center(args[0], style=style, end=end)
                return
        elif "status" == style:
            if stew.split_needed(args[1], LineLength, 50, style=style):
                lines = stew.split_shorten(args[1], LineLength - len(args[0]) - 2)
                cls.text(lines,args[1],style=style, end="\n")
                return
            else:
                # Regular call, no shortening needed
                cls.text(args[0], args[1], style=style, end="\n")
        
        if len(args) == 0:
            cls._left("", style=style, end=end)
            return
        elif len(args) == 1:
            if stew.split_needed(len_arg, LineLength, 75, style=style):
                pos = stew.split_calc_char_pos(LineLength, 75)
                lines = stew.split_string_preserve_words(args[0], pos)
                cls._left(lines[0], style=style, end="\n")
                cls.border(style=style)
                cls._right(lines[1], style=style, end="\n")
                return
            else:
                #print(f"DEBUG SPLIT 2 - {width_inside} // {len_arg}")
                cls._left(args[0], style=style, end=end)
                return
        elif len(args) == 2:
            if stew.split_needed(len_arg, LineLength, 50, style=style):
                # We do need splitting, lets check if we can solve it by one argument per line..
                if len(args[0]) < AspireCore.width_line_inner and len(args[1]) < LineLength:
                    # Each is smaller, so lets keep simple:
                    cls._left(args[0], style=style, end="\n")
                    cls.border(style=style)
                    cls._right(args[1], style=style, end=end)
                    return
                else:
                    # No, we actualy need to split both.
                    pos = stew.split_calc_char_pos(LineLength, 50)
                    linesL = stew.split_string_preserve_words(args[0], pos)
                    linesR = stew.split_string_preserve_words(args[1], pos)

                    #textL = args[0]
                    #linesL = [textL[i:i+len_arg] for i in range(0, len(textL), len_arg)]
                    #textR = args[1]
                    #linesR = [textR[i:i+len_arg] for i in range(0, len(textR), len_arg)]
                    cls.text(linesL[0], linesR[0], style=style, end="\n")
                    cls.border(style=style)
                    # TODO -- Should this not split up any text that is too long?
                    cls.text(linesL[1], linesR[1], style=style, end="\n")
                    return
            else:
                cls._left(args[0], style=style, end='')
                cls._right(args[1], style=style, end=end)
                return
        elif len(args) == 3:
            #TODO 3 split
            if stew.split_needed(len_arg, LineLength, 30, style=style):
                # We do need splitting, lets check if we can solve it by one argument per line..
                if len(args[0]) < LineLength and len(args[2]) < LineLength:
                    # Each is smaller, so lets keep simple:
                    cls.text(args[0], args[2], style=style, end="\n")
                    cls.border(style=style)
                    cls.text("", args[1], "", style=style, end=end)
                    return
                else:
                    # Gotta split each text, just to be sure.
                    pos = stew.split_calc_char_pos(LineLength, 30)
                    linesL = stew.split_string_preserve_words(args[0], pos)
                    linesC = stew.split_string_preserve_words(args[1], pos)
                    linesR = stew.split_string_preserve_words(args[2], pos)

                    cls.text(linesL[0], linesC[0], linesR[0], style=style, end="\n")
                    cls.border(style=style)
                    cls.text(linesL[1], linesC[1], linesR[1], style=style, end=end)
                    return
            else:
                # No splitting required, nice :)
                cls._left(args[0], style=style, end='')
                cls._center(args[1], style=style, end='')
                cls._right(args[2], style=style, end=end)
                return

    @classmethod
    def border(cls, style='print'):
        theme = Theme.get()
        width = AspireCore._get_terminal_width()
        len(theme.border_left)
        
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

        # Prepare filler chars / line
        if "header" == style:
            fill = theme.header_filler
        elif "title" == style:
            fill = theme.title_filler
        else:
            if "print" == style:
                fill = " "
        if fill == "":
            fill = " "
        
        # Print "filler"
        center = (width - 2 * len(theme.border_left)) // 2 * 2  * fill

        # Print Border Left
        cls.cursor2pos(0)
        print(f"{left_border}", flush=True, file=AspireCore.FD_BORDER, end="")
        
        print(f"{center}", flush=True, file=AspireCore.FD_BORDER, end="")
        print(f"{right_border}", flush=True, file=AspireCore.FD_BORDER, end="")


        
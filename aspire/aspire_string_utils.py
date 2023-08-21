# Basic header:
"""
	Created on:		2023.July.02
	Created by:		Simon Arjuna Erat
	License:		MIT
	URL:			https://www.github.com/sri-arjuna/ASPIRE
"""



class StringUtils:
    # Make it easier to use - internal function
    def needs_split(txt_len: int, percentage: int, style="print"):
        from .aspire_core import AspireCore
        AC = AspireCore()
        if txt_len >= AC.width_line_inner: #width_inside:
            # Text is too long
            return True
        else:
            # Basicly, no split required, but there are exceptions
            # Specificly, if it is title, text should not be longer than 50 percentage (or the passed percentage)
            if style == "title" and percentage <= (AC.width_line_inner / 100 * txt_len):
                return True
            return False
        
    # Split string at provided percentage
    # prfered at white space, or if not possible, hard value
    def split_string_preserve_words(text, percentage):
        total_length = len(text)
        split_index = int(total_length * percentage / 100)
        
        # Find the nearest whitespace before or at the split index
        while split_index > 0 and not text[split_index].isspace():
            split_index -= 1
        
        # If we didn't find a whitespace, just split at the provided index
        if split_index == 0:
            split_index = int(total_length * percentage / 100)
        
        line0 = text[:split_index].strip()
        line1 = text[split_index:].strip()
        
        # If line0 or line1 is empty, consider splitting the string without preserving words
        if not line0 or not line1:
            split_index = int(total_length * percentage / 100)
            line0 = text[:split_index].strip()
            line1 = text[split_index:].strip()
        
        return [line0, line1]
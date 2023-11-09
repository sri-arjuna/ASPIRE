# Basic header:
"""
	Created on:		2023.July.02
	Created by:		Simon Arjuna Erat
	License:		MIT
	URL:			https://www.github.com/sri-arjuna/ASPIRE
"""



class StringUtils:
    # Make it easier to use - internal function
    def split_needed(txt_len: int, LineLength:int, percentage: int, style="print"):
        if txt_len >= LineLength:
            # Text is too long
            return True
        else:
            # Basicly, no split required, but there are exceptions
            # Specificly, if it is title, text should not be longer than 50 percentage (or the passed percentage)
            if style == "title" and 50 <= (LineLength / 100 * txt_len):
                return True
            return False
        
    # Gets the char count at which it shall split the text
    # Returns desired split position
    def split_calc_char_pos(LineLength: int, Percentage: int):
        split_pos = 100 // LineLength * Percentage
        return split_pos
    
    # Split string at provided percentage
    # prfered at white space, or if not possible, hard value
    def split_string_preserve_words(text, max_chars):
        total_length = len(text)
        
        if total_length <= max_chars:
            return [text.strip(), ""]
        
        # Find the nearest whitespace before or at the max_chars index
        split_index = max_chars
        while split_index > 0 and not text[split_index].isspace():
            split_index -= 1
        
        # If we didn't find a whitespace, just split at the provided index
        if split_index == 0:
            split_index = max_chars
        
        line0 = text[:split_index].strip()
        line1 = text[split_index:].strip()
        
        # If line0 or line1 is empty, consider splitting the string without preserving words
        if not line0 or not line1:
            split_index = max_chars
            line0 = text[:split_index].strip()
            line1 = text[split_index:].strip()
        
        return [line0, line1]
    
    # Shorten text to fit into char_count, mostly used for tui.status
    # optional: can shorten text at end.
    def split_shorten(txt: str, char_count: int, cut_from_middle: bool = False) -> str:
        if len(txt) <= char_count:
            return txt
        
        if cut_from_middle:
            remaining_chars = char_count - 3
            side_chars = remaining_chars // 2
            shortened_text = f"{txt[:side_chars]}...{txt[-side_chars:]}"
        else:
            side_chars = (char_count - 3) // 2
            shortened_text = f"{txt[:side_chars]}...{txt[-side_chars:]}"

        return shortened_text

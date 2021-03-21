""" text_block.py """

import logging

class TextBlock:
    """
    A list of strings
    """
    def __init__(self, line: str, wrap: int = 1):
        """
        Constructor

        Break a line of text into the requested number or roughly even
        lines, splitting only on spaces.

        :param line: A single line of text without any newlines in it
        :param wrap: The number of lines desired in the text block
        """
        self.logger = logging.getLogger(__name__)
        if not line:
            self.logger.exception('Tried to wrap an empty line')
        self.wrap = wrap  # Number of requested lines, may not match actual total wrapped lines
        self.text = []

        # How many lines will there actually be in this text block?
        num_lines = max(1, self.wrap)  # Must be a positive int > 0
        num_lines = min(num_lines, line.count(' ')+1)  # Num lines can't be more than the number of spaces + 1

        num_chars = len(line)
        max_len = round(num_chars / num_lines)
        line_remaining = line[:] # Copy the original line
        while num_lines > len(self.text)+1 and ' ' in line_remaining:
            # Keep going as long as the remaining line exceeds our desired box width AND has at least one space in it
            caret = max_len-1  # Put the caret at our desired box width
            if line_remaining[caret] == ' ':  # Caret is on a space, so just cut the line there
                self.text.append(line_remaining[:caret])
                line_remaining = line_remaining[caret+1:]
            else:  # Cut at the space nearest to caret (there must be one either to the right or left
                lspace = line_remaining[:caret].rfind(' ')  # Get space on left distance, if any, from start of line
                rspace = line_remaining[caret:].find(' ')  # Get space on right distance, if any, from caret
                # If either of these is -1, there is no space in that direction, so make it the longest possible dist
                # There is definitely at least one space left, right or both or we wouldn't be here
                ldist = num_chars if lspace == -1 else caret-lspace
                rdist = num_chars if rspace == -1 else rspace
                cut = caret-ldist if ldist <= rdist else caret+rdist  # Move left or right of the caret to find the cut
                self.text.append(line_remaining[:cut])
                line_remaining = line_remaining[cut+1:]

        if line_remaining:
            # Put any left over text in the last line of our block
            self.text.append(line_remaining)

    def __repr__(self):
        return f'R: {self.wrap} T: {self.text}'


if __name__ == "__main__":
    # Run tests
    lines = ['visual',
             'visual elements can be presented according to',
             'defines style of visual elements for',
             'represents semantic elements with',
             'organizes annotation on',
             'a b',
             'requires semantic elements of',
             'frames placement of',
             'R16'
             ]
    nums = [4, 2, 3, 2, 8, 2, 3, 2, 1]
    blocks = [TextBlock(line=l, wrap=n) for l, n in zip(lines, nums)]
    for b in blocks:
        print(b)
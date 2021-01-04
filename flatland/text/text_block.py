""" text_block.py """

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
        assert line, "Tried to create empty text block"

        self.wrap = wrap  # Number of requested lines, may not match actual total wrapped lines
        self.text = []

        # How many lines will there actually be in this text block?
        num_lines = max(1, self.wrap)  # Must be a positive int > 0
        num_lines = min(num_lines, line.count(' ')+1)  # Num lines can't be more than the number of spaces + 1

        num_chars = len(line)
        max_len = round(num_chars / num_lines)
        line_remaining = line[:] # Copy the original line
        while num_lines > len(self.text)+1 and ' ' in line_remaining:
            caret = max_len-1
            if line_remaining[caret] == ' ':
                self.text.append(line_remaining[:caret])
                line_remaining = line_remaining[caret+1:]
            else:
                lspace = line_remaining[:caret].rfind(' ')  # Get left space distance from caret
                rspace = line_remaining[caret:].find(' ')  # Get right space distance from caret
                ldist = caret-lspace
                rdist = rspace
                cut = caret+rdist if rdist <= ldist else caret-ldist
                self.text.append(line_remaining[:cut])
                line_remaining = line_remaining[cut+1:]

        if line_remaining:
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
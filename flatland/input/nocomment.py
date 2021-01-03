"""
nocomment.py – Remove comments and trailing whitespace from file
"""

from typing import Optional


def nocomment(lines: str, prefix='//') -> Optional[str]:
    """
    Remove all comments blank lines and trailing whitespace from input
    :param lines:
    :param prefix:  Characters such as // used to signal a comment
    :return: A list of lint free strings
    """

    # Extract all lines that don't start with the comment prefix
    # Among those lines, split at the comment prefix, if any, and only take the left hand side
    # stripped of any whitespace on the right
    comments_stripped = [l.split(prefix)[0].rstrip() for l in lines.split('\n') if not l.startswith(prefix)]
    if not comments_stripped:
        return None
    # Join all of non-empty lines with newlines and return the string
    # Ensure that the last line is terminated by a newline
    return '\n'.join([l for l in comments_stripped if l]) + '\n'


if __name__ == "__main__":
    comment_prefix = '//'
    test_text = 'First line\n\n  \nKeyword and some text // Comment\n    arg1 arg2 // comment\n    abc //     \n //\n'
    print('---')
    print(test_text)
    print('---')
    print(nocomment(test_text, comment_prefix))
    print('---')

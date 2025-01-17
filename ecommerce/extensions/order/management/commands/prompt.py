from __future__ import absolute_import

import sys

from six.moves import builtins


def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {
        "yes": True,
        "y": True,
        "no": False,
        "n": False,
    }
    if default is None or default in list(valid.keys()):
        prompt = " [y/n] "
    else:
        raise ValueError("Invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = builtins.raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with one of the following ({}).\n".format(', '.join(list(valid.keys()))))

import sys

def error(message):
    """
    Throw an error with the given message and immediatly quit.

    Args:
        message(str): The message to display.
    """
    sys.exit("Error: {}".format(message))

def pick_one(options):
    numbered_options = dict(enumerate(options))
    for key, value in numbered_options.items():
        print "{}. {}".format(key+1, value)
    ans = raw_input("> ")
    return numbered_options.get(int(ans)-1)

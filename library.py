import config
import sys
import datetime


def debugPrint(prefix, string):
    if config.DEBUG:
        print "BEBUG: \"%s\" --> %s" % (prefix, string)

def debugPrintString(string):
    if config.DEBUG:
        print "DEBUG: %s" % string


def query_yes_no_quit(question, default="yes"):
    """Ask a yes/no/quit question via raw_input() and return their answer.
    
    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no", "quit" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes", "no" or "quit".
    """
    valid = {"yes":"yes",   "y":"yes",    "ye":"yes",
             "no":"no",     "n":"no",
             "quit":"quit", "qui":"quit", "qu":"quit", "q":"quit"}
    if default == None:
        prompt = " [y/n/q] "
    elif default == "yes":
        prompt = " [Y/n/q] "
    elif default == "no":
        prompt = " [y/N/q] "
    elif default == "quit":
        prompt = " [y/n/Q] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while 1:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return default
        elif choice in valid.keys():
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes', 'no' or 'quit'.\n")

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.
    
    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes":"yes",   "y":"yes",  "ye":"yes",
             "no":"no",     "n":"no"}
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while 1:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return default
        elif choice in valid.keys():
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "\
                             "(or 'y' or 'n').\n")

# input: 20110605 or 2011060505
# return datetime
def toDatetime(date_str):
    '''
    >>> toDatetime('20110605')
    (datetime.date(2011, 6, 5), None)
    >>> toDatetime('2011060505')
    (datetime.date(2011, 6, 5), datetime.time(5, 0))
    # TODO: Do this
    >>> toDatetime('1202101743') #doctest: +SKIP
    '''
    timep = True
    try:
        yyyy = int(date_str[:4])
        mm = int(date_str[4:6])
        dd = int(date_str[6:8])
    except:
        sys.stderr.write('Correct input?')

    try:
        hh = int(date_str[8:10])
    except:
        timep = False
    try:
        minute = int(date_str[10:12])
    except:
        minute = 0

    if timep:
        return datetime.date(year=yyyy, month=mm, day=dd),\
            datetime.time(hour=hh, minute=minute)
    else:
        return datetime.date(year=yyyy, month=mm, day=dd), None


### Pretty printing
# from http://ginstrom.com/scribbles/2007/09/04/pretty-printing-a-table-in-python/
import locale
locale.setlocale(locale.LC_NUMERIC, "")


def format_num(num):
    """Format a number according to given places.
    Adds commas, etc. Will truncate floats into ints!"""

    try:
        inum = int(num)
        return locale.format("%.*f", (0, inum), True)

    except (ValueError, TypeError):
        return str(num)


def get_max_width(table, index):
    """Get the maximum width of the given column index"""
    
    return max([len(format_num(row[index])) for row in table])


def pprint_table(out, table):
    """Prints out a table of data, padded for alignment
    @param out: Output stream (file-like object)
    @param table: The table to print. A list of lists.
    Each row must have the same number of columns. """

    col_paddings = []

    for i in range(len(table[0])):
        col_paddings.append(get_max_width(table, i))

    for row in table:
        # left col
        print >> out, row[0].ljust(col_paddings[0] + 1),
        # rest of the cols
        for i in range(1, len(row)):
            col = format_num(row[i]).rjust(col_paddings[i] + 2)
            print >> out, col,
        print >> out



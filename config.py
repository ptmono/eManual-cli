#!/usr/bin/python
# coding: utf-8

CREATE_ACTION = 1
MODIFY_ACTION = 2
DELETE_ACTION = 3

# OptionParser requires
# ("-p", "--purpose", dest="arg_purpose", help="the purpose")
# form.
# For kwargs we have to use dictionary
args = [
    # Actions
    [["--delete"], {'dest':"arg_delete",
                    'help':"Delete <element|group>", 'action':"store_true"}],
    [["--create"], {'dest':"arg_create", 
                    'help':"Create <element|group>", 'action':"store_true"}],
    [["--schedule"], {'dest':"arg_schedule",
                      'help':"schedule <element|group>", 'action':"store_true"}],
    [["--record"], {'dest':"arg_record",
                    'help':"We done, let's record that.", 'action':"store_true"}],
    [["-l", "--list"], {'dest':"arg_list",
                        'help':"list the databases.", 'action':"store_true"}],

    # Data
    [["-n", "--name"], {'dest':"arg_name", 'help':"the name"}],
    [["-g", "--gname"], {'dest':"arg_groupname", 'help':"the group name"}],

    [["--ea"], {'dest':"arg_elementargs", 'help':"the element arguments"}],
    [["--ga"], {'dest':"arg_groupargs", 'help':"the group arguments. It is the names of element that will be grouped."}],

    [["-s", "--shortcuts"], {'dest':"arg_shortcut", 'help':"the shortcuts"}],

    [["--db"], {'dest':"arg_database", 'help':"the database filename"}],

    ]

# Let's determine the action
# 순서대로 적용됩니다. 먼저 조건에 맞는다면 아래는 적용되지 않습니다.
# 괄호는 or을 의미합니다.
action_args = [
    [("-l", "--list"), "listTable"],
    ["--delete", ("-n", "-g"), "delete"],
    ["--delete", "deleteShort"], 			# arg is name
    ["--ea", "createElement"],                          # None arg
    ["--ga", "createGroup"],                   		# arg is name of group
    ["--schedule", ("-n", "-g"), "schedule"],	 	# arg is date
    ["--record", ("-n", "-s"), "record"],
    ["--record", "recordShort"],   		    	# arg is record
    ]

usage = \
"""usage: %prog options arg

--create --ea name=test,purpose=53,shortcut=tes,unit=num
--create --ga test test_group
--ea name=test,purpose=53,shortcut=tes,unit=num
--ga test test_group
--ga test,test2 test_group2
--list
--list element
--schedule -n test <DATE>
--schedule -g test_group <DATE>
--record -n test 10
--record -s tes 10
--record tes 10
"""

DEBUG = 0

# Default the database name
dbname = "exercise2.sqlite"


# exclude characters for database
# We use re.search.
dbexclude_chars = ['=', ',', '.', '[', ']']

def CreateShortToUsualDic(args):
    # shortcut either be or not. We must have longcut.
    dic = {}
    for arg in args:
        part_of_option = arg[0]
        shortcut = _getShortcut(part_of_option)
        if shortcut:
            longcut = _getLongcut(part_of_option)
            dic[shortcut] = longcut
    return dic
        

def _getShortcut(arg):
    for a in arg:
        if a[1] == '-':
            return a
    return False

def _getLongcut(arg):
    # We support that we have one longcut.
    for a in arg:
        if not len(a) == 2:
            return a
    return False

    
    

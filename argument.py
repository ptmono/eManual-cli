#!/usr/bin/python
# coding: utf-8

from optparse import OptionParser
import types

import config
from library import *

_DBP = debugPrint
_DBPS = debugPrintString

# FIXME: It is more reusable to add the action into optparse class.
# FIXME: We need more useful method.
def action(*args):
    """To determine the action. It is determined in config.action_args. args
    are from sys.args. The function will return an integer which is in
    config."""

    # *args will recive the args as tuple like
    # (['-a', 'aaa', '-d', 'ddd', '-n', 'fdskf', 'abc'],)
    args = args[0]

    for action_arg in config.action_args:
        action_arg_count = len(action_arg[:-1])
        action_arg_action = action_arg[-1]
        required_args_number = action_arg_count
        arg_count = 0

        # substitute arg
        for action_arg_element in action_arg[:-1]:
            debugPrint('element', action_arg_element)
            # It can be a tuple. So we use _check_memq
            debugPrint("_check_memq", _check_memq(action_arg_element, args))
            if not _check_memq(action_arg_element, args):
                break           # Let's go next action_arg
            debugPrint('arg_count_in', arg_count)
            arg_count += 1

        # action_arg is the action
        debugPrint('arg_count', arg_count)
        debugPrint('action_arg_count', action_arg_count)

        if arg_count == action_arg_count:
            return action_arg_action

    # bad arg
    return 0


def _check_memq(element, compared_list):
    """We check that element is a part of compared_list. The element can
    be tuple. It is applied or 연산. It will return True when element is a
    part of compared_list. Other is False"""
    if isinstance(element, types.TupleType):
        if _mem_orq(element, compared_list):
            return True
    else:
        if _memq(element, compared_list):
            return True
    return False

def _memq(element, compared_list):
    "It will return True when compared_list list contains element. Other is False."
    _DBP("_memq.compared_list", compared_list)
    for c_element in compared_list:
        _DBP("_memq.c_element", c_element)
        if element == c_element:
            return True
    return False

def _mem_orq(tuple_element, compared_list):
    """It will return True when compared_list contains one of elements of
    tuple_element tuple. Other is False."""
    for element in tuple_element:
        if _memq(element, compared_list):
            return True
    return False

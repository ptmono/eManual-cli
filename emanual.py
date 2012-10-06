#!/usr/bin/python
# coding: utf-8

import getopt
import sys
import types
import os

from optparse import OptionParser, Option, OptionContainer, Values
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import FlushError

import config
import argument
from library import *
import db

_DBP = debugPrint
_DBPS = debugPrintString


class ActionBase(object):
    def __init__(self):

        #FIXME: I want to extract the_action from the instance options.
        argv = sys.argv[1:]
        self.the_action = argument.action(argv)

    def do(self):
        if self.the_action:
            func = getattr(self, 'do_' + self.the_action)
            return func()
        else:
            sys.stdout.write("We require the major options. See --help or -h.\n")

    def createOptionsAsSelf(options):
        for arg in options:
            setattr(self, arg, options[arg])


#TODO: We need a method to check the inputs for security. I think it can
#be to modify the methods of elixir. And test SQL injection.
class Action(ActionBase):
    """
    >>> db.init_test(create_db=True)
    >>> options_createElement = {'arg_elementargs' : 'name=test,purpose=53,shortcut=abbccd,unit=num'}
    >>> options = Values(options_createElement)
    >>> actionObj = Action(options,None)
    >>> actionObj.do_createElement() #doctest: +ELLIPSIS
    The element ...
    {...}

    >>> actionObj._listDbTable()
    ['db_element', 'db_group', 'db_record', 'db_group_fk_elements__db_element', 'db_schedule']

    #########
    ##### None argument of Action
    >>> new_element = 'name=direct_element,purpose=100,shortcut=direce,unit=num'
    >>> action = Action(None, None)
    >>> action.do_createElement(new_element) #doctest: +ELLIPSIS
    The element ...
    {...}

    #########
    ##### Error handling of createGroup
    >>> element_names = ['test', 'direct_element']
    >>> group_name = 'gname1'
    >>> action.do_createGroup(element_names, group_name)
    >>> # duplication
    >>> action.do_createGroup(element_names, group_name) #doctest: +SKIP

    #########
    ##### schedule
    >>> actionObj.do_schedule('test', '20120605', 'element')
    >>> actionObj.do_schedule('gname1', '2012060512' 'group')


    """
    
    def __init__(self, options, args):
        super(Action, self).__init__()
        self.options = options
        self.args = args

    def _dbInstance(self, name, title=True):
        "Return the instance of the table of database."
        if title:
            # Let's upper first character. db use that.
            titled_name = name.title()
        else:
            titled_name = name

        try:
            return getattr(db, titled_name)
        except AttributeError, e:
            raise NameError, 'The database has no table named "%s"\n' % \
                titled_name


    def _output_error(self, output, err=None):
        msg = 'ERROR: ' + output + '\n'
        if err:
            sys.stderr.write(msg % str(err))
        else:
            sys.stderr.write(msg)
        sys.exit(1)


    def _arg_zero_required(self):
        try: num_args = len(self.args)
        except TypeError: num_args = 0
        if not num_args == 0:
            self._output_error("We don't need arguments. Bad argument %s", err=str(self.args))


    def ea_parser(self, element_args):
        """
        Our element_arg '--ea' has a specified form '--ea
        name=test,purpose=53,shortcut=[ab,bc,cd]'. We check this form.
        shortcut only need list.

        >>> ak1 = "name=test,purpose=53,shortcut=[ab,bc,cd],unit=num"
        >>> ak2 = "name=test,purpose=53,shortcut=abbccd.unit=num"
        >>> correct = "name=test,purpose=53,shortcut=abbccd,unit=num"
        >>> ab = Action(ak1, None)
        >>> ab.ea_parser(ak1)
        Traceback (most recent call last):
        ...
        InputError: "Bad argument ['name=test', 'purpose=53', 'shortcut=[ab', 'bc', 'cd]', 'unit=num']"
        >>> ab = Action(ak2, None)
        >>> ab.ea_parser(ak2)
        Traceback (most recent call last):
        ...
        InputError: "Bad argument ['name=test', 'purpose=53', 'shortcut=abbccd.unit=num']"
        >>> ab = Action(correct, None)
        >>> ab.ea_parser(correct)
        {'unit': 'num', 'name': 'test', 'shortcut': 'abbccd', 'purpose': '53'}

        """
        # TODO: current shortcut can be single. I want to support
        # multiple shortcut.
        result = {}
        args = element_args.split(",")
        for arg in args:
            try:
                key, value = arg.split("=")
                result[key] = value
            except ValueError:
                raise InputError, "Bad argument %s" % args

        return result


    def do_listTable(self):
        """
        """
        # We need the name of table to be listed.

        # database name
        if not self.options.arg_database:
            self.options.arg_database = config.dbname
        database_filename = self.options.arg_database

        # table name
        try:
            tablename = self.args[0]
        except IndexError:
            # python emanual.py --list
            # We returns the list of tables
            print "You can use the name of database without db_ prefix."
            print self._listDbTable()
            return

        # Title the name of table
        table_instance = self._dbInstance(tablename)

        db.init(database_filename)
        tableobj = db.ListDb()
        tableobj.printa(table_instance)


    def _listDbTable(self):
        return db.metadata.tables.keys()
    

    def _do_delete_common(self, obj):
        if obj:
            obj.delete()
            db.update()
        else:
            raise NoDataError, "We has no database named %s" % name            


    def _do_delete_element(self, name):
        dbObj = db.Element.get_by(name=name)
        self._do_delete_common(dbObj)


    def _do_delete_group(self, name):
        dbObj = db.Group.get_by(name=name)
        self._do_delete_common(dbObj)


    def do_delete(self):
        name = self.options.arg_name
        gname = self.option.arg_groupname

        if name:
            self._do_delete_element(name)
        else:
            self._do_delete_group(gname)


    def do_deleteShort(self):
        name = self.args[0]
        self._do_delete_element(name)


    def do_createElement(self, value=None):
        if not value: value = self.options.arg_elementargs
        # TODO: What is this function???
        self._arg_zero_required() 

        # {'unit': 'num', 'name': 'test', 'shortcut': 'abbccd', 'purpose':
        # '53'} The value is string. Convert to dictionary that will used
        # by database.
        args_dic = self.ea_parser(value)

        # IntegrityError will be occured when there is no "name" and
        # "purpose" in args_dic. "name" and "purpose" are the required
        # fields of db.Element.
        dbObj = db.Element()
        try:
            dbObj.from_dict(args_dic)
            db.update()
            print "The element \"%s\" is created as\n%s" %(args_dic['name'], str(dbObj.to_dict()))

        except IntegrityError:
            raise InputError, "We requires name and purpose. %" % value

        except FlushError:
            raise InputError, "The name is already exist. %" % value


    def do_createGroup(self, element_names=None, group_name=None):
        """
        @args

        element_names: A list of string. The element is the name of
        db.Element. It will be grouped.

        group_name: A string. Newly created group name
        """
        # From command line the element_names has the form -l
        # element1,element2
        if not element_names:
            # The optparse deals the error if element_names is empty. 
            element_names = self.options.arg_groupargs
            element_names = element_names.split(',')

        if not group_name:
            try: group_name = self.args[0]
            except IndexError:
            # No group_name
                self._output_error("We need group name.\nex) --ga test,test2 test_group2")

        # Create group table
        try:
            dbObj = db.Group(name=group_name)
            db.update()
        except:
            # The name is duplicated.
            sys.stdout.write("\n======== Warnning ==========\n")
            sys.stdout.write("The name of group \"%s\" is already exist.\n" % group_name)
            yorn = query_yes_no(\
                "The \"%s\" column will be replaced by new one if yes.\n" % group_name)
            if yorn == 'yes':
                db.session.rollback()
                self._do_delete_group(group_name)
                dbObj = db.Group(name=group_name)
            else: sys.exit(1)

        # Add data to group table
        for element in element_names:
            try:
                elementObj = db.Element.query.filter_by(name=element).one()
            except:
                # There is no element in Element
                emsg = 'There is no "%s" element.\n See emanual.py -l element' % element
                self._output_error(emsg)
            dbObj.fk_elements.append(elementObj)

        # TODO: error handling
        db.update()


    # TODO: 9 Auto-check of name_type
    def do_schedule(self, name=None, date=None, name_type=None):
        """
        @args

        name: Our target. A string. Either be the name of db.Element or
        the name of db.Group.
        date: the date. A stirng. ex. 20110605 or 2011060505
        name_type: 'group' or 'element'
        """
        # Determine the name to be scheduled.
        if not name:
            if self.options.arg_name:
                name = self.options.arg_name
                name_type = 'element'
            else:
                name = self.options.arg_groupname
                name_type = 'group'

        # Determine the date of the schedule.
        if not date: date = self.args[0]

        if date == 'today':
            dateObj = datetime.date.today()
            timeObj = None
        else:
            try: dateObj, timeObj = toDatetime(date)
            except: self._output_error("Date %s is invalid. It is YYYYMMDD.", date)
                
        if name_type == 'element':
            self._do_schedule_element(name, dateObj, timeObj)
        else:
            self._do_schedule_group(name, dateObj, timeObj)


    def _do_schedule_element(self, name, dateObj, timeObj):
        elementObj = db.Element.get_by(name=name)

        if not elementObj:
            self._output_error("Element name %s is invalid.", name)

        dbObj = db.Schedule(fk_element=elementObj, date=dateObj, time=timeObj)
        db.update()
                            
                            
    def _do_schedule_group(self, name, dateObj, timeObj):
        groupObj = db.Group.get_by(name=name)

        if not groupObj:
            self._output_error("Group name %s is not valid.", name)
            
        dbObj = db.Schedule(fk_group=groupObj, date=dateObj, time=timeObj)
        db.update()
        

    def _do_record_common(self, name, record):
        elementObj = db.Element.get_by(name=name)
        purpose = elementObj.purpose

        def check_miss_typing():
            if purpose < record:
                yorn = query_yes_no("The input %d over the purpose %d.\n Are you sure continue?"\
                                    % (record, purpose))
                if not yorn == 'yes':
                    self._output_error("Miss typing")

        check_miss_typing()
        db.Record(fk_element=elementObj, record=record)
        db.update()


    def do_record(self):
        record = int(self.args[0])
        name = self.options.arg_name
        self._do_record_common(name, record)


    def do_recordShort(self):
        # TODO: error handling
        record = int(self.args[0])
        name = int(self.args[1])
        self._do_record_common(name, record)


    def do_statistic(self):
        pass


class Check:
    def string(self, value):
        pass

    def shortcut(self, value):
        pass


# TODO: create more usefule class
class InputError(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return repr(self.msg)


def initParser(usage=None):
    parser = OptionParser(usage)
    for arg in config.args:
        parser.add_option(*arg[0], **arg[1])

    (options, args) = parser.parse_args()

    # if len(args) != 1:
    #     parser.error("incorrect number of arguments")
    #     if options.verbose:
    #         print "reading %s..." % options.filename

    return (options, args)

def initDatabase():
    db.init(config.dbname)

def main():

    # Create options
    # args is list
    # options is dictionary
    (options, args) = initParser(config.usage)
    # print "options"
    # print options
    # print 'args'
    # print args

    # action = ActionDo(the_action, argv, args)
    # action.do()
    initDatabase()
    action = Action(options, args)
    action.do()


def _test():

    (options, args) = initParser(config.usage)
    print "options"
    print type(options)
    print options
    print 'args'
    print args

    # action = ActionDo(the_action, argv, args)
    # action.do()
    action = Action(options, args)
    action.do()

    import doctest
    doctest.testmod()

if __name__ == "__main__":
    main()
    #_test()


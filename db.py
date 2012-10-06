#!/usr/bin/python
# coding: utf-8

from elixir import *
import datetime
import os
import sys
from library import pprint_table

class Element(Entity):
    name = Field(Unicode, required=True, primary_key=True)
    purpose = Field(Integer, required=True)
    note = Field(Text)
    unit = Field(Unicode(10))
    shortcut = Field(Unicode(10))

    #fk_group = ManyToMany('Group')

    def __repr__(self):
        return '<Element "%s" (%s)>' % (self.name, self.shortcut)


class Group(Entity):
    name = Field(Unicode, required=True, primary_key=True)
    note = Field(Text)

    fk_elements = ManyToMany('Element')

    def __repr__(self):
        return '<Group "%s">' % self.name


class Schedule(Entity):
    # scheduled date
    date = Field(Date, required=True)
    time = Field(Time)

    # schedule -- ManyToOne -- element
    # schedule -- ManyToOne -- group
    fk_element = ManyToOne('Element', colname='fk_element_name', target_column='name')
    fk_group = ManyToOne('Group', colname='fk_group_name', target_column='name')

    
class Record(Entity):
    datetime = Field(DateTime, default=datetime.datetime.now)
    record = Field(Integer, required=True)

    # record -- ManyToOne  -- schedule
    fk_element = ManyToOne('Element', colname='fk_element_name', target_column='name')

    

def update():
    "Let's commit the database."
    session.commit()


def init(filename):
    """The first time after designing database we need to create tables of
    database and initial database file """
    #TODO: Support abpath of sqlname
    sqlname = "sqlite:///" + filename
    metadata.bind = sqlname
    #metadata.bind = "sqlite:///exercise2.sqlite"
    metadata.bind.echo = True
    # Set up database table from designed classes
    setup_all(False)                    # True shows the query
    # Create the database file
    if not os.path.exists(filename):
        create_all()


def bind():
    metadata.bind = "sqlite:///exercise2.sqlite"
    setup_all(True)
    

def columns(cls):
    """
    The function will returns the list of the columns of the cls.
    Such as
    ['id', 'name', 'purpose', 'note', 'fk_unit_id', 'fk_shortcut_id']
    """
    columns = []
    # To obtains the list of columns
    dataobj = cls.table.columns._data
    for a in dataobj:
        columns.append(a)
    return columns


def init_test(create_db=False):
    test_db = "testdb.sqlite"
    if create_db:
        delete_testdb()
    init(test_db)


def delete_testdb():
    os.system('rm testdb.sqlite')
    

# obsolete
def createElement(options):
    # -n, -p (-d) (-s) (--note)
    try:
        Element(name = options.arg_name,
                   purpose = options.arg_purpose,
                   note = options.arg_note,
                   fk_unit = arg_unit,
                   fk_shortcut = arg_shortcut)
        update()
        return 0
    except Exception, err:
        sys.stderr.write('ERROR: %s\n' % str(err))
        return 1

# obsolete    
def deleteElement(options):
    # --delete, -n
    if not options.arg_delete:
        raise RuntimeError('Huk~ Why deleteElement is called. It is critical problem.')

    element = Element.get_by(name=options.arg_name)
    if isinstance(element, Element):
        element.delete()
        update()
        return 0
    else:
        sys.stderr.write('ERROR: We do not have element %s\n' % arg_name)
        return 1

# obsolete
def modifyElement(options):
    # ("-n", "-s")
    element = Element.get_by(name=options.arg_name)
    if isinstance(element, Element):
        element.purpose = options.arg_purpose,
        element.note = options.arg_note,
        element.fk_unit = arg_unit,
        element.fk_shortcut = arg_shortcut

        update
        return 0
    else:
        sys.stderr.write('ERROR: We do not have element %s\n' % arg_name)
        return 1

# def testa(clsstring):
#     return getattr(db, clsstring)


### listing

#TODO: We need error handling and security method
#DONE: more fine output
class ListDb:
    """
    ab = ListDb('element')
    ab.printa()
    will print the database of the table Element.
    """
    def printa(self, cls):
        "Print all database for a table."
        result = []
        #columnObj = cls.table.columns._data
        columns = cls._sa_class_manager.keys()
        # Fixme: we want no output of query.
        queries = cls.query.all()

        result.append(columns)
        # List database
        for query in queries:
            row = []
            for column in columns:
                attr = getattr(query, column)
                value = str(attr)
                row.append(value)
            result.append(row)
        # columns is header and rows is data

        out = sys.stdout
        pprint_table(out, result)

        

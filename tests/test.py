#!/usr/bin/python
# coding: utf-8

import os, sys

from db import *
from emanual import Action

def test_createDb():
    os.system('rm exercise2.sqlite')
    bind()
    create_all()

    # We require to query both metadata.bind and setup_all(True)

    names = [u'name1', u'name2', u'name3', u'name4', u'name5']
    purpose = range(1,5)
    note = "It is note"

    for a in names:
        for p in purpose:
            Element(name=a, purpose=p, note=note)
    update()

def test_print():
    bind()
    elements = Element.query.all()
    for element in elements:
        print "%s, %s, %s, %s\n" % (str(element.id),
                                        element.name,
                                        element.purpose,
                                        element.note)

def test_print(cls=None):
    if cls is None:
        cls = Element
    bind()
    columnobj = cls.table.columns._data
    clss = cls.query.all()
    for cl in clss:
        for column in columnobj:
            fullname = getattr(cl, column)
            sys.stdout.write(str(fullname))
            sys.stdout.write(', ')

        sys.stdout.write("\n")



# vanished
def test_Unit():
    os.system('rm exercise2.sqlite')
    metadata.bind = "sqlite:///exercise2.sqlite"

    setup_all(True)
    create_all()

    print "================================"
    print "========Define Unit=============="
    print "This will error in emacs shell in windows7 See worknote_xp.muse#1010181617"
    print ""
    print "================================"

    value = u'개'
    error_message_in_emacsShell_in_windows7 = \
        "This will error in emacs shell in windows7 See worknote_xp.muse#1010181617"
    try:
        print "The unicode value is encoded with utf-8 %s" % value.encode('utf-8') # failed in emacs shell in windows 7
        print "The value %s" % value                  # both all ok in cmd.exe
    except:
        print error_message_in_emacsShell_in_windows7
    Unit(name=value)
    Unit(name=u'b')

    session.commit()
    units = [unit for unit in session.query(Unit).all()]
    print "The length of Unit is %d" % len(units)
    #print unit.name.encode('utf-8')



# def understand_elixir():
#     import db; db.init_test(create_db=True)
#     e1 = db.Element(name='name1', purpose=40)
#     e2 = db.Element(name='name2', purpose=80)
#     db.update()
#     e3 = db.Element(name='name3', purpose=90)
#     e4 = db.Element(name='name4', purpose=100)
#     db.update()
#     g1 = db.Group(name='gname1')
#     g1.fk_elements.append(e1)
#     g1.fk_elements.append(e2)
#     db.update()
#     db.Group.query.all()
#     q1 = db.Group.query.all()
#     q1a = q1[0]
#     q1a.to_dict()
#     db.Element.query.all()
#     g2 = db.Group(name='gname2')
#     g2.fk_elements.append(e1)
#     g2.fk_elements.append(e2)
#     g2.fk_elements.append(e3)
#     db.update()
#     an = db.Element.query.all()
#     an1 = an[0]
#     print an1.to_dict()
#     ai = db.Group.query.all()
#     ai1 = ai[0]
#     print ai1.to_dict()


class Movie(Entity):
    title = Field(Unicode(30))
    year = Field(Integer)
    description = Field(UnicodeText)
    director = ManyToMany('Director')    # <-- add this line

    def __repr__(self):
        return '<Movie "%s" (%d)>' % (self.title, self.year)


class Director(Entity):
    name = Field(Unicode(60))
    movies = ManyToMany('Movie')         # <-- and this one

    def __repr__(self):
        return '<Director "%s">' % self.name


def init(filename):
    """The first time after designing database we need to create tables of
    database and initial database file """
    #TODO: Support abpath of sqlname
    sqlname = "sqlite:///" + filename
    metadata.bind = sqlname
    #metadata.bind = "sqlite:///exercise2.sqlite"
    metadata.bind.echo = True
    # Set up database table from designed classes
    setup_all(True)
    # Create the database file
    if not os.path.exists(filename):
        create_all()


def init_test(create_db=False):
    test_db = "testdb.sqlite"
    if create_db:
        delete_testdb()
    init(test_db)


def delete_testdb():
    os.system('rm testdb.sqlite')
    

def createdb():
    rscott = Director(name=u"Ridley Scott")
    glucas = Director(name=u"George Lucas")
    alien = Movie(title=u"Alien", year=1979)
    swars = Movie(title=u"Star Wars", year=1977)
    brunner = Movie(title=u"Blade Runner", year=1982)

    rscott.movies.append(brunner) 
    rscott.movies.append(alien)
    glucas.movies.append(brunner)
    glucas.movies.append(alien)
    #swars.director = glucas
    update()

    print "\n\n==listdb(Movie)=="
    listdb(Movie)
    print "\n\n==listdb(Director)=="
    listdb(Director)
    print "\n\n==relation(Director)=="
    relation(Director)

def listdb(cls):

    ab = cls.query.all()
    for a in ab:
        print a.to_dict()

def relation(cls):

    ab = cls.query.all()
    for a in ab:
        print a.movies

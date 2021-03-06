
.. contents:: :local:

PURPOSE
=======

Many hours I play with computer in a day. I think it provides many fats to
body. I need "Fight the Fat". Sometimes I exercise in which the exercise
is not scheduled. I have no information how many I exercising. If I record
the exercise, it provide the information. It simply can be realized with
pen or elisp. I, however, adapt the study purpose.

I need a software tool to know that how many I did. Simply I can note the
count of push-ups, crunches in a day. After a month the tool will report
how many i exercise. eManual helps the recording, statistic and scheduling
for exercises with my desktop.

Another purpose of eManual is to study programming. I need practices to
study programming. eManual is a part of that. So I tried to use more
favorite tools such as extreme programming, patterns, object-oriented
programming, object-relational mapper. I briefly meets that tools.


REQUIREMENTS
============

 - sqlalchemy
 - elixir


FILES
=====

 - emanual.py
 - library.py
 - argument.py
 - config.py
 - db.py
 - test.py
 - utest.py


 - db.mwb : Mysql Workbench file. Used to think database.
 - *.dia : Dia file.
 - *,v : GNU RCS file
 - *.muse : note


USING
=====

Let's assume that I will do exercises in a day.

 - push-ups : 100 count
 - crunches : 100 count
 - running : 1 hour

I did the exercises.

 - 30 push-ups at AM 6
 - 40 crunches at PM 3
 - 50 push-ups at PM 7
 - 1 hour running at PM 10

It will be recorded with eManual2 at that time.
::

 $ python emanual.py --record push 30
 $ python emanual.py --record crunches 40
 $ python emanual.py --record push 50
 $ python emanual.py --record running 60

It has the form
::

 $ python emanual.py --record <TABLE_NAME> <NUMBER>

To record push, crunches and running we must create the tables of database.
To create the tables we use following command.
::

 $ python emanual.py --create --ea name=push,purpose=1000,unit=count
 $ python emanual.py --create --ea name=crunches,purpose=1000,unit=count
 $ python emanual.py --create --ea name=running,purpose=180,unit=min

It has the form
::

 $ python emanual.py --create --ea <name=TABLE_NAME,purpose=NUMBER(,unit=NUMBER,shortcut=SHORTCUT_NAME)

Our tables must have the name and purpose. The name is used to
record/schedule the exercise. The purpose is our goal. Optionally we can
add the shortcut and unit. The shortcut can be used instead of the name.
The unit provides more information for the result report.

The exercise can be scheduled with following command.
::

 $ python emanual.py --schedule -n push 20110505
 $ python emanual.py --schedule -n crunches 20110505
 $ python emanual.py --schedule -n running 20110505

It has the form
::

 $ python emanual.py --schedule -n <TABLE_NAME> <DATE>

The TABLE_NAME is the name of table we created. The DATE is a day/time we
will do somelike 20110505, 2011050503, 201105050330 and today.

We also can group the tables and schedule that.
::

 $ python emanual.py --create --ga push,crunches,running basicExercises
 $ python emanual.py --schedule -g basicExercises 20110505


Current time the reporting facility is not added. It is major feature of
eManual. Instead just use --list to see the database we recorded.
::

 $ python emanual.py --list <TABLE_NAME>

 ex) $ python emanual.py --list push

If you don't remember the table names, use
::

 $ python emanual.py --list

It shows the names of table.


COMMANDS
========

::

 python emanual.py --create --ea name=test,purpose=53,shortcut=tes,unit=num
 
 python emanual.py --create --ga test test_group
 
 python emanual.py --list # to know the element to the group
 
 python emanual.py --list element
 
 python emanual.py --schedule -n test <DATE>
 
 python emanual.py --schedule -g test_group <DATE>
 
 python emanual.py --schedule -n test today
 
 python emanual.py --record -n test 10
 
 python emanual.py --record -s tes 10



TODO
====

 - report the result
 - schedule for week, month
 - more comment for source
 - GUI version


LICENSE
=======

I am not interest what you are do with this source. However, if the file
contains the license which module is not written by me, so follow that
license.



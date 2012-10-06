import sys
from unittest import TestCase
import optparse

sys.path.insert(0, "../")
import db
from emanual import Action




class Test_Action(TestCase):
    @classmethod
    def setUpClass(cls):
        db.init_test(create_db=True)
        options_createElement = {'arg_elementargs' : 'name=test,purpose=53,shortcut=abbccd,unit=num',
                                 'arg_groupargs' : 'gname1,gname2'}
        cls.options = optparse.Values(options_createElement)
        cls.action = Action(cls.options, None)


    @classmethod
    def tearDownClass(cls): pass
    def setUp(self): pass
    def tearDown(self): pass
    
    def test_base(self):
        self.action.do_createElement()
        list_db_table = self.action._listDbTable()
        expected_list_db_table = ['db_element', 'db_group', 'db_record', 'db_group_fk_elements__db_element', 'db_schedule']
        self.assertEqual(list_db_table, expected_list_db_table)

    def test_createGroup(self):
        # do_createGroup(self, element_names=None, group_name=None)
        pass

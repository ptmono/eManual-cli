import unittest

import emanual
import db
from optparse import Values

# assertEqual(integer, result)
# assertRaises(roman.OutOfRangeError, roman.toRoman, 4000)
assertEqual = unittest.TestCase.assertEqual
assertRaises = unittest.TestCase.assertRaises

class TestInput(unittest.TestCase):

    def testCommaSpace(self):
        "name=test,purpose=53,shortcut=[ab,bc,cd], unit=num"
        pass

    def testUnExpectedCharacters(self):
        "name=test,purpose=53,shortcut=[ab,bc,cd].unit=num"
        pass

    def testRequiredElement(self):
        "createElement requires name and purpose"
        pass


def test_createGroup():
    db.init_test(create_db=True)
    options_createElement = {'arg_groupargs': 'ab,bc,cd,ef'}
    options = Values(options_createElement)
    args = ['gname1']
    ab = emanual.Action(options, args)
    ab.do_createGroup()


if __name__ == "__main__":
    #unittest.main()
    test_createGroup()

    

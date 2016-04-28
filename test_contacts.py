import unittest
from voip import app
from contacts import Contacts

ntd = Contacts.name_to_digit

   
"""
test_contacts = {
    'a'   :  '1',
    'd'   : '2',
    'ad'  : '3',
    'da'  : '4',
    'dad' : '5',
    'matt': '66',
    'uuo' : '9',
    'stuart' : '00447949',
    'w'   : '11',
    'arturo': '+341111',
    'matt venn' : '100',
    'AbCdEf' : '100',
    }
"""

class TestMenu(unittest.TestCase):

    def setUp(cls):
        app.config.from_object('config.TestConfiguration')
        cls._contacts = app.config['CONTACTS']

    def test_digit_conv(self):
        self.assertEqual(ntd('matt'), '6288')
        self.assertEqual(ntd('aaa'), '222')
        self.assertEqual(ntd('dad'), '323')
    
    def test_bad_digits(self):
        self.assertEqual(self._contacts.get_options('xx'), [])

    def test_no_digits(self):
        self.assertEqual(len(self._contacts.get_options('')), self._contacts.num_contacts)

    def test_single_options_single_digits(self):
        self.assertEqual(len(self._contacts.get_options(ntd('w'))),1)
        self.assertEqual(self._contacts.get_options(ntd('w'))[0]['number'], '11')

    def test_single_options_multi_digits(self):
        self.assertEqual(len(self._contacts.get_options(ntd('dad'))), 1)
        self.assertEqual(self._contacts.get_options(ntd('dad'))[0]['number'], '5')

        self.assertEqual(len(self._contacts.get_options(ntd('ad'))), 1)
        self.assertEqual(self._contacts.get_options(ntd('ad'))[0]['number'], '3')
      
    
    def test_incomplete_digits(self):
        stu_num = '00447949'
        self.assertEqual(len(self._contacts.get_options(ntd('stu'))), 1)
        self.assertEqual(stu_num, self._contacts.get_options(ntd('stu'))[0]['number'])

        self.assertEqual(len(self._contacts.get_options(ntd('stua'))), 1)
        self.assertEqual(stu_num, self._contacts.get_options(ntd('stua'))[0]['number'])

        self.assertEqual(len(self._contacts.get_options(ntd('stuart'))), 1)
        self.assertEqual(stu_num, self._contacts.get_options(ntd('stuart'))[0]['number'])

    def test_ignore_spaces(self):
        self.assertEqual(len(self._contacts.get_options(ntd('matt'))), 2)
        self.assertEqual(len(self._contacts.get_options(ntd('mattv'))), 1)

    def test_ignore_case(self):
        self.assertEqual(len(self._contacts.get_options(ntd('abcdef'))), 1)

if __name__ == '__main__':
    unittest.main()

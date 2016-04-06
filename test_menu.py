import unittest
from alt_menu import Menu, numbers

def ntd(name):
    digits = ''
    for l in name:
        for g, digit in zip(numbers, range(len(numbers))):
            if l in g:
                digits += str(digit)
    return digits
   
test_contacts = {
    'a'   : '1',
    'd'   : '2',
    'ad'  : '3',
    'da'  : '4',
    'dad' : '5',
    'matt': '66',
    'uuo' : '9',
    'stuart' : '+447949',
    'w'   : '11',
    'arturo': '+341111',
    'matt venn' : '100',
    'AbCdEf' : '100',
    }

class TestMenu(unittest.TestCase):
    """
    @classmethod
    def setupClass(cls):
        from control import Control
        cls._robot = Control(PORT)
    """

    def test_digit_conv(self):
        self.assertEqual(ntd('matt'), '6288')
        self.assertEqual(ntd('aaa'), '222')
        self.assertEqual(ntd('dad'), '323')
    
    def test_init(self):
        m = Menu(test_contacts)

    def test_bad_digits(self):
        m = Menu(test_contacts)
        self.assertEqual(m.get_options('xx'), [])

    def test_no_digits(self):
        m = Menu(test_contacts)
        assert len(m.get_options('')) == len(test_contacts)

    def test_single_options_single_digits(self):
        m = Menu(test_contacts)
        assert len(m.get_options(ntd('w'))) == 1
        assert m.get_options(ntd('w'))[0]['number'] == test_contacts['w']

    def test_single_options_multi_digits(self):
        m = Menu(test_contacts)

        for name in ['dad', 'ad']:
            self.assertEqual(len(m.get_options(ntd(name))), 1)
            self.assertEqual(test_contacts[name], m.get_options(ntd(name))[0]['number'])
      
    
    def test_incomplete_digits(self):
        m = Menu(test_contacts)
        self.assertEqual(len(m.get_options(ntd('stu'))), 1)
        self.assertEqual(test_contacts['stuart'], m.get_options(ntd('stu'))[0]['number'])

        self.assertEqual(len(m.get_options(ntd('stua'))), 1)
        self.assertEqual(test_contacts['stuart'], m.get_options(ntd('stua'))[0]['number'])

        self.assertEqual(len(m.get_options(ntd('stuart'))), 1)
        self.assertEqual(test_contacts['stuart'], m.get_options(ntd('stuart'))[0]['number'])

    def test_ignore_spaces(self):
        m = Menu(test_contacts)
        self.assertEqual(len(m.get_options(ntd('matt'))), 2)
        self.assertEqual(len(m.get_options(ntd('mattv'))), 1)

    def test_ignore_case(self):
        m = Menu(test_contacts)
        self.assertEqual(len(m.get_options(ntd('abcdef'))), 1)

if __name__ == '__main__':
    unittest.main()

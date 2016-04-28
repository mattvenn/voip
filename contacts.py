"""
need to pre process stupid nokia 108 export first:
    dos2unix backup.dat

then replace all split name lines:
    :%s/=\n//
"""
import os
import vobject
import logging
log = logging.getLogger(__name__)

numbers = [ '', '', 'abc', 'def', 'ghi', 'jkl', 'mno', 'pqrs', 'tuv', 'wxyz' ]

class Contacts():
    def __init__(self, filename, verbose=False, *args):
        self.contacts = {}
        self.num_contacts = 0
        self.filename = filename
        self.verbose = verbose
        self.parse()

    @staticmethod
    def format_number(num):
        if num.startswith('00'):
            return num
        elif num.startswith('+'):
            return '00' + num.lstrip('+')
        elif num.startswith('0'):
            return '0044' + num.lstrip('0')
        elif num.startswith('6'):
            return '0034' + num
        return num

    @staticmethod
    def detect_country(num):
        if num.startswith('0044'):
            return 'UK'
        elif num.startswith('0034'):
            return 'ES'
        else:
            return None

    @staticmethod
    def get_mp3(name):
        if os.path.exists('static/' + name + '.mp3'):
            return name + '.mp3'
        return None

    @staticmethod
    def name_to_digit(name):
        digits = ''
        for l in name.lower():
            for g, digit in zip(numbers, range(len(numbers))):
                if l in g:
                    digits += str(digit)
        return digits

    def parse(self):
        for file in os.listdir(self.filename):
            if file.endswith(".vcf"):
                with open(self.filename + '/' + file) as vcf:
                    self.num_contacts += 1
                    v = vobject.readOne( vcf )
                    name = v.n.value.given
                    number = Contacts.format_number(v.tel.value)
                    country = Contacts.detect_country(number)
                    mp3 = Contacts.get_mp3(name)
                    code = Contacts.name_to_digit(name) 

                    if self.contacts.has_key(code):
                        logging.warn("contact clash: %s with %s" % (name, self.contacts[code]['name']))

                    self.contacts[code] = { 'name' : name, 'number' : number, 'mp3' : mp3, 'country' : country }
                    if self.verbose:
                        print(name, number, mp3, country)
        log.info("read %d contacts" % self.num_contacts)

    def get_options(self, digits):
        options = []
        for key in self.contacts:
            if key.startswith(digits):
                options.append(self.contacts[key])
        return options

    def find_by_number(self, number):
        number = Contacts.format_number(number)
        for code in self.contacts.keys():
            if self.contacts[code]['number'] == number:
                return self.contacts[code]


if __name__ == '__main__':
    contacts = Contacts('contacts', verbose=True)
    print(contacts.get_options(Contacts.name_to_digit('Ben Todd')))


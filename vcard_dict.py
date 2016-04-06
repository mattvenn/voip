"""
need to pre process stupid nokia 108 export first:
    dos2unix backup.dat

then replace all split name lines:
    :%s/=\n//
"""
import os
import vobject
import logging
log = logging.getLogger('contacts')

class Vcard_Dict(dict):
    def __init__(self, filename, verbose=False, *args):
        dict.__init__(self, *args)
        self.filename = filename
        self.verbose = verbose
        self.parse()

    def add_country_code(self, num):
        if num.startswith('00'):
            return num
        elif num.startswith('+'):
            return '00' + num.lstrip('+')
        elif num.startswith('0'):
            return '0044' + num.lstrip('0')
        elif num.startswith('6'):
            return '0034' + num
        return num

    def parse(self):
        contacts = 0
        for file in os.listdir(self.filename):
            if file.endswith(".vcf"):
                with open(self.filename + '/' + file) as vcf:
                    contacts += 1
                    v = vobject.readOne( vcf )
                    v.tel.value = self.add_country_code(v.tel.value)
                    self[v.n.value.given] = v.tel.value
                    if self.verbose:
                        print(v.n.value.given, v.tel.value)
        log.info("read %d contacts" % contacts)

if __name__ == '__main__':
    contacts = Vcard_Dict('contacts', verbose=True)
    print(contacts['Ben Todd'])


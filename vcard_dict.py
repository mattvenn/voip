class Vcard_Dict(dict):
    def __init__(self, filename, verbose=False, *args):
        dict.__init__(self, *args)
        self.filename = filename
        self.verbose = verbose
        self.parse()

    def strip(self, word):
        word = word.replace(';', ' ')
        word = word.replace('  ', ' ')
        word = word.replace('-', '')
        word = word.lower()
        return word

    def add_country_code(self, num):
        if num.startswith('00'):
            return num
        elif num.startswith('0'):
            return '0044' + num.lstrip('0')
        elif num.startswith('64'):
            return '0034' + num
        return num

    def parse(self):
        with open(self.filename) as vcf:
            start = None
            name = None
            number = None

            for line in vcf.readlines():
                line = line.strip()
                if line == 'BEGIN:VCARD':
                    start = True
                elif line.startswith("N:"):
                    name = line.replace('N:','')
                    name = self.strip(name)
                elif line.startswith("TEL:"):
                    number = line.replace('TEL:','')
                    number = self.strip(number)
                    number = self.add_country_code(number)
                    self[name] = number
                    if self.verbose:
                        print(name, number)

if __name__ == '__main__':
    contacts = Vcard_Dict('backup.dat', verbose=True)


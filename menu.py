import logging
numbers = [ '', '', 'abc', 'def', 'ghi', 'jkl', 'mno', 'pqrs', 'tuv', 'wxyz' ]
log = logging.getLogger('')

class Menu():

    def __init__(self, contacts):
        self.pre_process(contacts)

    def ntd(self, name):
        digits = ''
        for l in name.lower():
            for g, digit in zip(numbers, range(len(numbers))):
                if l in g:
                    digits += str(digit)
        return digits

    def pre_process(self, contacts):
        self.codes = {}
        for contact in contacts.keys():
            code = self.ntd(contact)
            # warn crash
            if self.codes.has_key(code):
                logging.warn("contact clash: %s with %s" % (contact, self.codes[code]['name']))
            self.codes[code] = { 'name' : contact,
                'number' : contacts[contact],
                }
            
  
    def get_options(self, digits):
        options = []
        for key in self.codes:
            if key.startswith(digits):
                options.append(self.codes[key])
        return options


numbers = [ '', '', 'abc', 'def', 'ghi', 'jkl', 'mno', 'pqrs', 'tuv', 'wxyz' ]

class Menu():

    def __init__(self, contacts):
        self.contacts = contacts
  
    def get_options(self, digits):
        all_combos = self.recurse_combos(digits)
        combos = []
        # filter out everything that doesn't have the right length
        for c in all_combos:
            if len(c) == len(digits):
                combos.append(c)
                
        # filter out anything that doesn't start with a name in the dictionary
        options = []
        for c in combos:
            for name in self.contacts.keys():
                strip_name = name.replace(' ','')
                if strip_name.startswith(c):
                    options.append({'name' : name, 'number': self.contacts[name]})

        return options 


    """
    1  : a,b,c
    11 : aa,ab,ac,ba,bb,bc,ca,cb,cc
    111: aaa,aab,aac,aba,abb,abc,aca,acb,acc.....
    """
    def recurse_combos(self, digits, index=0, combos=[]):
        # base case
        if index == len(digits):
            return combos

        assert digits[index].isdigit()
        digit = int(digits[index])
        group = numbers[digit]

        new_combos = [g for g in group]

        for c in combos:
            for l in group:
                new_combos.append( c + l )

        return self.recurse_combos(digits, index + 1, new_combos)

        


from contacts import Contacts

class BaseConfiguration(object):
    DEBUG = False
    TESTING = False
    CONTACTS = Contacts('contacts')

class TestConfiguration(BaseConfiguration):
    from vcard_dict import Vcard_Dict
    TESTING = True
    WTF_CSRF_ENABLED = False
    CONTACTS = Contacts('test_contacts')

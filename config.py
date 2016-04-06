from menu import Menu

class BaseConfiguration(object):
    from vcard_dict import Vcard_Dict
    DEBUG = False
    TESTING = False
    contacts = Vcard_Dict('contacts')
    MENU = Menu(contacts)

class TestConfiguration(BaseConfiguration):
    from test_menu import test_contacts as contacts
    TESTING = True
    WTF_CSRF_ENABLED = False
    MENU = Menu(contacts)

from voip import app
import unittest
from xml.etree import ElementTree
import os
from test_menu import ntd
from secrets import http_user, http_pass
from secrets import nums
import logging
import base64

log = logging.getLogger('')
log.setLevel(logging.INFO)


class TestVOIP(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        app.config.from_object('config.TestConfiguration')

    # request handler for basic auth
    def request(self, method, url, auth=None, **kwargs):
        headers = kwargs.get('headers', {})
        if auth:
            headers['Authorization'] = 'Basic ' + base64.b64encode(auth[0] + ':' + auth[1])

        kwargs['headers'] = headers

        return self.app.open(url, method=method, **kwargs)

    def test_dial_noauth(self):
        response = self.app.post('/dial', data={'Digits':
            '+15556667777'})
        self.assertEquals(response.status, "401 UNAUTHORIZED")

    def test_dial_uk(self):
        response = self.request('POST', '/dial', data={'Digits':
            '004415556667777'}, auth=(http_user, http_pass))
        self.assertEquals(response.status, "200 OK")

        root = ElementTree.fromstring(response.data)
        elems = root.findall('Dial')
        self.assertEquals(len(elems), 1)
        self.assertEquals(elems[0].get('callerId'), nums['uk_twilio'])

    def test_dial_es(self):
        response = self.request('POST', '/dial', data={'Digits':
            '00361111'}, auth=(http_user, http_pass))
        self.assertEquals(response.status, "200 OK")

        root = ElementTree.fromstring(response.data)
        elems = root.findall('Dial')
        self.assertEquals(len(elems), 1)
        self.assertEquals(elems[0].get('callerId'), nums['es_twilio'])

    def test_dial(self):
        response = self.request('POST', '/dial', data={'Digits':
            '+15556667777'}, auth=(http_user, http_pass))

        self.assertEquals(response.status, "200 OK")

        root = ElementTree.fromstring(response.data)

        self.assertEquals(root.tag, 'Response')

        elems = root.findall('Dial')
        self.assertEquals(len(elems), 1)

        elems = root.findall('Say')
        self.assertEquals(len(elems), 2)

    def test_menu_phonebook_noauth(self):
        response = self.app.post('/menu', data={'Digits': '1'})
        self.assertEquals(response.status, "401 UNAUTHORIZED")

    def test_menu_phonebook(self):
        response = self.request('POST', '/menu', data={'Digits': '1'},
            auth=(http_user, http_pass))

        self.assertEquals(response.status, "200 OK")
        root = ElementTree.fromstring(response.data)
        self.assertEquals(root.tag, 'Response')

        elems = root.findall('Gather')
        self.assertEquals(len(elems), 1)

        elems = elems[0].findall('Say')
        self.assertEquals(len(elems), 1)
        self.assertIn('phonebook', elems[0].text)

    def test_menu_dial_noauth(self):
        response = self.app.post('/menu', data={'Digits': '2'})
        self.assertEquals(response.status, "401 UNAUTHORIZED")

    def test_menu_dial(self):
        response = self.request('POST', '/menu', data={'Digits': '2'},
            auth=(http_user, http_pass))

        self.assertEquals(response.status, "200 OK")
        root = ElementTree.fromstring(response.data)
        self.assertEquals(root.tag, 'Response')

        elems = root.findall('Gather')
        self.assertEquals(len(elems), 1)

        elems = elems[0].findall('Say')
        self.assertEquals(len(elems), 1)
        self.assertIn('dial', elems[0].text)

    def test_menu_bad(self):
        response = self.request('POST', '/menu', data={'Digits': '9'},
            auth=(http_user, http_pass))

        self.assertEquals(response.status, "302 FOUND")

    def test_single_phonebook_uk(self):
        response = self.request('POST', '/phonebook', data={'Digits': ntd('stu')}, auth=(http_user, http_pass))
        self.assertEquals(response.status, "200 OK")
        root = ElementTree.fromstring(response.data)
        self.assertEquals(root.tag, 'Response')

        elems = root.findall('Say')
        self.assertEquals(len(elems), 1)

        self.assertIn('calling Stuart Childs', elems[0].text)
        elems = root.findall('Dial')
        self.assertEquals(len(elems), 1)
        self.assertEquals(elems[0].get('callerId'), nums['uk_twilio'])

    def test_single_phonebook_es(self):
        response = self.request('POST', '/phonebook', data={'Digits': ntd('artu')}, auth=(http_user, http_pass))
        self.assertEquals(response.status, "200 OK")
        root = ElementTree.fromstring(response.data)
        self.assertEquals(root.tag, 'Response')

        elems = root.findall('Say')
        self.assertEquals(len(elems), 1)

        self.assertIn('calling arturo', elems[0].text)
        elems = root.findall('Dial')
        self.assertEquals(len(elems), 1)
        self.assertEquals(elems[0].get('callerId'), nums['es_twilio'])

    def test_no_phonebook(self):
        response = self.request('POST', '/phonebook', data={'Digits': ntd('xxx')}, auth=(http_user, http_pass))
        self.assertEquals(response.status, "200 OK")
        root = ElementTree.fromstring(response.data)
        self.assertEquals(root.tag, 'Response')

        elems = root.findall('Say')
        self.assertEquals(len(elems), 1)

        self.assertIn('no numbers found', elems[0].text)

        # check menu starts again
        elems = root.findall('Gather')
        self.assertEquals(len(elems), 1)

        elems = elems[0].findall('Say')
        self.assertEquals(len(elems), 1)
        self.assertIn('phonebook', elems[0].text)

    def test_too_many_phonebook(self):
        response = self.request('POST', '/phonebook', data={'Digits': ntd('a')}, auth=(http_user, http_pass))

        self.assertEquals(response.status, "200 OK")
        root = ElementTree.fromstring(response.data)
        self.assertEquals(root.tag, 'Response')

        elems = root.findall('Say')
        self.assertEquals(len(elems), 1)

        self.assertIn('more than 1 number found', elems[0].text)

        # check menu starts again
        elems = root.findall('Gather')
        self.assertEquals(len(elems), 1)

        elems = elems[0].findall('Say')
        self.assertEquals(len(elems), 1)
        self.assertIn('phonebook', elems[0].text)

    def test_start_noauth(self):
        response = self.app.post('/caller', data={'From': nums['es_mobile'], 'To': nums['es_twilio']})
        self.assertEquals(response.status, "401 UNAUTHORIZED")

    def test_start_from_me(self):
        response = self.request('POST', '/caller', data={'From': nums['es_mobile'], 'To': nums['es_twilio']}, auth=(http_user, http_pass))

        self.assertEquals(response.status, "200 OK")
        root = ElementTree.fromstring(response.data)
        self.assertEquals(root.tag, 'Response')

    def test_from_unknown_to_es(self):
        response = self.request('POST','/caller', data={'From': 11111, 'To': nums['es_twilio']}, auth=(http_user,http_pass))

        self.assertEquals(response.status, "200 OK")
        root = ElementTree.fromstring(response.data)
        self.assertEquals(root.tag, 'Response')

        elems = root.findall('Play')
        self.assertEquals(len(elems), 1)

        self.assertIn('ES.mp3', elems[0].text)

        elems = root.findall('Dial')
        self.assertEquals(len(elems), 1)

        self.assertIn(nums['uk_mobile'], elems[0].text)

    def test_from_stuart_to_es(self):
        response = self.request('POST','/caller', data={'From': '+447949', 'To': nums['es_twilio']}, auth=(http_user,http_pass))

        root = ElementTree.fromstring(response.data)

        elems = root.findall('Play')
        self.assertEquals(len(elems), 1)

        self.assertIn('Stuart%20Childs.mp3', elems[0].text)

    def test_from_unknown_to_uk(self):
        response = self.request('POST','/caller', data={'From': 11111, 'To': nums['uk_twilio']}, auth=(http_user,http_pass))

        self.assertEquals(response.status, "200 OK")
        root = ElementTree.fromstring(response.data)
        self.assertEquals(root.tag, 'Response')

        elems = root.findall('Play')
        self.assertEquals(len(elems), 1)

        self.assertIn('UK.mp3', elems[0].text)

        elems = root.findall('Dial')
        self.assertEquals(len(elems), 1)

        self.assertIn(nums['es_mobile'], elems[0].text)

if __name__ == '__main__':
    unittest.main()

from flask import Flask, request, redirect, abort, url_for, render_template
import twilio.twiml
from twilio.rest import TwilioRestClient
import logging, time, socket
from menu import Menu
import os
from http_auth import requires_auth
from secrets import nums
from vcard_dict import Vcard_Dict

log = logging.getLogger()
app = Flask(__name__)

"""
# this doesn't work because the test program can't set it
# so has to be set on the command line
TEST_MODE = os.environ.get("TEST_MODE", None)
if not TEST_MODE:
    contacts = Vcard_Dict('contacts')
else:
    from test_menu import test_contacts as contacts
"""

@app.route("/")
@requires_auth
def index():
    return render_template('index.html')

@app.route("/logs")
@requires_auth
def logs():
    # do seek
    with open('voip.log') as log:
        log_lines = log.readlines()
    log_lines = log_lines[-20:]
    return render_template('logs.html', log_lines=log_lines)

@app.route("/phonebook", methods=['GET', 'POST'])
@requires_auth
def phonebook():
    response = twilio.twiml.Response()
    digits = request.values.get('Digits', None)
    if digits is None:
        log.info("no keys pressed")
        response.say("no keys pressed")
        # start phonebook menu again
        get_phonebook_twiml(response)
        return str(response)

    options = app.config['MENU'].get_options(digits)

    if len(options) == 0:
        log.info("no numbers found")
        response.say("no numbers found")
        # start phonebook menu again
        get_phonebook_twiml(response)

    elif len(options) == 1:
        response.say("calling " + options[0]['name'])

        # set callerId depending on target country
        if options[0]['number'].startswith('0044'):
            from_number = nums['uk_twilio']
        else:
            from_number = nums['es_twilio']

        log.info("calling %s [%s] from %s" % (options[0]['number'], options[0]['name'], from_number))
        response.dial(options[0]['number'], callerId=from_number)

    else:
        log.info("%d numbers found for code %s" % (len(options), digits))
        response.say("more than 1 number found")
        # start phonebook menu again
        get_phonebook_twiml(response)

    return str(response)
        
@app.route("/dial", methods=['GET', 'POST'])
@requires_auth
def dial():
    response = twilio.twiml.Response()
    digits = request.values.get('Digits', None)

    # set callerId depending on target country
    if digits.startswith('0044'):
        from_number = nums['uk_twilio']
    else:
        from_number = nums['es_twilio']

    log.info("dialing %s from %s" % (digits, from_number))
    response.say("calling")
    response.dial(digits, callerId=from_number)
    response.say("The call failed")
    return str(response)


def get_phonebook_twiml(response):
    log.info("phonebook")
    with response.gather(finishOnKey='*', action="/phonebook", method="POST") as g:
        g.say("phonebook, type name and * to finish")

@app.route("/menu", methods=['GET', 'POST'])
@requires_auth
def menu():
    response = twilio.twiml.Response()

    # Get the digit pressed by the user
    digit_pressed = request.values.get('Digits', None)
    if digit_pressed == "1":
        # phone book
        get_phonebook_twiml(response)
        return str(response)
 
    # dial a number
    elif digit_pressed == "2":
        log.info("dial")
        with response.gather(finishOnKey='*', action="/dial", method="POST") as g:
            g.say("dial number, press * to finish")
        return str(response)

    else:
        log.info("bad menu option")
        return redirect("/")

@app.route("/caller", methods=['GET', 'POST'])
@requires_auth
def forward():
    from_number = request.values.get('From', None) 
    to_number = request.values.get('To', None) 
    log.info("got call from [%s] to [%s]" % (from_number, to_number))

    response = twilio.twiml.Response()

    # allow from either mobile numbers
    if from_number == nums['uk_mobile'] or from_number == nums['es_mobile']:
        with response.gather(numDigits=1, action="/menu", method="POST") as g:
            g.say("phonebook press 1, dial press 2")
 
        return str(response)
    
    else:
        # play message in correct language
        if to_number == nums['es_twilio']:
            my_number = nums['uk_mobile']
            mp3_file = 'ES.mp3'
        else:
            my_number = nums['es_mobile']
            mp3_file = 'UK.mp3'

        response.play(url_for('static', filename=mp3_file))

        # dial my number
        response.dial(my_number)

        # if the dial fails TODO message
        response.say("The call failed")
        return str(response)

if __name__ == "__main__":

    # create console handler and set level to info
    log_format = logging.Formatter('%(asctime)s - %(levelname)-8s - %(message)s')
    ch = logging.StreamHandler()
    ch.setFormatter(log_format)
    log.addHandler(ch)

    app.config.from_object('config.BaseConfiguration')

    hostname = socket.gethostname()
    if hostname == 'mattsmac':
        debug = True
        log.setLevel(logging.DEBUG)
    else:
        debug = False
        log.setLevel(logging.INFO)

    app.run('0.0.0.0',40000)
    log.info("stopping")

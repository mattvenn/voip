# Matt's VOIP

Provides VOIP services for people calling me, and for me calling people.

Symmetric service where a call to the UK Twilio number will call my ES mobile
and vice versa.

Requires Twilio UK & ES landline numbers.

# Spec

## Voice from Matt

Services to include:

* Menu to select a number to call from the phonebook
* Option to type a number that is then called

## Text from Matt

Services to include:

* Switch between ES & UK mobiles for when I'm back in the UK.
* Dictionary lookup, translation services, callbacks etc.

## Voice from unknown number

Play a brief message 'Matt is currently in X and this number will redirect you
free of charge to his X number' and then redirect to Matt's mobile.

## Text

Redirect to Matt's mobile.

# Todo

* caller id is right for the country call recieved in

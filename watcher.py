"""
This script watches for an available covid-19 vaccine appointment and sends an email if one is found
@author: Parker Clayon
"""
# pylint: disable=wrong-import-order
import argparse
from dateutil import parser, datetime
from gmail import MailClient, generate_gmail_token
import json
import os
import requests
import time

last_updated = None
BASE_URL = 'https://am-i-eligible.covid19vaccine.health.ny.gov/api/'
REQ_HEADERS = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
PROVIDER = 'Javits Center'
POLLING_INTERVAL = 3    # seconds

def main_loop(args):

    if args.init:
        if generate_gmail_token():
            print('Success. Now run watcher.py without the --init flag')
        else:
            print('ERROR - unable to get gmail token.pickle file')
        return

    # Check that we have everything we need
    if not os.path.exists('token.pickle'):
        print('ERROR - Missing gmail token file "token.pickle". please run with --init flag')
        return
    if not os.path.exists('messages.json'):
        print('ERROR - Missing messages.json')
        return
    
    with open('messages.json', 'r') as f:
        emails = json.load(f)
    if (len(emails) == 1 and emails[0]['from'] == 'youremail@gmail.com'):
        print('ERROR - please update emails json template')
        return

    mail_client = MailClient()
    global last_updated
        
    while True:
        global last_updated
        response = requests.get(BASE_URL + 'list-providers', headers=REQ_HEADERS).json()
        print('   Polling: {} | lastupdated: {}'.format(datetime.now().strftime("%H:%M:%S"), last_updated), end='\r')
        if not last_updated:
            last_updated = response['lastUpdated']
            if appointment_available(PROVIDER, response):
                print('Appointment Available!!')
                mail_client.send_multiple_emails(emails)
                break

        if response['lastUpdated'] != last_updated:
            last_updated = response['lastUpdated']

        if appointment_available(PROVIDER, response):
            print('Appointment Available!!')
            mail_client.send_multiple_emails(emails)
            break

        time.sleep(POLLING_INTERVAL)

def appointment_available(providerName, status):
    """
    Checks if an appointment is available from a given provider
    Args:
            providerName (str): name of a provider
            Status response from: https://am-i-eligible.covid19vaccine.health.ny.gov/api/list-providers
        Returns:
            True or False
    """
    for provider in status['providerList']:
        if provider.get('providerName') == providerName:
            if provider.get('availableAppointments') != 'NAC':
                return True
    return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--init", help="Used to generate gmail token", action='store_true')
    args = parser.parse_args()
    main_loop(args)

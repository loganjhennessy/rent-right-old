'''rentscraper.zipcoderequest
'''
import os
import requests

class ZipCodeRequest(object):

    def __init__(self, city, state):
        self.apikey = os.environ['ZIP_KEY']
        self.base = (
            'https://www.zipcodeapi.com/rest/{}/city-zips.{}/{}/{}'
        )
        self.city = city
        self.form = 'json'
        self.state = state

    def execute(self):
        url = self.base.format(
            self.apikey,
            self.form,
            self.city,
            self.state
        )
        resp = requests.get(url)
        return resp.json()['zip_codes']

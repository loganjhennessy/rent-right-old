"""rentscraper.zipcoderequest"""
import os
import requests

class ZipCodeRequest(object):
    """Allows for encapsulated configuration and use of Zip Code API.

    Attributes:
        apikey: str containing Zip Code API key
        base: str containing base URL of Zip Code ZPI
        city: str of city to search for zips
        form: str indicating format of return from API
        state: str of state to search for zips
    """

    def __init__(self, city, state):
        """Inits ZipCodeRequest with city and state.

        apikey is set to value of ZIP_KEY environment variable
        base is hardcoded to Zip Code API URL
        form is hardcoded to 'json'
        """
        self.apikey = os.environ['ZIP_KEY']
        self.base = (
            'https://www.zipcodeapi.com/rest/{}/city-zips.{}/{}/{}'
        )
        self.city = city
        self.form = 'json'
        self.state = state

    def execute(self):
        """Uses attributes to make a Zip Code API query.

        Formats base (url) attribute with all required parameters to make a
        valid request.

        Returns
            zipcodes: a list of zipcodes returned fro the API
        """
        url = self.base.format(
            self.apikey,
            self.form,
            self.city,
            self.state
        )
        resp = requests.get(url)
        return resp.json()['zip_codes']

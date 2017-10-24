"""rentright.scraper.zipcoderequest"""
import os
import requests

from rentright.utils.log import get_configured_logger

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
        self.logger = get_configured_logger('DEBUG', __name__)
        self.state = state

        self.logger.info('ZipCodeRequest initialized')

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

        try:
            resp = requests.get(url)
        except Exception as e:
            self.logger.info('Caught exception')
            self.logger.info('{}'.format(e))

        return resp.json()['zip_codes']

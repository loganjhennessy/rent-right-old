"""rentscraper.listing"""

from bs4 import BeautifulSoup
from unit import Unit

class Listing(object):

    def __init__(self, content):
        self.content = content
        self.soup = BeautifulSoup(self.content)
        self.unit = Unit()

    def clean(self):
        self._attributes()
        self._imagemeta()
        self._price()
        self._sizeinfo()

    def _attributes(self):
        pass

    def _imagemeta(self):
        pass

    def _price(self):
        self.unit['price'] = self.soup.select('.price')[0].text

    def _sizeinfo(self):
        pass

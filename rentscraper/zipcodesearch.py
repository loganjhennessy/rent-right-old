'''rentscraper.zipcodesearch
'''
import requests

from bs4 import BeautifulSoup

class ZipCodeSearch(object):

    def __init__(self, city, zipcode):
        self.base = 'https://{}.craigslist.org/search/apa'
        self.city = city.lower()
        self.zipcode = zipcode

    def execute(self):
        results = []
        content = self._search()
        results.append(content)

        count = self._countresults(content)

        # iterate through results until all results are retrieved
        for s in range(120, int(count), 120):
            content = self._search(str(s))
            listings = self._parseresults(content)
            self._writetomongo(listings)

    def _countresults(self, content):
        '''return number of results found in content'''
        soup = BeautifulSoup(content)
        count = soup.select('.totalcount').text
        return count

    def _parseresults(self, content):
        listings = []
        soup = BeautifulSoup(content)
        resulttitles = soup.select('.result-title.hdrlnk')
        for title in resulttitles:
            listing = {
                'link': title.attrs['href'],
                'title': title.text,
                'zipcode': self.zipcode
            }
            listings.append(listing)
        return listings

    def _search(self, s=None):
        '''get a page of search results'''
        url = self.base.format(city)
        params = {
            'postal': self.zipcode
        }
        if s:
            params['s'] = s
        resp = requests.get(base.format(), params)
        return resp.content

    def _writetomongo(self):

        pass

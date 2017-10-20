"""rentscraper.listing"""

from log import get_configured_logger

from bs4 import BeautifulSoup
from unit import Unit

class Listing(object):
    """Implements a Listing.

    A listing contains the raw HTML contents of a listing and the associated
    methods required to clean the contents and get usable features.

    Attributes:
        attrset: set of attributes encountered in this listing
        content: str of raw HTML content of the listing
        soup: BeautifulSoup object of content parsed using 'html.parser'
        unit: Unit object for content
    """

    def __init__(self, content, listing_id):
        """Inits a Listing with the raw HTML content."""
        self.attrset = set()
        self.content = content
        self.listing_id = listing_id
        self.logger = get_configured_logger('DEBUG', __name__)
        self.soup = BeautifulSoup(self.content, 'html.parser')
        self.unit = Unit(listing_id)

    def clean(self):
        """Executes the cleaning of a listing."""
        self._attrgroups()
        self._description()
        self._location()
        self._imagemeta()
        self._price()
        self._title()

    def getattrs(self):
        """Returns the set of attributes encountered in this listing.

        Returns:
            attrset: set of attributes encountered in this listing
        """
        return self.attrset

    def isremoved(self):
        """Indicates whether or not this post has been removed.

        Returns:
            bool: True if the post has been removed.
        """
        removed_by_author_text = 'This posting has been deleted by its author.'
        removed_by_author_tags = self.soup.findAll('div', {'class': 'removed'})
        for tag in removed_by_author_tags:
            if removed_by_author_text in tag.text:
                return True

        not_found_text = ('The post has expired, ' 
                          'or the post ID in the URL is invalid.')
        not_found_tags = self.soup.findAll('div', {'class': 'post-not-found'})
        for tag in not_found_tags:
            if not_found_text in tag.text:
                return True

        return False

    def _attrgroups(self):
        """Parses all attributes with the 'attrgroup' class.

        This includes both the housing info (beds, baths, sqft) and the boolean
        attributes describing the unit (W/D in unit, etc).
        """
        attrgroups = self.soup.findAll('p', {'class': 'attrgroup'})
        for attrgroup in attrgroups:
            bubbles = attrgroup.findAll('span', {'class': 'shared-line-bubbles'})
            if bubbles:
                for bubble in bubbles:
                    if _isrooms(bubble):
                        self._parserooms(bubble)
                    elif _issqft(bubble):
                        self._parsesqft(bubble)
            else:
                self._parseattrs(attrgroup)
        #
        # housinginfo = attrgrouptags[0]
        # self._parsehousinginfo(housinginfo)
        # attrinfo = attrgrouptags[1]
        # self._parseattrinfo(attrinfo)

    def _description(self):
        """Parses the text contained in the listing description."""
        description = self.soup.find('section', {'id': 'postingbody'}).text
        self.unit['description'] = description

    def _imagemeta(self):
        """Parses the meta data of the images."""
        num_images = 0
        if self.soup.find('span', {'class': 'slider-info'}):
            imageinfostr = self.soup.select('.slider-info')[0].text
            num_images = imageinfostr.split()[-1]

        self.unit['num_images'] = int(num_images)

    def _isrooms(self, bubble):
        """Determines whether or not a 'shared-line-bubble' tag contains rooms.

        Arguments:
            bubble: a bs4.Tag containing a 'shared-line-bubble' class

        Returns:
            str: 'BR', 'Ba', 'BRBa' or None (if tag does not contain rooms)
        """
        out = ''
        if 'BR' in bubble.text:
            out += 'BR'
        if 'Ba' in bubble.text:
            out += 'Ba'
        if not out:
            return None
        else:
            return out

    def _issqft(self, bubble):
        """Determines whether or not a 'shared-line-bubble' tag contains sqft.

        Arguments:
            bubble: a bs4.Tag containing a 'shared-line-bubble' class

        Returns:
            bool: True if tag contains sqft
        """
        if 'ft' in bubble.text:
            return True
        return False

    def _location(self):
        """Parses the location information from the listing content."""
        maptag = self.soup.find('div', {'id': 'map'})
        self.unit['latitude'] = maptag.attrs['data-latitude']
        self.unit['longitude'] = maptag.attrs['data-longitude']

    def _parseattrs(self, attrgroup):
        """Parses the boolean attributes about the listing.

        Sets a boolean attribute to true in self.unit for each attribute that is
        found in the listing.

        Arguments:
            attrinfo: BeautifulSoup tag containing attrs.
        """
        attributes = attrgroup.findAll('span')
        for attr in attributes:
            self.attrset.add(attr.text)
            self.unit[attr.text] = True

    def _parserooms(self, bubble):
        """Parses the room attributes in the listing.

        Sets 'bedrooms' and 'bathrooms' attributes of self.unit.

        Arguments:
            bubble: BeautifulSoup tag with class 'shared-line-bubble'
        """
        isrooms = self._isrooms(bubble)
        if isrooms == 'BRBa':
            bedrooms, bathrooms = bubble.text.split(' / ')
            self.unit['bedrooms'] = int(bedrooms.strip('BR'))
            self.unit['bathrooms'] = float(bathrooms.strip('Ba'))
        elif isrooms == 'BR':
            self.unit['bedrooms'] = int(bubble.text.strip('BR'))
        elif isrooms == 'Ba':
            self.unit['bathrooms'] = float(bubble.text.strip('Ba'))

    def _parsesqft(self, bubble):
        """Parses the sqft attributes in the listing.

        Sets 'sqft' attribute of self.unit.

        Arguments:
            bubble: BeautifulSoup tag with class 'shared-line-bubble'
        """
        self.unit['sqft'] = int(bubble.text.strip('ft2'))

    def _price(self):
        """Parses the price in the listing.

        Sets 'price' attribute of self.unit.
        """
        pricetag = self.soup.find('span', {'class': 'price'})
        pricestr = pricetag.text.strip('$')
        self.unit['price'] = float(pricestr)

    def _title(self):
        """Parse the title of the listsing.

        Sets 'title' attribute of self.unit.
        """
        titletext = self.soup.find('span', {'id': 'titletextonly'}).text
        self.unit['title'] = titletext

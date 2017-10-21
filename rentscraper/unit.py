"""rentscraper.unit"""

class Unit(object):
    """Implements a class to represent a single Unit.

    Attributes:
        Boolean:
            apartment: bool
            cats_ok: bool
            dogs_ok: bool
            laundry_on_site: bool
            no_smoking: bool
            off_street_parking: bool
            street_parking: bool
            wheelchair_accessible: bool

        Numeric:
            bedrooms: int
            bathrooms: float
            latitude: float
            longitude: float
            num_images: int
            price: float
            sqft: int

        Text:
            description: str
            listing_id: str
            title: str
            zipcode: str
    """
    def __init__(self, listing_id=None, zipcode=None):
        self.data = {
            'bedrooms': int(),
            'bathrooms': float(),
            'latitude': float(),
            'listing_id': str(),
            'longitude': float(),
            'num_images': int(),
            'price': float(),
            'sqft': int(),
            'description': str(),
            'listing_id': str(),
            'title': str(),
            'zipcode': str()
        }

        if listing_id:
            self.data['listing_id'] = listing_id

        if zipcode:
            self.data['zipcode'] = zipcode

    def __getitem__(self, item):
        return self.data[item]

    def __iter__(self, item):
        for key, val in  self.data.items():
            yield key, val

    def __setitem__(self, item, val):
        self.data[item] = val

"""rentscraper.batchclean"""
import sys

from log import get_configured_logger
from pymongo import MongoClient

from listing import Listing

from absl import app

def cleanlistings(listings):
    """Clean a list of listings and return a clean unit object.

    Arguments:
        listings: pymongo cursor containing all listings

    Returns:
        units: list of Unit objects representing the cleaned listings
    """
    units = []
    for listing in listings:
        l = Listing(listing['content'])
        unit = l.clean()
        units.append(unit)

    return units

def queryforlistings(mongoclient):
    """Get all listings in the mongo database

    Arguments:
        mongoclient: mongo db to get listings from

    Returns:
        listings: list
    """
    listing_collection = mongoclient.scraper.listing
    query = {"content_parsed": False}
    listings = listing_collection.find(query)
    return listings

def writetomongo(mongoclient):
    """Write unit objects to mongo database

    Arguments:
        mongoclient: mongo db to write to
    """
    unit_collection = mongoclient.scraper.unit
    listing_collection = mongoclient.scraper.listing
    for unit in unit_collection
        unit_collection.insert_one(dict(unit))
        query = {"_id": unit['listing_id']}
        update = {"$set": {"content_parsed": True}}
        listing_collection.update_one(query, update)

def main(argv):
    """Main entry-point for batchclean."""
    del argv # unused

    mongoclient = MongoClient('localhost', 27017)
    listings = queryforlistings(mongoclient)
    units = cleanlistings(listings)
    writetomongo(units)

if __name__ == '__main__':
    app.run(main)

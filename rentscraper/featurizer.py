"""rentscraper.featurizer"""
import sys

from log import get_configured_logger
from pymongo import MongoClient

from listing import Listing

from absl import app

def featurizelistings(listings, mongoclient):
    """Featurize a list of listings, then write to mongo.

    Arguments:
        listings: pymongo cursor containing all listings
        mongoclient: mongo db to write to
    """
    for listing in listings:
        l = Listing(listing, mongoclient)
        l.featurize()
        l.writetomongo()

def queryforlistings(mongoclient):
    """Get all listings in the mongo database

    Arguments:
        mongoclient: mongo db to get listings from

    Returns:
        listings: list
    """
    listing_collection = mongoclient.scraper.listing
    listings = listing_collection.find()
    return listings

def main(argv):
    """Main entry-point for featurizer."""
    del argv # unused

    mongoclient = MongoClient('localhost', 27017)
    listings = queryforlistings(mongoclient)
    featurizelistings(listings, mongoclient)

if __name__ == '__main__':
    app.run(main)

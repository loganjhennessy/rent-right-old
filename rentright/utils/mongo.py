"""rentright.utils.mongo"""
import os

from pymongo import MongoClient

def get_mongoclient():
    MONGO_USER = os.environ['MONGO_USER']
    MONGO_PASS = os.environ['MONGO_PASS']
    MONGO_IP = os.environ['MONGO_IP']
    connstr = 'mongodb://{}:{}@{}/scraper'
    mongoclient = MongoClient(connstr.format(MONGO_USER, MONGO_PASS, MONGO_IP))
    return mongoclient

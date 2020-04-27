from pymongo import MongoClient

from pymongo import MongoClient

client = MongoClient('mongo-0.mongo', 27017)
feeds = client.feeds
config = client.config


def getCrawlers():
    crawlers = config["crawlers"]
    return crawlers.find({})
from enum import Enum

import jsonpickle

from FeedToRestrictionMapping import JsonEnumHandler
from crawlers import *
jsonpickle.handlers.registry.register(Enum, JsonEnumHandler, True)
for crawler in CRAWLERS:
    try:
        print('Start crawling: ' + type(crawler).__name__ + ' with mapper: ' + jsonpickle.encode(crawler.mapper,unpicklable=True))
        crawler.parse_feed()
        print('Finished crawling: ' + type(crawler).__name__)
    except Exception as e:
        print(type(crawler).__name__ + ' failed with:' + str(e))

print("--------------------------------------------")
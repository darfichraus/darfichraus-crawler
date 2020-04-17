import os;
from enum import Enum
from optparse import OptionParser

import jsonpickle

from FeedToRestrictionMapping import JsonEnumHandler
from crawlers import *

jsonpickle.handlers.registry.register(Enum, JsonEnumHandler, True)

parser = OptionParser()
parser.add_option('-u', '--url', action="store", dest="url", help="Post url (ex. https://api.dev.crimsy.tech"
                                                                  "/restrictions)",
                  default='http://backend/restrictions')
parser.add_option('-a', '--api_key', action="store", dest="api_key", help="API-KEY for authentication",
                  default=os.environ.get("API_KEY"))

options, args = parser.parse_args()
if not options.url:
    print("[+] Specify an url target")
    exit()
if not options.api_key:
    print("[+] Specify an api_key (or specifiy API_KEY env variable)")
    exit()

for crawler in CRAWLERS:
    try:
        print('Start crawling: ' + type(crawler).__name__ + ' with mapper: ' + jsonpickle.encode(crawler.mapper,
                                                                                                 unpicklable=True))
        crawler.parse_feed(options)
        print('Finished crawling: ' + type(crawler).__name__)
    except Exception as e:
        print(type(crawler).__name__ + ' failed with:' + str(e))

print("--------------------------------------------")

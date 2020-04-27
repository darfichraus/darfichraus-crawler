from FeedParser import *

for crawler in database.getCrawlers():

    try:
        parser = FeedParser(crawler)
        print('Start crawling: ' + crawler["name"])
        parser.parse_feed()
        print('Finished crawling: ' + crawler["name"])
    except Exception as e:
        print(crawler["name"] + ' failed with:' + str(e))

print("--------------------------------------------")

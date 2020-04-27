import locale
import re
from html.parser import HTMLParser

import feedparser
import database
from datetime import datetime


class FeedParser:
    unique_field = "id"
    locale.setlocale(locale.LC_ALL, "de_DE")
    TAG_RE = re.compile(r'<[^>]+>')
    hp = HTMLParser()
    dateHandler = None

    def __init__(self, config: dict):
        self.feed_url = config["url"]
        self.collection = database.feeds[config["name"]]
        if "unique_field" in config:
            self.unique_field = config["unique_field"]
        if "publishedDateFormat" in config:
            self.dateHandler = lambda datestring: datetime.strptime(datestring,
                                                                    config["publishedDateFormat"]).timetuple()

    def parse_feed(self):
        new_feed = []
        if self.dateHandler:
            feedparser.registerDateHandler(self.dateHandler)
        feed = feedparser.parse(self.feed_url)
        for feedelement in feed.entries:
            for key in feedelement.keys():
                if "_parsed" in key:
                    continue
                if isinstance(feedelement[key], list):
                    if key == "content":
                        feedelement[key] = feedelement[key][0].value
                feedelement[key] = str(feedelement[key])
                feedelement[key] = self.TAG_RE.sub('', feedelement[key])
                feedelement[key] = self.hp.unescape(feedelement[key])
            new_feed.append(feedelement)
        self.deduplicateAndProcess(new_feed)

    def deduplicateAndProcess(self, feed):
        for feeditem in feed:
            if not self.collection.find_one({self.unique_field: feeditem[self.unique_field]}, {self.unique_field: 1}):
                self.collection.insert(feeditem)

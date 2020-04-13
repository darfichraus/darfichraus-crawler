import locale
import re
from abc import ABC
from html.parser import HTMLParser
import feedparser
import requests
from pymongo import MongoClient


class FeedParser(ABC):
    ref_fields = ["summary", "title"]
    unique_field = "id"
    key_words = ['Corona', 'Sperre', 'Covid']
    locale.setlocale(locale.LC_ALL, "de_DE")
    mapper = None

    TAG_RE = re.compile(r'<[^>]+>')
    hp = HTMLParser()
    dateHandler = None

    def __init__(self, mapper, feed_url):
        self.feed_url = feed_url
        self.mapper = mapper
        self.dbclient = MongoClient('localhost', 27017)
        self.db = self.dbclient.feeds
        self.collection = self.db[type(self).__name__]

    def get_key_words(self):
        return ['Corona', 'Sperre', 'Covid']

    def contains_wanted(self, feedelement):
        for wrd in self.key_words:
            for ref_field in self.ref_fields:
                if wrd.lower() in feedelement[ref_field].lower():
                    return True
        return False

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
        self.deduplicate(new_feed)

    def deduplicate(self, feed):
        filtered_feed = []
        for feeditem in feed:
            if not self.collection.find_one({self.unique_field: feeditem[self.unique_field]}, {self.unique_field: 1}):
                if self.contains_wanted(feeditem):
                    filtered_feed.append(feeditem)
                else:
                    self.markAsProcessed(feeditem)
        self.saveFeedElements(filtered_feed)

    def markAsProcessed(self, feedelement):
        self.collection.insert(feedelement)

    def saveFeedElements(self, feed):
        processed_entries = []
        headers = {'API-KEY': '6bce1751a010f90b68eb887cae8e2141cce149d5de664412e67cdf150006aa16f2bd0373ce496aa5'}
        url = 'https://api.dev.crimsy.tech/restrictions'
        for feedelement in feed:
            json = self.mapper.map_to_restriction(feedelement).to_json()
            response = requests.post(url, headers=headers,
                                     json=json)
            if response.status_code == 204:
                processed_entries.append(feedelement)
                self.markAsProcessed(feedelement)
            else:
                print(feedelement[self.unique_field] + 'could not be saved: ' + response.text)

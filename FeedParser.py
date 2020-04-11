from abc import ABC, abstractmethod
import feedparser
from pymongo import MongoClient
import requests
from datetime import *
import locale
from time import mktime
from html.parser import HTMLParser
import re

api_dateFormat = '%Y-%m-%d'



class FeedParser(ABC):
    
    ref_fields = ["summary","title"]
    unique_field = "id"
    dateFormat = None
    key_words = ['Corona','Sperre', 'Covid']   
    locale.setlocale(locale.LC_ALL, "de_DE")

    TAG_RE = re.compile(r'<[^>]+>')
    hp = HTMLParser()


    def __init__(self):
        self.dbclient =  MongoClient('localhost', 27017)
        self.db = self.dbclient.feeds
        self.collection = self.db[type(self).__name__]

    def get_key_words(self):
        return ['Corona','Sperre', 'Covid']   
    
    def contains_wanted(self, feedelement):
        for wrd in self.key_words:
            for ref_field in self.ref_fields:
                if wrd.lower() in feedelement[ref_field].lower():
                    return True
        return False
    def parse_feed(self):
        newFeed = []
        # feedp= new FeedParser()
        feed = feedparser.parse(self.feed_url)
        print("feed len" + str(len(feed.entries)))
        for feedelement in feed.entries:
            if self.contains_wanted(feedelement):
                for key in feedelement.keys():
                    if "_parsed" in key:
                        continue
                    print(feedelement[key])
                    feedelement[key] = str(feedelement[key])
                    feedelement[key] = self.TAG_RE.sub('', feedelement[key])
                    feedelement[key] = self.hp.unescape(feedelement[key])
                  
                newFeed.append(feedelement)
        print("newFeed len" + str(len(newFeed)))
        self.deduplicate(newFeed)

    def deduplicate(self, feed):
        print("feed len2" + str(len(feed)))
        cleaned_feed = []
        for feeditem in feed:
            if not self.collection.find_one({self.unique_field: feeditem[self.unique_field]}, { self.unique_field: 1}):
                cleaned_feed.append(feeditem)
        print("len cleaned feed" + str(len(cleaned_feed)))
        self.saveFeedElements(cleaned_feed)

    def markAsProcessed(self, feedelement):
        self.collection.insert(feedelement)   
    
    def saveFeedElements(self, feed):
        print("feed3 len " + str(len(feed)))
        processed_entries = []
        headers = {'API-KEY': '6bce1751a010f90b68eb887cae8e2141cce149d5de664412e67cdf150006aa16f2bd0373ce496aa5'}
        url = 'https://api.dev.crimsy.tech/restrictions'
        for feedelement in feed:
            response = requests.post(url, headers=headers,json = self.mapToRestriction(feedelement))
            if response.status_code==204:
                processed_entries.append(feedelement)
                self.markAsProcessed(feedelement)
        print("last feed " + str(len(feed)))

    def mapToRestriction(self,feedelement):
        if self.dateFormat:
            feedelement.published_parsed = datetime.strptime(feedelement.published, self.dateFormat)
        else:
            feedelement.published_parsed = datetime.fromtimestamp(mktime(feedelement.published_parsed))   

        
        
        return {
            "areal": self.areal,
            "arealIdentifier": self.arealIdentifier,
            "restrictionType": "EVENTS_AND_ASSEMBLIES",
            "restrictionState": "BAN",
            "shortDescription": feedelement.title,
            "restrictionDescription": feedelement.summary,
            "restrictionStart": feedelement.published_parsed.strftime(api_dateFormat),
            "restrictionEnd":  (feedelement.published_parsed + timedelta(days=14)).strftime(api_dateFormat),
            "recipient": "Bürger",
            "publisher": "Landesregierung " + self.arealIdentifier,
            "furtherInformation": feedelement.link,
            }
                   




#! python
import feedparser
from w3lib.html import remove_tags

link = "https://www.baden-wuerttemberg.de/de/service/rss/xml/rss-alle-meldungen/"
feed = feedparser.parse(link)

key_words = ['Corona','Sperre', 'Covid']

def contains_wanted(feedelement):
    for wrd in key_words:
        # print(feedelement.summary)
        if wrd.lower() in feedelement.summary.lower():
            return True
    return False

newFeed = []

print(feed.entries[0])

for feedelement in feed.entries:
    for key in feedelement.keys():
        feedelement[key] = remove_tags(str(feedelement[key]))
        if contains_wanted(feedelement):
            newFeed.append(feedelement)

            
            
print(newFeed[0])
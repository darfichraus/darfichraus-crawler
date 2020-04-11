#! python
import feedparser
from w3lib.html import remove_tags
key_words = ['Corona','Sperre', 'Covid']

def contains_wanted(feedelement):
    for wrd in key_words:
        # print(feedelement.summary)
        if wrd.lower() in feedelement.summary.lower():
            return True
    return False

links = ["https://www.landtag.brandenburg.de/cms/detail.php?template=lt_rss_presse_d",
"https://www.baden-wuerttemberg.de/de/service/rss/xml/rss-alle-meldungen/",
"https://www.parlament-berlin.de/C12581B8002C4D6A/DIRECTOR.xsp?qname=RSS_Materialien_Ausschuss_GesPflegGleich&rsstitle=RSS%20Feed%20Materialien%20des%20Ausschusses%20fuer%20Gesundheit,%20Pflege%20und%20Gleichstellung"]

newFeed = []
for link in links:
    feed = feedparser.parse(link)
    for feedelement in feed.entries:
        for key in feedelement.keys():
            feedelement[key] = remove_tags(str(feedelement[key]))
            if contains_wanted(feedelement):
                newFeed.append(feedelement)

print(newFeed[0].guid)    
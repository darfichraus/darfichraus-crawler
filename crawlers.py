from FeedParser import *

class BadenW(FeedParser):
    def __init__(self):
        super().__init__()
        self.feed_url = "https://www.baden-wuerttemberg.de/de/service/rss/xml/rss-alle-meldungen/"
        self.areal = "STATE"
        self.arealIdentifier = "Baden-Württemberg"



class Nrw(FeedParser):
     def __init__(self):
        super().__init__()
        self.feed_url = "https://www.land.nrw/de/press-release/feed"
        self.areal = "STATE"
        self.arealIdentifier = "Nordrhein-Westfalen"
        self.dateFormat="%A, %d. %B %Y - %H:%M"

class Bayern(FeedParser):
       def __init__(self):
        super().__init__()
        self.feed_url = "https://www.bayern.de/category/pressemitteilungen/feed"
        self.areal = "STATE"
        self.arealIdentifier = "Bayern"
from datetime import datetime

from feedparser import FeedParserDict

from FeedParser import *
from FeedToRestrictionMapping import Mapper, Areal, Restriction


def content_mapper(restriction: Restriction, feeditem: FeedParserDict) -> Restriction:
    restriction.restrictionDescription = feeditem["content"]
    return restriction


class BadenW(FeedParser):
    def __init__(self):
        super().__init__(mapper=Mapper(Areal.STATE, "Baden-Württemberg"),
                         feed_url="https://www.baden-wuerttemberg.de/de/service/rss/xml/rss-alle-meldungen/")


class Nrw(FeedParser):
    def __init__(self):
        super().__init__(mapper=Mapper(Areal.STATE, "Nordrhein-Westfalen"),
                         feed_url="https://www.land.nrw/de/press-release/feed")
        self.dateHandler = lambda datestring: datetime.strptime(datestring, "%A, %d. %B %Y - %H:%M").timetuple()


class Niedersachsen(FeedParser):
    def __init__(self):
        super().__init__(mapper=Mapper(Areal.STATE, "Niedersachsen"),
                         feed_url="https://www.landtag-niedersachsen.de/rss/presse.xml")


class Bayern(FeedParser):
    def __init__(self):
        super().__init__(mapper=Mapper(Areal.STATE, "Bayern", content_mapper),
                         feed_url="https://www.bayern.de/category/pressemitteilungen/feed")
        self.unique_field = "link"


class Sachsen(FeedParser):
    def __init__(self):
        super().__init__(mapper=Mapper(Areal.STATE, "Sachsen", use_system_time=True),
                         feed_url="https://www.landtag.sachsen.de/de/rss/meldungen")
        self.unique_field = "link"


class RheinlandP(FeedParser):
    def __init__(self):
        super().__init__(mapper=Mapper(Areal.STATE, "Rheinland-Pfalz", content_mapper),
                         feed_url="https://www.landtag.rlp.de/de/general-storage/footer/infos-zum-herunterladen/rss-feed/rss-feed-presse/index.rss")



class MecklenburgVorpommern(FeedParser):
     def __init__(self):
         super().__init__(mapper=Mapper(Areal.STATE, "Mecklenburg-Vorpommern", use_system_time=True),
                          feed_url="https://service.mvnet.de/_php/feedcreator/feeds/feed_Regierungsportal_99.xml")


class Hessen(FeedParser):
    def __init__(self):
        super().__init__(mapper=Mapper(Areal.STATE, "Hessen"),
                         feed_url="https://www.hessen.de/feeds")


class Thueringen(FeedParser):
    def __init__(self):
        super().__init__(mapper=Mapper(Areal.STATE, "Thüringen"),
                         feed_url="https://www.tlm.de/presse.xml")
        self.unique_field = "link"


class PressePortalDe(FeedParser):
    def __init__(self):
        super().__init__(mapper=Mapper(Areal.COUNTRY, "Deutschland", content_mapper),
                         feed_url="https://www.presseportal.de/rss/gesundheit-medizin.rss2")


class Brandenburg(FeedParser):
    def __init__(self):
        super().__init__(mapper=Mapper(Areal.STATE, "Brandenburg"),
                         feed_url="https://www.landtag.brandenburg.de/cms/detail.php?template=lt_rss_presse_d")


class SachsenAnhalt(FeedParser):
    def __init__(self):
        super().__init__(mapper=Mapper(Areal.STATE, "Sachsen-Anhalt", content_mapper),
                         feed_url="https://statistik.sachsen-anhalt.de/index.php?id=57455")


class Hamburg(FeedParser):
    def __init__(self):
        super().__init__(mapper=Mapper(Areal.STATE, "Hamburg"),
                         feed_url="https://www.hamburg-news.hamburg/feeds/articles/46/")


CRAWLERS = [BadenW(), Brandenburg(), Hamburg(), Hessen(), RheinlandP(), Niedersachsen(), PressePortalDe(), Sachsen(),
            SachsenAnhalt(), Thueringen(), Nrw(), MecklenburgVorpommern(), Bayern()]

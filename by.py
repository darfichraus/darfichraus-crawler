import feedparser

link = "https://www.bayern.de/category/pressemitteilungen/feed"

feed = feedparser.parse(link)

entry = feed.entries[0]
print(entry.keys())
print(entry)
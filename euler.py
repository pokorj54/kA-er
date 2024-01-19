import feedparser

def get_items():
    d = feedparser.parse('https://projecteuler.net/rss2_euler.xml')
    return d['entries']
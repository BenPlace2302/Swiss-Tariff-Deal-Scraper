import feedparser
import requests
from bs4 import BeautifulSoup

rss_feeds = [
    "https://feeds.bloomberg.com/politics/news.rss",
    "https://feeds.bloomberg.com/markets/news.rss",
    "https://news.google.com/rss/search?q=site%3Areuters.com&hl=en-US&gl=US&ceid=US%3Aen"
]

keywords = ["swiss", "switzerland"]

important_keywords = [
    "deal reached",
    "deal signed",
    "agreement signed",
    "trade agreement finalized",
    "trade pact concluded",
    "deal finalized",
    "deal struck",
    "deal concluded",
    "deal completed",
    "agreement finalized",
    "agreement sealed",
    "deal secured",
    "agreement ratified",
    "signed trade agreement"
]

def is_important(news):
    return any(keyword in news for keyword in important_keywords)

def get_finance_news():
    matches = []
    for url in rss_feeds:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            title = entry.get('title', '').lower()
            if any(keyword in title for keyword in keywords):
                matches.append(title)
    return matches

def get_roche_price():
    url = "https://finance.yahoo.com/quote/ROG.SW"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    price_tag = soup.find("span", {"data-testid": "qsp-price"})

    if price_tag:
        price_text = price_tag.text.replace(',', '')
        return float(price_text)
    else:
        print("Price not found.")
        return None

if __name__ == "__main__":
    news = get_finance_news()
    if news:
        print("Swiss headlines:")
        important_found = False
        for n in news:
            if is_important(n):
                important_found = True
                print(f"! {n}")
            else:
                print(f"- {n}")

        if important_found:
            price = get_roche_price()
            print(f"Roche Holding AG current price: {price}")
    else:
        print("No Swiss headlines found.")

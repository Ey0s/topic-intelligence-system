from typing import List
from app.scrapers.rss_scraper import RSSScraper
from app.scrapers.sources import news, tech, sports, finance

class QueryService:
    """
    Aggregates multiple RSS feeds by category and filters by topic.
    """

    def __init__(self):
        self.scraper = RSSScraper()

    def search(self, topic: str, category: str = "news") -> List[dict]:
        """
        Search articles by topic and category.
        """
        feeds = []

        if category == "news":
            feeds = news.NEWS_FEEDS
        elif category == "tech":
            feeds = tech.TECH_FEEDS
        elif category == "sports":
            feeds = sports.SPORTS_FEEDS
        elif category == "finance":
            feeds = finance.FINANCE_FEEDS
        else:
            feeds = news.NEWS_FEEDS

        all_articles = []

        for feed_url in feeds:
            articles = self.scraper.fetch_feed(feed_url)

            filtered = [
                a for a in articles
                if topic.lower() in a["title"].lower() or topic.lower() in a["summary"].lower()
            ]

            all_articles.extend(filtered)

        return all_articles[:10]
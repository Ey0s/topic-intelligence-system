import asyncio
import httpx
from typing import List
from app.scrapers.rss_scraper import RSSScraper
from app.scrapers.sources import news, tech, sports, finance


class QueryService:

    def __init__(self):
        self.scraper = RSSScraper()

    async def search(self, topic: str, category: str = "news") -> List[dict]:
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

        async with httpx.AsyncClient(headers={"User-Agent": "Mozilla/5.0"}) as client:

            tasks = [
                self.scraper.fetch_feed(client, feed_url)
                for feed_url in feeds
            ]

            results = await asyncio.gather(*tasks)

        all_articles = [article for feed in results for article in feed]

        filtered = [
            a for a in all_articles
            if topic.lower() in a["title"].lower()
            or topic.lower() in a["summary"].lower()
        ]

        return filtered[:10]
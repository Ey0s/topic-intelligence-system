import asyncio
import httpx
from typing import List
from datetime import datetime
from app.scrapers.rss_scraper import RSSScraper
from app.scrapers.sources import news, tech, sports, finance


class QueryService:
    def __init__(self):
        self.scraper = RSSScraper()

    def compute_score(self, article: dict, topic: str) -> int:
        score = 0
        topic_lower = topic.lower()

        if topic_lower in article["title"].lower():
            score += 2

        if topic_lower in article["summary"].lower():
            score += 1

        return score

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
                self.scraper.fetch_feed(client, url)
                for url in feeds
            ]

            results = await asyncio.gather(*tasks)

        all_articles = [article for feed in results for article in feed]

        for article in all_articles:
            article["score"] = self.compute_score(article, topic)

        filtered = [a for a in all_articles if a["score"] > 0]

        filtered.sort(
            key=lambda x: (
                x["score"],
                x["pubDate"] or datetime.min
            ),
            reverse=True
        )

        return filtered
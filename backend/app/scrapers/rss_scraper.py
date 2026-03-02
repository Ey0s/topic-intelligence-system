import requests
import xml.etree.ElementTree as ET
from typing import List, Dict

class RSSScraper:
    """
    Generic RSS feed scraper.
    Fetches RSS feed and returns structured articles.
    """

    def fetch_feed(self, url: str) -> List[Dict]:
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                print(f"Failed to fetch RSS feed: {url}")
                return []

            root = ET.fromstring(response.content)
            articles = []

            for item in root.findall(".//item"):
                title = item.find("title").text
                link = item.find("link").text
                description = item.find("description").text

                articles.append({
                    "title": title,
                    "link": link,
                    "summary": description
                })

            return articles

        except Exception as e:
            print(f"RSS Scraper Error ({url}): {e}")
            return []
import httpx
import xml.etree.ElementTree as ET
from typing import List, Dict


class RSSScraper:
    async def fetch_feed(self, client: httpx.AsyncClient, url: str) -> List[Dict]:
        try:
            response = await client.get(url, timeout=10.0)

            if response.status_code != 200:
                print(f"Failed to fetch: {url}")
                return []

            root = ET.fromstring(response.content)
            articles = []

            for item in root.findall(".//item"):
                title = item.find("title").text if item.find("title") is not None else ""
                link = item.find("link").text if item.find("link") is not None else ""
                description = item.find("description").text if item.find("description") is not None else ""

                articles.append({
                    "title": title,
                    "link": link,
                    "summary": description
                })

            return articles

        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return []
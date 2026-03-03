import httpx
import xml.etree.ElementTree as ET
from typing import List, Dict
from email.utils import parsedate_to_datetime

class RSSScraper:
    async def fetch_feed(self, client: httpx.AsyncClient, url: str) -> List[Dict]:
        try:
            response = await client.get(url, timeout=10.0)

            if response.status_code != 200:
                return []

            root = ET.fromstring(response.content)
            articles = []

            for item in root.findall(".//item"):
                title = item.findtext("title", default="")
                link = item.findtext("link", default="")
                description = item.findtext("description", default="")
                guid = item.findtext("guid", default=link)
                pub_date_raw = item.findtext("pubDate")

                parsed_date = None
                if pub_date_raw:
                    try:
                        parsed_date = parsedate_to_datetime(pub_date_raw)
                    except Exception:
                        parsed_date = None

                articles.append({
                    "id": guid,
                    "title": title,
                    "link": link,
                    "summary": description,
                    "pubDate": parsed_date
                })

            return articles

        except Exception:
            return []
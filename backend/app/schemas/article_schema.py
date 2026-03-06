from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import datetime


class Article(BaseModel):
    id: str
    title: str
    link: HttpUrl
    summary: str
    pubDate: Optional[datetime] = None
    score: Optional[int] = 0


class ArticleResponse(BaseModel):
    topic: str
    page: int
    size: int
    total_results: int
    results: List[Article]
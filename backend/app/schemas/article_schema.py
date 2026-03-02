from pydantic import BaseModel
from typing import List

class Article(BaseModel):
    title: str
    link: str
    summary: str

class ArticleResponse(BaseModel):
    topic: str
    results: List[Article]
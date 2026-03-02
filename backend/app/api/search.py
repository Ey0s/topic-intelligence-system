from fastapi import APIRouter, Query
from app.services.query_service import QueryService
from app.schemas.article_schema import ArticleResponse, Article

router = APIRouter()
query_service = QueryService()

@router.get("/search", response_model=ArticleResponse)
def search(topic: str = Query(..., description="Search topic"),
           category: str = Query("news", description="Category: news, tech, sports, finance")):
    results = query_service.search(topic, category)
    return ArticleResponse(
        topic=topic,
        results=[Article(**a) for a in results]
    )
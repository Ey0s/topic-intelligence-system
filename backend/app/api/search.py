from fastapi import APIRouter, Query
from app.services.query_service import QueryService
from app.schemas.article_schema import ArticleResponse, Article

router = APIRouter()
query_service = QueryService()

@router.get("/")
async def home():
    return {"message": "Welcome to the Topic Intelligence System API. Use /search endpoint to find articles."}

from fastapi import APIRouter, Query
from app.services.query_service import QueryService
from app.schemas.article_schema import ArticleResponse, Article

router = APIRouter()
query_service = QueryService()


@router.get("/search", response_model=ArticleResponse)
async def search(
    topic: str = Query(..., description="Search topic"),
    category: str = Query("news", description="news, tech, sports, finance"),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=50)
):
    results = await query_service.search(topic, category)

    total = len(results)

    start = (page - 1) * size
    end = start + size

    paginated = results[start:end]

    return ArticleResponse(
        topic=topic,
        page=page,
        size=size,
        total_results=total,
        results=[Article(**a) for a in paginated]
    )
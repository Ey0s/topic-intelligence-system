from fastapi import FastAPI
from app.api.search import router as search_router
from app.core.logger import setup_logger
from app.core.database import Base, engine
from app.models.article import Article

# starting logger
setup_logger()

app = FastAPI(title="CyberRisk Forecasting API")

Base.metadata.create_all(bind=engine)

app.include_router(search_router)
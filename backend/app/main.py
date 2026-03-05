from fastapi import FastAPI
from app.core.logger import setup_logger
from app.api.search import router as search_router
# starting logger
setup_logger()

app = FastAPI()

app.include_router(search_router)
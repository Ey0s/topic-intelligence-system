from fastapi import FastAPI
from app.api import search

app = FastAPI(title="Topic Intelligence System")

app.include_router(search.router)
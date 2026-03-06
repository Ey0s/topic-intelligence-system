from sqlalchemy import Column, String, DateTime, Integer
from app.core.database import Base


class Article(Base):
    __tablename__ = "articles"

    id = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    link = Column(String, nullable=False)
    summary = Column(String)
    pubDate = Column(DateTime)
    score = Column(Integer, default=0)
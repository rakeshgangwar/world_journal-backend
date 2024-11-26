import os

from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv("DATABASE_URL")

Base = declarative_base()
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class RSSFeed(Base):
    __tablename__ = "rss_feeds"
    id = Column(Integer, primary_key=True, index=True)
    topic = Column(String, index=True)
    feed_url = Column(String)

class Feeds(Base):
    __tablename__ = "feeds"
    feedId = Column(Integer, primary_key=True, index=True)
    categoryId = Column(Integer)
    title = Column(String, index=True)
    description = Column(String)
    feed_url = Column(String)

def init_db():
    Base.metadata.create_all(bind=engine)
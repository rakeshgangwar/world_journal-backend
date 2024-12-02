from database import SessionLocal, RSSFeed, Feeds


def get_feeds_by_topic(topic: str):
    """
    Fetch all RSS feeds for a specific topic.
    """
    session = SessionLocal()
    feeds = session.query(RSSFeed).filter(RSSFeed.topic == topic).all()
    session.close()
    return feeds

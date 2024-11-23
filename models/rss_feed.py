from database import SessionLocal, RSSFeed

def get_feeds_by_topic(topic: str):
    """
    Fetch all RSS feeds for a specific topic.
    """
    session = SessionLocal()
    feeds = session.query(RSSFeed).filter(RSSFeed.topic == topic).all()
    session.close()
    return feeds

def add_feed(topic: str, feed_url: str):
    """
    Add a new RSS feed to the database.
    """
    session = SessionLocal()
    new_feed = RSSFeed(topic=topic, feed_url=feed_url)
    session.add(new_feed)
    session.commit()
    session.close()

def delete_feed(feed_id: int):
    """
    Delete an RSS feed by ID.
    """
    session = SessionLocal()
    feed = session.query(RSSFeed).filter(RSSFeed.id == feed_id).first()
    if feed:
        session.delete(feed)
        session.commit()
    session.close()
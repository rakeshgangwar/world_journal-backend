from dotenv import load_dotenv

load_dotenv()

from fastapi import FastAPI, HTTPException, BackgroundTasks
from database import init_db
from models.rss_feed import get_feeds_by_topic, add_feed, delete_feed
from services.workflow import process_and_publish
from scheduler import schedule_jobs

app = FastAPI()

# @app.on_event("startup")
# def startup_event():
#     init_db()
#     schedule_jobs()

@app.get("/")
def read_root():
    return {"message": "Earth Journal Backend with LangGraph is running."}

@app.post("/rss/add/")
def add_rss_feed(topic: str, feed_url: str):
    add_feed(topic, feed_url)
    return {"message": f"RSS feed added for topic: {topic}"}

@app.get("/rss/{topic}/")
def get_rss_feeds(topic: str):
    feeds = get_feeds_by_topic(topic)
    if not feeds:
        raise HTTPException(status_code=404, detail="No feeds found for this topic")
    return {"feeds": [{"id": feed.id, "feed_url": feed.feed_url} for feed in feeds]}

@app.delete("/rss/delete/{feed_id}/")
def delete_rss_feed(feed_id: int):
    delete_feed(feed_id)
    return {"message": f"RSS feed with ID {feed_id} deleted"}

@app.post("/publish/")
def publish_entry(topic: str):
    content = process_and_publish(topic)
    return {"status": "Processing", "title": content["title"], "content": content["content"], "summary": content["summary"]}
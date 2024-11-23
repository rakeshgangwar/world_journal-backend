from apscheduler.schedulers.background import BackgroundScheduler
from services.workflow import process_and_publish
from models.rss_feed import get_feeds_by_topic
import random

def schedule_jobs():
    scheduler = BackgroundScheduler()

    def publish_random_topic():
        topics = [feed.topic for feed in get_feeds_by_topic()]
        if topics:
            topic = random.choice(topics)
            process_and_publish(topic)

    scheduler.add_job(publish_random_topic, "interval", hours=4)
    scheduler.start()
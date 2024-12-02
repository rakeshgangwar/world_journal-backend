import time

from dotenv import load_dotenv

from supabase_api import fetch_feeds_by_category

load_dotenv()

import feedparser
import requests
from bs4 import BeautifulSoup
from earth.langchain_utils import summarize_with_chain
from models.rss_feed import get_feeds_by_topic


def fetch_rss_data(topic: str) -> str:
    feeds = get_feeds_by_topic(topic)
    if not feeds:
        return f"No RSS feeds available for topic: {topic}"
    print(f"Feeds for topic {topic}: {feeds}")

    context = []
    for feed in feeds:
        parsed_feed = feedparser.parse(feed.feed_url)
        for entry in parsed_feed.entries[:5]:  # Limit to 5 entries
            print(f"Entry: {entry.title}")
            scraped_content = scrape_article(entry.link)
            # print(f"Scraped content for {entry.title}: {scraped_content}")
            if scraped_content:
                summary = summarize_with_chain(scraped_content, False)
                # print(f"Summary for {entry.title}: {summary}")
                context.append(f"- **{entry.title}**: {summary} ({entry.link})")
            else:
                context.append(f"- **{entry.title}**: Unable to fetch content. ({entry.link})")

    # print(f"Context for topic {topic}: {context}")
    return "\n".join(context)


def fetch_category_rss(category_id: int) -> str:
    feeds = fetch_feeds_by_category(category_id)
    if not feeds:
        return f"No RSS feeds available for category ID: {category_id}"
    print(f"Feeds for category ID {category_id}: {feeds}")

    context = []
    for feed in feeds:
        parsed_feed = feedparser.parse(feed["feed_url"])
        for entry in parsed_feed.entries[:5]:  # Limit to 5 entries
            if hasattr(entry, 'published_parsed') and entry.published_parsed.tm_year == time.localtime().tm_year and entry.published_parsed.tm_mon == time.localtime().tm_mon and entry.published_parsed.tm_mday == time.localtime().tm_mday:
                print(f"Entry: {entry.title}")
                scraped_content = scrape_article(entry.link)
                # print(f"Scraped content for {entry.title}: {scraped_content}")
                if scraped_content:
                    summary = summarize_with_chain(scraped_content, False)
                    # print(f"Summary for {entry.title}: {summary}")
                    context.append(f"- **{entry.title}**: {summary} ({entry.link})")
                else:
                    context.append(f"- **{entry.title}**: Unable to fetch content. ({entry.link})")

    # print(f"Context for category ID {category_id}: {context}")
    return "\n".join(context)


def scrape_article(url: str) -> str:
    try:
        print(f"Scraping {url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(url, timeout=10, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        paragraphs = soup.find_all("p")
        content = " ".join([p.get_text() for p in paragraphs])
        return content if len(content) > 200 else None
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

# print(fetch_rss_data("Life and Evolution"))

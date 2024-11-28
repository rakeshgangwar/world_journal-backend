import requests
import os
from datetime import datetime
import base64

GITHUB_API_URL = "https://api.github.com/repos/rakeshgangwar/world-journal/contents/"
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
BRANCH = "main"  # or your default branch name

def publish_blog(topic: str, title: str, content: str, summary: str):
    """
    Publish the blog post to GitHub via the GitHub API.
    """
    print(f"Publishing blog: {title}")
    date = datetime.now().isoformat()
    date_slug = datetime.now().strftime("%Y-%m-%d")
    filename = f"src/content/blog/{date_slug}-{title.replace(' ', '-').lower()}/index.md"

    frontmatter = f"""---
title: "{title}"
summary: "{summary}"
date: "{date}"
draft: false
featured: false
tags:
    - {topic}
---

"""
    markdown_content = frontmatter + content
    encoded_content = base64.b64encode(markdown_content.encode()).decode()

    url = GITHUB_API_URL + filename
    headers = {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Content-Type": "application/vnd.api+json",
        "Accept": "application/vnd.github+json",
        "User-Agent": "World-Bot"
    }
    payload = {
        "message": f"Add new blog post: {title}",
        "content": encoded_content,
        "branch": BRANCH
    }

    response = requests.put(url, headers=headers, json=payload)
    if response.status_code == 201:
        print("Blog published successfully.")
    else:
        print(f"Failed to publish blog: {response.text}")

# publish_blog("Life and Evolution", "This is a test blog post.", "This is a summary.")
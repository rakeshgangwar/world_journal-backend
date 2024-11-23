from services.rss_fetcher import fetch_rss_data
from services.prompt_generator import generate_prompt
from services.langchain_utils import summarize_with_chain, generate_blog_with_chain, title_with_chain
from services.publisher import publish_blog

def process_and_publish(topic: str):
    """
    Workflow to fetch data, generate content, and publish a blog.
    """
    # Fetch and summarize RSS content
    context = fetch_rss_data(topic)

    # Generate blog content using LangChain
    prompt = generate_prompt(topic, context)
    blog_content = generate_blog_with_chain(prompt)

    title = title_with_chain(blog_content)
    summary = summarize_with_chain(blog_content, title, True)

    # Publish to TinaCMS
    publish_blog(topic, title, blog_content, summary)

    return {"title": title, "content": blog_content, "summary": summary}

# process_and_publish("Life and Evolution")
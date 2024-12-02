from wheel.rss_fetcher import fetch_rss_data, fetch_category_rss
from wheel.prompt_generator import generate_prompt
from wheel.langchain_utils import summarize_with_chain, generate_blog_with_chain, title_with_chain
from earth.publisher import publish_blog
from supabase_api import fetch_category


def process_and_publish(category_id: int):
    """
    Workflow to fetch data, generate content, and publish a blog.
    """
    # Fetch and summarize RSS content
    # context = fetch_rss_data(topic)
    category = fetch_category(category_id)
    category_name = category[0]["name"]
    print(category_name)
    context = fetch_category_rss(category_id)

    # Generate blog content using LangChain
    prompt = generate_prompt(category_name, context)
    blog_content = generate_blog_with_chain(prompt)

    summary = summarize_with_chain(blog_content, True)
    title = title_with_chain(summary)


    # Publish to TinaCMS
    # publish_blog(category_name, title, blog_content, summary)

    print({"title": title, "content": blog_content, "summary": summary})

    return {"title": title, "content": blog_content, "summary": summary}

# process_and_publish(11)

# process_and_publish("Life and Evolution")



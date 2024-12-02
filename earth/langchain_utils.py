import time

import anthropic
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_ollama import ChatOllama, OllamaLLM
from langchain_anthropic import ChatAnthropic

# Initialize the OpenAI LLM
# llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.7)
# llm = ChatOllama(model="mistral:latest", temperature=0.7)

summarising_llm = ChatAnthropic(model="claude-3-5-haiku-20241022", temperature=0.3)
title_llm = ChatAnthropic(model="claude-3-5-haiku-20241022", temperature=0.8)
blog_llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0.7)

# summarising_llm = OllamaLLM(model="llama3.2:latest", temperature=0.1)
# title_llm = OllamaLLM(model="llama3.2:latest", temperature=0.1)
# blog_llm = OllamaLLM(model="llama3.2:latest", temperature=0.5)

SHORT_SUMMARY_PROMPT = """
Summarize the following article in 40-50 words:
{content}

Only provide summary of the article and no additional text like 'Here is the summary', 'Summary of the content', etc.

Summary:
"""

SUMMARY_PROMPT = """
Summarize the following article:
{content}
Summary:
"""


def summarize_with_chain(content: str, short: bool) -> str:
    """
    Summarize content using a LangChain summarization chain.
    """
    print(f"Summarizing content")
    if short:
        prompt = PromptTemplate(
            input_variables=["content"],
            template=SHORT_SUMMARY_PROMPT,
        )
    else:
        prompt = PromptTemplate(
            input_variables=["content"],
            template=SUMMARY_PROMPT,
        )
    # prompt = PromptTemplate(
    #     input_variables=["content"],
    #     template="Summarize the following article:\n\n{content}\n\nSummary:",
    # )
    chain = prompt | summarising_llm
    result = chain.invoke({"content": content})
    print(result)
    return result.content


def generate_blog_with_chain(prompt: str) -> str:
    """
    Generate blog content using a LangChain chain.
    """
    print(f"Generating blog with prompt: {prompt}")
    prompt_template = PromptTemplate(input_variables=["prompt"], template="{prompt}")
    # print("Generated Prompt ---", prompt1)
    chain = prompt_template | blog_llm
    max_retries = 5
    backoff_factor = 2
    for attempt in range(max_retries):
        try:
            blog = chain.invoke({"prompt": prompt})
            return blog.content
        except anthropic.InternalServerError as e:
            if 'overloaded' in str(e).lower():
                wait_time = backoff_factor ** attempt
                print(f"Anthropic API overloaded. Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                raise e
    raise RetryException("Failed to generate blog content after multiple retries due to API overload.")


def title_with_chain(summary: str) -> str:
    """
    Summarize content using a LangChain summarization chain.
    """
    print(f"Getting Title for the Blog Post")
    prompt = PromptTemplate(
        input_variables=["summary"],
        template="Generate single journal title for:\n\n{summary}\n\nDo not provide any other information except the title. Final answer should be only a title with maximum 10 words.\n\nTitle:",
    )
    chain = prompt | title_llm
    result = chain.invoke({"content": summary})
    return result.content


class RetryException(Exception):
    pass

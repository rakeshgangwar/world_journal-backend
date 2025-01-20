# World Journal Backend

## Overview

World Journal Backend is a FastAPI-based service designed to fetch RSS feeds by category, process their content using AI-powered tools, and publish them as blog posts. Leveraging LangChain with Anthropic's Claude models, the backend ensures high-quality, engaging content generation. It integrates with Supabase for data management and utilizes GitHub's API for publishing content to the CMS. The application is containerized using Docker for easy deployment and scalability.

## Features

- **RSS Feed Management**: Fetch and manage RSS feeds categorized by topics.
- **AI-Powered Content Generation**: Utilize LangChain and Anthropic's Claude models to summarize and generate blog content.
- **Automated Publishing**: Publish generated blog posts to TinaCMS via GitHub API.
- **Scheduling**: Automate content fetching and publishing at regular intervals using APScheduler.
- **RESTful API**: Expose endpoints to interact with feeds and publishing workflows.
- **Database Integration**: Use Supabase for managing feed data and categories.

## Technologies Used

- **Backend Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **AI Models**: [LangChain](https://langchain.com/), [Anthropic Claude](https://www.anthropic.com/)
- **Database**: [Supabase](https://supabase.com/)
- **ORM**: [SQLAlchemy](https://www.sqlalchemy.org/)
- **Containerization**: [Docker](https://www.docker.com/)
- **Scheduling**: [APScheduler](https://apscheduler.readthedocs.io/)
- **Version Control**: [GitHub](https://github.com/)

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/get-started) installed on your machine.
- [Git](https://git-scm.com/) installed.
- Access to [Supabase](https://supabase.com/) and [GitHub](https://github.com/) accounts.
- API keys for OpenAI, Anthropic, and TinaCMS.

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/rakeshgangwar/world-journal-backend.git
   cd world-journal-backend
   ```

2. **Set Up Environment Variables**

   Create a `.env` file based on the provided `.env.example`:

   ```bash
   cp .env.example .env
   ```

   Populate the `.env` file with your credentials:

   ```env
   OPENAI_API_KEY=your_openai_api_key
   ANTHROPIC_API_KEY=your_anthropic_api_key
   TINA_API_URL=your_tina_api_url
   TINA_API_TOKEN=your_tina_api_token
   GITHUB_TOKEN=your_github_token
   DATABASE_URL=your_supabase_database_url
   SUPABASE_URL=your_supabase_url
   SUPABASE_API_KEY=your_supabase_api_key
   ```

3. **Build and Run the Application with Docker**

   ```bash
   docker-compose up --build
   ```

   The backend service will be accessible at `http://localhost:8000`.

### Running Locally Without Docker

1. **Create a Virtual Environment**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install Dependencies**

   ```bash
   pip install poetry
   poetry install
   ```

3. **Initialize the Database**

   ```bash
   poetry run python -c "from database import init_db; init_db()"
   ```

4. **Run the Application**

   ```bash
   poetry run uvicorn main:app --reload
   ```

## Usage

### API Endpoints

- **GET /**

  Check if the backend is running.

  **Response:**

  ```json
  {
    "message": "Earth Journal Backend with LangGraph is running."
  }
  ```

- **GET /feeds**

  Retrieve all available feeds.

- **GET /feeds/{category_id}/**

  Retrieve feeds based on a specific category ID.

- **POST /publish/**

  Publish a new blog entry by providing a category ID.

  **Request Body:**

  ```json
  {
    "category_id": 1
  }
  ```

  **Response:**

  ```json
  {
    "status": "Processing",
    "title": "Generated Title",
    "content": "Generated blog content",
    "summary": "Generated summary"
  }
  ```

### Scheduling

The application uses APScheduler to automate the publishing process. A background scheduler is set to run the `publish_random_topic` job every 4 hours, selecting a random topic from the available feeds and processing it.

### Publishing Workflow

1. **Fetch Feeds**: Retrieve RSS feeds based on the selected category.
2. **Scrape Content**: Extract and scrape content from feed entries.
3. **Summarize Content**: Use LangChain and Anthropic's models to summarize the scraped content.
4. **Generate Blog Post**: Create a blog post with a generated title, content, and summary.
5. **Publish**: Use GitHub API to publish the generated blog post to TinaCMS.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- [FastAPI](https://fastapi.tiangolo.com/): Modern, fast (high-performance) web framework for building APIs with Python.
- [LangChain](https://langchain.com/): A framework for developing applications powered by language models.
- [Anthropic](https://www.anthropic.com/): Creators of the Claude family of language models.
- [Supabase](https://supabase.com/): The open-source Firebase alternative. 
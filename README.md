# FastAPI Scraper Project
This project is a FastAPI application that integrates with Redis for caching. It can be run both with and without Docker. This README provides instructions for both methods.

## Prerequisites

- Python 3.11 or higher
- Docker (for Docker setup)

## Running without docker
- [Create a virtual env and activate it](https://docs.python.org/3/library/venv.html)
- Install all dependencies. (pip install -r requirements.txt)
- Install redis and make sure redis is running on the system
- uvicorn app.main:app --reload    -> Use this for local testing and running
- uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4 - Use this for deployed version

## Running with docker
- [Install Docker](https://docs.docker.com/engine/install/)
- docker-compose build
- docker compose up
# Stratigo Backend

This repository contains the backend for the Stratigo project. The backend is responsible for processing requests and integrating with various language models and external services.

## Features

- **FastAPI-based RESTful API**: High-performance, modern API with automatic OpenAPI documentation.
- **LangChain Integration**: Connects to various AI models and tools using LangChain.
- **Telegram Integration**: Supports sending notifications via Telegram.
- **OpenAPI Documentation**: Built-in interactive API documentation at `/api/v1/docs`.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.8 or higher
- `pip` for managing Python packages

## Installation

To install and set up the project locally:

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd saas-template/backend
   ```

2. **Create and activate virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in the backend directory with your configuration:
   ```
   
   ```

4. **Run the development server:**
   ```bash
   uvicorn main:app --reload
   ```

5. **Access the API documentation:**
   Open your browser and go to [http://localhost:8000/api/v1/docs](http://localhost:8000/api/v1/docs)

## Deployment

For production deployment, you can use Gunicorn with Uvicorn workers:

```bash
gunicorn -c gunicorn_config.py main:app
```

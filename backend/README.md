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
   Create a `.env` file in the backend directory with your configuration.
   
   For local Supabase development, get the JWT keys by running:
   ```bash
   npx supabase status --output json
   ```
   
   Copy the `ANON_KEY` and `SERVICE_ROLE_KEY` values (these are JWT tokens starting with `eyJ`).
   **Important**: Do NOT use the `SECRET_KEY` or `PUBLISHABLE_KEY` - those are CLI keys, not API keys.
   
   Example `.env` file:
   ```env
   ENVIRONMENT=development
   FRONTEND_URL=http://localhost:5173
   SUPABASE_URL=http://127.0.0.1:54321
   SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
   SUPABASE_SERVICE_ROLE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
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

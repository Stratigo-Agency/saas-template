import os
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import uvicorn

load_dotenv()

# Environment configuration
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
FRONTEND_URL = os.getenv('FRONTEND_URL', 'http://localhost:5173')

ALLOWED_ORIGINS = [FRONTEND_URL]
if ENVIRONMENT == 'production':
    ALLOWED_ORIGINS.append('https://www.google.com')  # TODO: Change to the production URL

app = FastAPI(
    title="SaaS API",
    description="API for SaaS application",
    version="1.0.0",
    docs_url="/api/v1/docs",
    openapi_url="/apispec.json"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/")
async def health_check():
    """Health check endpoint for Digital Ocean."""
    return HTMLResponse(status_code=200)

# Import and include routers
from routes.sample_route import router as sample_router
from routes.auth_route import router as auth_router

app.include_router(sample_router, prefix="/sample", tags=["Sample"])
app.include_router(auth_router, prefix="/auth", tags=["Auth"])

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  # Digital Ocean often uses port 8000
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=ENVIRONMENT == 'development'
    ) 
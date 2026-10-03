import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from app.core.config import settings
from app.core.database import engine, Base
from app.api import (
    auth, profile, code, knowledge, vault, chat, plan, assessment, career, aptitude, interview, admin, health
)

# Initialize database schema
Base.metadata.create_all(bind=engine)

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="CodePilot: An AI that knows what you know. Private personal technical AI companion & Knowledge Vault for consistent developers.",
    version="1.0.0"
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global error handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": f"Internal server error: {str(exc)}"}
    )

# Include API Routers
app.include_router(health.router)
app.include_router(auth.router, prefix="/api")
app.include_router(profile.router, prefix="/api")
app.include_router(code.router, prefix="/api")
app.include_router(knowledge.router, prefix="/api")
app.include_router(vault.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(plan.router, prefix="/api")
app.include_router(assessment.router, prefix="/api")
app.include_router(career.router, prefix="/api")
app.include_router(aptitude.router, prefix="/api")
app.include_router(interview.router, prefix="/api")
app.include_router(admin.router, prefix="/api")

# Serve uploaded files safely
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

@app.get("/")
def root():
    return {
        "project": settings.PROJECT_NAME,
        "tagline": settings.PROJECT_TAGLINE,
        "docs_url": "/docs",
        "api_v1": "/api"
    }

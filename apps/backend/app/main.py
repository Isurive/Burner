# FastAPI app + routers mounting
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import profile, job, resume, cover_letter, form, autofill, alignment
from app.core.config import settings
from app.core.logging import setup_logging

setup_logging()

app = FastAPI(
    title="OB Agent API",
    description="AI-powered job application assistant backend",
    version="0.1.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount routers
app.include_router(profile.router, prefix="/profile", tags=["profile"])
app.include_router(job.router, prefix="/job", tags=["job"])
app.include_router(resume.router, prefix="/resume", tags=["resume"])
app.include_router(cover_letter.router, prefix="/cover-letter", tags=["cover-letter"])
app.include_router(form.router, prefix="/form", tags=["form"])
app.include_router(autofill.router, prefix="/autofill", tags=["autofill"])
app.include_router(alignment.router, prefix="/alignment", tags=["alignment"])

@app.get("/")
async def root():
    return {"message": "OB Agent API", "version": "0.1.0"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from app.database import Base, engine
from app.models.user import User
from app.models.paper import Paper
from app.routers.auth import router as auth_router
from app.routers.papers import router as papers_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Research Paper Assistant",
    version="1.0.0"
)

# Configure CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(papers_router)

@app.get("/")
def home():
    return {
        "message": "Research Paper Assistant Backend Running"
    }
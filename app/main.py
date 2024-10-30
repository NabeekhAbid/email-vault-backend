# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base
from .routes import user
# Create the database tables if they don't exist
Base.metadata.create_all(bind=engine)
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins or specify a list of allowed origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)
app.include_router(user.router, prefix="/api", tags=["users"])
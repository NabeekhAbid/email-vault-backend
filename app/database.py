from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Define the database URL using environment variables
DATABASE_URL = os.getenv('DATABASE_URL', 'mysql+pymysql://root:rootpassword@localhost/vault')

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a base class for declarative models
Base = declarative_base()

# Create a session local class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency for getting the database session
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

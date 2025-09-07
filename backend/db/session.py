# backend/db/session.py (Updated)

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .pii_db import Base as PiiBase
from .key_db import Base as KeyBase
from dotenv import load_dotenv

# Load environment variables from a .env file for local development
load_dotenv()

# --- Production-Ready Database Configuration ---
# In production, Render will provide these full URLs as environment variables.
# For local development, you'll add these to your .env file.
PII_DB_URL = os.getenv("PII_DATABASE_URL")
KEY_DB_URL = os.getenv("KEY_DATABASE_URL")

# --- Verification ---
# A simple check to ensure the variables are loaded.
if not PII_DB_URL or not KEY_DB_URL:
    raise ValueError("Database URLs are not configured. Please set PII_DATABASE_URL and KEY_DATABASE_URL environment variables.")

# Create the SQLAlchemy engines using the full URLs
pii_engine = create_engine(PII_DB_URL)
key_engine = create_engine(KEY_DB_URL)

PiiSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=pii_engine)
KeySessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=key_engine)

def init_db():
    print("Initializing MySQL tables...")
    PiiBase.metadata.create_all(bind=pii_engine)
    KeyBase.metadata.create_all(bind=key_engine)
    print("Tables initialized.")

# --- Dependency Injection Functions (No changes needed here) ---

def get_pii_db():
    db = PiiSessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_key_db():
    db = KeySessionLocal()
    try:
        yield db
    finally:
        db.close()
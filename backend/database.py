from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import HTTPException
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

# Always try MySQL first if configured, then fallback to SQLite
mysql_available = False
if DATABASE_URL and DATABASE_URL.startswith("mysql"):
    # DATABASE_URL is set to MySQL - test it
    try:
        test_engine = create_engine(DATABASE_URL, pool_pre_ping=True, connect_args={"connect_timeout": 1})
        with test_engine.connect() as conn:
            pass
        mysql_available = True
        print("✅ Using MySQL database (from DATABASE_URL)")
    except Exception:
        mysql_available = False
        print("⚠️  MySQL connection failed, falling back to SQLite")
        DATABASE_URL = None  # Clear it so we use SQLite

if not DATABASE_URL:
    # Try MySQL first
    db_user = os.getenv("DB_USER", "root")
    db_password = os.getenv("DB_PASSWORD", "")
    db_host = os.getenv("DB_HOST", "localhost")
    db_port = os.getenv("DB_PORT", "3306")
    db_name = os.getenv("DB_NAME", "ai_news_agency")
    mysql_url = f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    
    # Try MySQL connection (quick test)
    if not mysql_available:
        try:
            test_engine = create_engine(mysql_url, pool_pre_ping=True, connect_args={"connect_timeout": 1})
            with test_engine.connect() as conn:
                pass
            mysql_available = True
            DATABASE_URL = mysql_url
            print("✅ Using MySQL database")
        except Exception:
            mysql_available = False
    
    # Fallback to SQLite if MySQL not available
    if not mysql_available:
        db_path = Path(__file__).parent.parent / "ai_news_agency.db"
        # Use absolute path with forward slashes for SQLite (handles spaces in path)
        db_path_str = str(db_path.absolute()).replace("\\", "/")
        DATABASE_URL = f"sqlite:///{db_path_str}"
        print(f"⚠️  MySQL not available, using SQLite: {db_path}")
        print("✅ SQLite database will be created automatically (no installation needed)")

# Create engine
try:
    if DATABASE_URL.startswith("sqlite"):
        engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=False)
    else:
        engine = create_engine(DATABASE_URL, pool_pre_ping=True, pool_recycle=300, connect_args={"connect_timeout": 2})
    
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    # Test connection
    with engine.connect() as conn:
        pass
    DB_AVAILABLE = True
    db_type = "SQLite" if DATABASE_URL.startswith("sqlite") else "MySQL"
    print(f"✅ Database connection successful ({db_type})")
except Exception as e:
    print(f"⚠️  Database not available: {e}")
    print("⚠️  Server will run in memory-only mode (data won't be persisted)")
    DB_AVAILABLE = False
    engine = None
    SessionLocal = None

Base = declarative_base()

# Auto-create tables will be done in main.py after all models are imported

def get_db():
    """Dependency for getting database session"""
    if not DB_AVAILABLE or SessionLocal is None:
        raise HTTPException(status_code=503, detail="Database not available. Please check database connection.")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


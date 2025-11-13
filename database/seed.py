"""
Seed script for initial database data
"""
import sys
import os
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

from sqlalchemy.orm import Session
from backend.database import SessionLocal, engine, Base
from backend.models import Source

def seed_sources():
    """Seed initial source data"""
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    
    try:
        # Check if sources already exist
        existing = db.query(Source).count()
        if existing > 0:
            print("Sources already seeded. Skipping...")
            return
        
        # Default sources from Event Registry example
        sources = [
            Source(
                name="United States",
                uri="http://en.wikipedia.org/wiki/United_States"
            ),
            Source(
                name="Canada",
                uri="http://en.wikipedia.org/wiki/Canada"
            ),
            Source(
                name="United Kingdom",
                uri="http://en.wikipedia.org/wiki/United_Kingdom"
            ),
        ]
        
        for source in sources:
            db.add(source)
        
        db.commit()
        print(f"Seeded {len(sources)} sources successfully!")
        
    except Exception as e:
        print(f"Error seeding sources: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_sources()


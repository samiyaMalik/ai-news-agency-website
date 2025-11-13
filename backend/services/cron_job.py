"""
Optional: Daily cron job to fetch news for popular keywords
Run this script daily using a scheduler (cron, APScheduler, Celery, etc.)
"""
import asyncio
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.services.event_registry import EventRegistryService
from backend.database import SessionLocal
from backend.models import Article, Source

# Popular keywords to fetch daily
POPULAR_KEYWORDS = [
    "technology",
    "business",
    "sports",
    "politics",
    "health",
    "science"
]

async def fetch_daily_news():
    """Fetch news for popular keywords and store in database"""
    event_registry = EventRegistryService()
    db = SessionLocal()
    
    try:
        total_fetched = 0
        
        for keyword in POPULAR_KEYWORDS:
            print(f"Fetching news for keyword: {keyword}")
            
            try:
                # Fetch articles
                fetched_articles = await event_registry.fetch_articles(
                    keyword=keyword,
                    articles_count=20,  # Fetch 20 articles per keyword
                    articles_page=1
                )
                
                for article_data in fetched_articles:
                    # Check if article already exists
                    existing_article = db.query(Article).filter(
                        Article.title == article_data["title"]
                    ).first()
                    
                    if existing_article:
                        continue
                    
                    # Handle source
                    source = None
                    if article_data.get("source_name"):
                        source = db.query(Source).filter(
                            Source.name == article_data["source_name"]
                        ).first()
                        
                        if not source:
                            source = Source(
                                name=article_data["source_name"],
                                uri=article_data.get("source_uri")
                            )
                            db.add(source)
                            db.flush()
                    
                    # Create article
                    article = Article(
                        title=article_data["title"],
                        content=article_data.get("content"),
                        image_url=article_data.get("image_url"),
                        published_date=article_data.get("published_date"),
                        source_id=source.id if source else None
                    )
                    
                    db.add(article)
                    total_fetched += 1
                
                db.commit()
                print(f"Fetched {len(fetched_articles)} articles for '{keyword}'")
                
            except Exception as e:
                print(f"Error fetching news for '{keyword}': {e}")
                db.rollback()
                continue
        
        print(f"\nTotal new articles fetched: {total_fetched}")
        
    except Exception as e:
        print(f"Error in daily news fetch: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(fetch_daily_news())


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from backend.database import get_db, DB_AVAILABLE
from backend.models import Article, Source
from backend.schemas import NewsFetchRequest, NewsFetchResponse, Article as ArticleSchema
from backend.services.event_registry import EventRegistryService

router = APIRouter()

@router.post("/news/fetch", response_model=NewsFetchResponse)
async def fetch_news(
    request: NewsFetchRequest,
    db: Optional[Session] = Depends(get_db)
):
    """Fetch news articles from Event Registry API and store in database"""
    event_registry = EventRegistryService()
    
    try:
        # Fetch articles from Event Registry
        fetched_articles = await event_registry.fetch_articles(
            keyword=request.keyword,
            articles_count=request.articles_count,
            articles_page=request.articles_page
        )
        
        stored_articles = []
        
        # Try to save to database if available
        if db:
            try:
                for article_data in fetched_articles:
                    # Check if article already exists (by title)
                    existing_article = db.query(Article).filter(
                        Article.title == article_data["title"]
                    ).first()
                    
                    if existing_article:
                        stored_articles.append(existing_article)
                        continue
                    
                    # Handle source
                    source = None
                    if article_data.get("source_name"):
                        source = db.query(Source).filter(
                            Source.name == article_data["source_name"]
                        ).first()
                        
                        if not source:
                            # Create new source
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
                    stored_articles.append(article)
                
                db.commit()
                
                # Refresh articles to get IDs
                for article in stored_articles:
                    db.refresh(article)
            except Exception as db_error:
                # If database fails, return articles without saving
                try:
                    db.rollback()
                except:
                    pass
                print(f"Database error (returning articles without saving): {db_error}")
                # Convert to dict format
                stored_articles = []
                for idx, article_data in enumerate(fetched_articles, 1):
                    source_dict = None
                    if article_data.get("source_name"):
                        source_dict = {
                            "id": idx,
                            "name": article_data.get("source_name"),
                            "uri": article_data.get("source_uri"),
                            "created_at": article_data.get("published_date"),
                            "updated_at": None
                        }
                    article_dict = {
                        "id": idx,
                        "title": article_data["title"],
                        "content": article_data.get("content"),
                        "image_url": article_data.get("image_url"),
                        "published_date": article_data.get("published_date"),
                        "source": source_dict,
                        "source_id": None,
                        "ai_summary": None,
                        "ai_tags": None,
                        "ai_caption": None,
                        "ai_image_prompt": None,
                        "created_at": article_data.get("published_date"),
                        "updated_at": None
                    }
                    stored_articles.append(article_dict)
        else:
            # Database not available - return articles in memory format
            stored_articles = []
            for idx, article_data in enumerate(fetched_articles, 1):
                source_dict = None
                if article_data.get("source_name"):
                    source_dict = {
                        "id": idx,
                        "name": article_data.get("source_name"),
                        "uri": article_data.get("source_uri"),
                        "created_at": article_data.get("published_date"),
                        "updated_at": None
                    }
                article_dict = {
                    "id": idx,
                    "title": article_data["title"],
                    "content": article_data.get("content"),
                    "image_url": article_data.get("image_url"),
                    "published_date": article_data.get("published_date"),
                    "source": source_dict,
                    "source_id": None,
                    "ai_summary": None,
                    "ai_tags": None,
                    "ai_caption": None,
                    "ai_image_prompt": None,
                    "created_at": article_data.get("published_date"),
                    "updated_at": None
                }
                stored_articles.append(article_dict)
        
        return NewsFetchResponse(
            articles=stored_articles,
            total_fetched=len(stored_articles),
            keyword=request.keyword
        )
        
    except Exception as e:
        if db:
            try:
                db.rollback()
            except:
                pass
        raise HTTPException(status_code=500, detail=f"Error fetching news: {str(e)}")


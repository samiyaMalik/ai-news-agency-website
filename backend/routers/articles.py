from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, or_
from typing import Optional, List
from datetime import datetime
from backend.database import DB_AVAILABLE

from backend.database import get_db
from backend.models import Article, Source, AIMetadata
from backend.schemas import (
    Article as ArticleSchema,
    ArticleCreate,
    ArticleUpdate,
    ArticleListResponse,
    SemanticSearchRequest,
    SemanticSearchResponse,
    SemanticSearchResult,
    SocialPostResponse
)
from backend.services.openai_service import OpenAIService
from backend.services.pinecone_service import PineconeService

router = APIRouter()

@router.get("/articles", response_model=ArticleListResponse)
async def get_articles(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = None,
    source_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Get all articles with pagination and filtering"""
    if not db:
        raise HTTPException(status_code=503, detail="Database not available")
    query = db.query(Article)
    
    # Apply filters
    if search:
        query = query.filter(
            or_(
                Article.title.contains(search),
                Article.content.contains(search),
                Article.ai_summary.contains(search)
            )
        )
    
    if source_id:
        query = query.filter(Article.source_id == source_id)
    
    # Get total count
    total = query.count()
    
    # Apply pagination and ordering
    articles = query.order_by(desc(Article.published_date)).offset((page - 1) * page_size).limit(page_size).all()
    
    total_pages = (total + page_size - 1) // page_size
    
    return ArticleListResponse(
        articles=articles,
        total=total,
        page=page,
        page_size=page_size,
        total_pages=total_pages
    )

@router.get("/articles/{article_id}", response_model=ArticleSchema)
async def get_article(article_id: int, db: Session = Depends(get_db)):
    """Get a single article by ID"""
    if not db:
        raise HTTPException(status_code=503, detail="Database not available")
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    return article

@router.post("/articles", response_model=ArticleSchema, status_code=201)
async def create_article(article_data: ArticleCreate, db: Session = Depends(get_db)):
    """Create a new article"""
    if not db:
        raise HTTPException(status_code=503, detail="Database not available")
    # Handle source
    source = None
    if article_data.source_id:
        source = db.query(Source).filter(Source.id == article_data.source_id).first()
    elif article_data.source_name:
        # Find or create source by name
        source = db.query(Source).filter(Source.name == article_data.source_name).first()
        if not source:
            source = Source(name=article_data.source_name)
            db.add(source)
            db.flush()
    
    # Create article
    article = Article(
        title=article_data.title,
        content=article_data.content,
        image_url=article_data.image_url,
        published_date=article_data.published_date,
        source_id=source.id if source else None
    )
    
    db.add(article)
    db.commit()
    db.refresh(article)
    return article

@router.put("/articles/{article_id}", response_model=ArticleSchema)
async def update_article(
    article_id: int,
    article_data: ArticleUpdate,
    db: Session = Depends(get_db)
):
    """Update an article"""
    if not db:
        raise HTTPException(status_code=503, detail="Database not available")
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    # Update fields
    update_data = article_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(article, field, value)
    
    db.commit()
    db.refresh(article)
    return article

@router.delete("/articles/{article_id}", status_code=204)
async def delete_article(article_id: int, db: Session = Depends(get_db)):
    """Delete an article"""
    if not db:
        raise HTTPException(status_code=503, detail="Database not available")
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    db.delete(article)
    db.commit()
    return None

@router.post("/articles/{article_id}/process-ai", response_model=ArticleSchema)
async def process_article_ai(article_id: int, db: Session = Depends(get_db)):
    """Process article through AI pipeline"""
    if not db:
        raise HTTPException(status_code=503, detail="Database not available. SQLite database should be created automatically.")
    
    # Get article from database
    article = db.query(Article).filter(Article.id == article_id).first()
    
    # If article not in database
    if not article:
        raise HTTPException(
            status_code=404, 
            detail=f"Article with ID {article_id} not found. Please fetch news first to save articles to database."
        )
    
    try:
        openai_service = OpenAIService()
    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"OpenAI service error: {str(e)}")
    
    try:
        pinecone_service = PineconeService()
    except (ValueError, Exception) as e:
        raise HTTPException(status_code=500, detail=f"Pinecone service error: {str(e)}")
    
    # Generate AI content
    ai_summary = await openai_service.generate_summary(article.title, article.content or "")
    ai_tags = await openai_service.generate_tags(article.title, article.content or "")
    ai_caption = await openai_service.generate_caption(article.title, article.content or "")
    ai_image_prompt = await openai_service.generate_image_prompt(article.title, article.content or "")
    
    # Update article
    article.ai_summary = ai_summary
    article.ai_tags = ai_tags
    article.ai_caption = ai_caption
    article.ai_image_prompt = ai_image_prompt
    
    # Generate embedding
    embedding = await openai_service.generate_embedding(article.title + " " + (article.content or ""))
    
    # Store in Pinecone
    try:
        embedding_id = await pinecone_service.upsert_embedding(
            article_id=article_id,
            embedding=embedding,
            metadata={
                "title": article.title,
                "article_id": article_id,
                "source_id": article.source_id
            }
        )
        
        # Update or create AI metadata
        ai_metadata = db.query(AIMetadata).filter(AIMetadata.article_id == article_id).first()
        if not ai_metadata:
            ai_metadata = AIMetadata(article_id=article_id, embedding_id=embedding_id)
            db.add(ai_metadata)
        else:
            ai_metadata.embedding_id = embedding_id
    except Exception as e:
        print(f"Warning: Could not store embedding: {e}")
    
    db.commit()
    db.refresh(article)
    
    return article

@router.get("/articles/{article_id}/related", response_model=List[ArticleSchema])
async def get_related_articles(
    article_id: int,
    top_k: int = Query(5, ge=1, le=20),
    db: Session = Depends(get_db)
):
    """Get related articles using semantic search"""
    if not db:
        raise HTTPException(status_code=503, detail="Database not available")
    article = db.query(Article).filter(Article.id == article_id).first()
    if not article:
        raise HTTPException(status_code=404, detail="Article not found")
    
    ai_metadata = db.query(AIMetadata).filter(AIMetadata.article_id == article_id).first()
    if not ai_metadata or not ai_metadata.embedding_id:
        raise HTTPException(status_code=404, detail="Article embedding not found. Please process article with AI first.")
    
    try:
        pinecone_service = PineconeService()
    except (ValueError, Exception) as e:
        raise HTTPException(status_code=500, detail=f"Pinecone service error: {str(e)}")
    
    try:
        openai_service = OpenAIService()
    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"OpenAI service error: {str(e)}")
    
    # Get article embedding from Pinecone
    embedding = await pinecone_service.get_embedding(ai_metadata.embedding_id)
    if not embedding:
        raise HTTPException(status_code=404, detail="Embedding not found in vector database")
    
    # Search for similar articles
    similar_results = await pinecone_service.search_similar(
        embedding=embedding,
        top_k=top_k + 1,  # +1 to exclude the article itself
        exclude_ids=[article_id]
    )
    
    # Get article IDs from results
    article_ids = [result["article_id"] for result in similar_results]
    
    # Fetch articles from database
    articles = db.query(Article).filter(Article.id.in_(article_ids)).all()
    
    # Sort by similarity score
    article_dict = {a.id: a for a in articles}
    sorted_articles = [article_dict[result["article_id"]] for result in similar_results if result["article_id"] in article_dict]
    
    return sorted_articles

@router.post("/articles/semantic-search", response_model=SemanticSearchResponse)
async def semantic_search(
    request: SemanticSearchRequest,
    db: Session = Depends(get_db)
):
    """Semantic search for articles using vector similarity"""
    if not db:
        raise HTTPException(status_code=503, detail="Database not available")
    try:
        openai_service = OpenAIService()
    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"OpenAI service error: {str(e)}")
    
    try:
        pinecone_service = PineconeService()
    except (ValueError, Exception) as e:
        raise HTTPException(status_code=500, detail=f"Pinecone service error: {str(e)}")
    
    # Generate embedding for query
    query_embedding = await openai_service.generate_embedding(request.query)
    
    # Search in Pinecone
    search_results = await pinecone_service.search_similar(
        embedding=query_embedding,
        top_k=request.top_k
    )
    
    # Get article IDs
    article_ids = [result["article_id"] for result in search_results]
    
    # Fetch articles from database
    articles = db.query(Article).filter(Article.id.in_(article_ids)).all()
    article_dict = {a.id: a for a in articles}
    
    # Build response with similarity scores
    results = []
    for result in search_results:
        article_id = result["article_id"]
        if article_id in article_dict:
            results.append(SemanticSearchResult(
                article=article_dict[article_id],
                similarity_score=result["score"]
            ))
    
    return SemanticSearchResponse(
        results=results,
        query=request.query,
        total_results=len(results)
    )

@router.get("/articles/{article_id}/social-post", response_model=SocialPostResponse)
async def get_social_post(article_id: int, db: Session = Depends(get_db)):
    """Get social media post (caption and image) for an article"""
    if not db:
        raise HTTPException(status_code=503, detail="Database not available")
    
    article = db.query(Article).filter(Article.id == article_id).first()
    
    if not article:
        raise HTTPException(
            status_code=404, 
            detail="Article not found. Please ensure article is saved in database."
        )
    
    try:
        openai_service = OpenAIService()
    except ValueError as e:
        raise HTTPException(status_code=500, detail=f"OpenAI service error: {str(e)}")
    
    # Generate caption if not exists
    if not article.ai_caption:
        article.ai_caption = await openai_service.generate_caption(article.title, article.content or "")
        if db:
            db.commit()
    
    # Generate image prompt if not exists
    if not article.ai_image_prompt:
        article.ai_image_prompt = await openai_service.generate_image_prompt(article.title, article.content or "")
        if db:
            db.commit()
    
    # Always generate image (DALL·E)
    image_url = None
    if article.ai_image_prompt:
        try:
            print(f"Generating DALL·E image with prompt: {article.ai_image_prompt[:100]}...")
            image_url = await openai_service.generate_image(article.ai_image_prompt)
            if image_url:
                print(f"✅ Image generated successfully: {image_url[:50]}...")
            else:
                print("⚠️ Image generation returned None")
        except Exception as e:
            print(f"❌ Error generating image: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("⚠️ No image prompt available for image generation")
    
    return SocialPostResponse(
        caption=article.ai_caption or article.title,
        image_url=image_url,
        image_prompt=article.ai_image_prompt
    )


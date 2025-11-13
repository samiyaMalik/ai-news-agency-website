from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Source Schemas
class SourceBase(BaseModel):
    name: str
    uri: Optional[str] = None

class SourceCreate(SourceBase):
    pass

class Source(SourceBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# Article Schemas
class ArticleBase(BaseModel):
    title: str
    content: Optional[str] = None
    image_url: Optional[str] = None
    published_date: Optional[datetime] = None
    source_id: Optional[int] = None

class ArticleCreate(ArticleBase):
    source_name: Optional[str] = None

class ArticleUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    image_url: Optional[str] = None
    published_date: Optional[datetime] = None
    ai_summary: Optional[str] = None
    ai_tags: Optional[List[str]] = None
    ai_caption: Optional[str] = None
    ai_image_prompt: Optional[str] = None

class Article(ArticleBase):
    id: int
    ai_summary: Optional[str] = None
    ai_tags: Optional[List[str]] = None
    ai_caption: Optional[str] = None
    ai_image_prompt: Optional[str] = None
    source: Optional[Source] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class ArticleListResponse(BaseModel):
    articles: List[Article]
    total: int
    page: int
    page_size: int
    total_pages: int

# AI Metadata Schemas
class AIMetadataBase(BaseModel):
    embedding_id: Optional[str] = None
    similarity_scores: Optional[dict] = None

class AIMetadata(AIMetadataBase):
    id: int
    article_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# News Fetching Schemas
class NewsFetchRequest(BaseModel):
    keyword: str = Field(..., description="Search keyword for news articles")
    articles_count: int = Field(default=100, ge=1, le=100, description="Number of articles to fetch")
    articles_page: int = Field(default=1, ge=1, description="Page number")

class NewsFetchResponse(BaseModel):
    articles: List[Article]
    total_fetched: int
    keyword: str

# Semantic Search Schemas
class SemanticSearchRequest(BaseModel):
    query: str = Field(..., description="Search query text")
    top_k: int = Field(default=10, ge=1, le=50, description="Number of results to return")

class SemanticSearchResult(BaseModel):
    article: Article
    similarity_score: float

class SemanticSearchResponse(BaseModel):
    results: List[SemanticSearchResult]
    query: str
    total_results: int

# Social Post Schemas
class SocialPostResponse(BaseModel):
    caption: str
    image_url: Optional[str] = None
    image_prompt: Optional[str] = None


from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from backend.database import Base

class Source(Base):
    __tablename__ = "sources"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    uri = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship
    articles = relationship("Article", back_populates="source", cascade="all, delete-orphan")

class Article(Base):
    __tablename__ = "articles"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(500), nullable=False, index=True)
    content = Column(Text, nullable=True)
    image_url = Column(String(1000), nullable=True)
    published_date = Column(DateTime(timezone=True), nullable=True, index=True)
    source_id = Column(Integer, ForeignKey("sources.id"), nullable=True)
    
    # AI-generated fields
    ai_summary = Column(Text, nullable=True)
    ai_tags = Column(JSON, nullable=True)  # Store as JSON array
    ai_caption = Column(Text, nullable=True)
    ai_image_prompt = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    source = relationship("Source", back_populates="articles")
    ai_metadata = relationship("AIMetadata", back_populates="article", uselist=False, cascade="all, delete-orphan")

class AIMetadata(Base):
    __tablename__ = "ai_metadata"
    
    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("articles.id"), unique=True, nullable=False)
    embedding_id = Column(String(255), nullable=True, index=True)  # Pinecone vector ID
    similarity_scores = Column(JSON, nullable=True)  # Store similarity scores for related articles
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationship
    article = relationship("Article", back_populates="ai_metadata")


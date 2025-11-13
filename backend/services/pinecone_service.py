import os
from typing import List, Dict, Optional
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

load_dotenv()

class PineconeService:
    """Service for Pinecone vector database operations"""
    
    def __init__(self):
        api_key = os.getenv("PINECONE_API_KEY")
        if not api_key:
            raise ValueError("PINECONE_API_KEY environment variable is required")
        
        self.pc = Pinecone(api_key=api_key)
        # Get index name from environment variable (required)
        provided_index = os.getenv("PINECONE_INDEX_NAME")
        if not provided_index:
            raise ValueError("PINECONE_INDEX_NAME environment variable is required")
        
        # Check available indexes
        try:
            available_indexes = list(self.pc.list_indexes())
            index_names = [idx.name for idx in available_indexes]
            
            # Use provided index if exists, otherwise use first available or create new
            if provided_index in index_names:
                self.index_name = provided_index
            elif index_names:
                # Use first available index
                self.index_name = index_names[0]
                print(f"⚠️  Using available index: {self.index_name} (instead of {provided_index})")
            else:
                self.index_name = provided_index
        except:
            self.index_name = provided_index
        
        self.dimension = 1024  # Pinecone index dimension (llama-text-embed-v2)
        
        # Try to get or create index
        try:
            # First, try to get existing index
            self.index = self.pc.Index(self.index_name)
            print(f"✅ Connected to Pinecone index: {self.index_name}")
        except Exception as e:
            # If index doesn't exist, try to create it
            print(f"⚠️  Index {self.index_name} not found. Attempting to create...")
            try:
                self.pc.create_index(
                    name=self.index_name,
                    dimension=self.dimension,
                    metric="cosine",
                    spec=ServerlessSpec(
                        cloud="aws",
                        region=os.getenv("PINECONE_ENVIRONMENT", "us-east-1")
                    )
                )
                print(f"✅ Created new Pinecone index: {self.index_name}")
                # Wait a bit for index to be ready
                import time
                time.sleep(2)
                self.index = self.pc.Index(self.index_name)
            except Exception as create_error:
                print(f"❌ Could not create index: {create_error}")
                print(f"⚠️  Pinecone operations will fail. Please create index manually: {self.index_name}")
                raise ValueError(f"Pinecone index {self.index_name} not found and could not be created: {create_error}")
    
    async def upsert_embedding(
        self,
        article_id: int,
        embedding: List[float],
        metadata: Optional[Dict] = None
    ) -> str:
        """
        Store or update embedding in Pinecone
        
        Args:
            article_id: Article ID
            embedding: Embedding vector
            metadata: Additional metadata to store
        
        Returns:
            Vector ID (embedding_id)
        """
        vector_id = f"article_{article_id}"
        
        # Prepare metadata
        if metadata is None:
            metadata = {}
        metadata["article_id"] = article_id
        
        # Upsert to Pinecone
        self.index.upsert(
            vectors=[{
                "id": vector_id,
                "values": embedding,
                "metadata": metadata
            }]
        )
        
        return vector_id
    
    async def get_embedding(self, embedding_id: str) -> Optional[List[float]]:
        """Retrieve embedding vector by ID"""
        try:
            result = self.index.fetch(ids=[embedding_id])
            if embedding_id in result["vectors"]:
                return result["vectors"][embedding_id]["values"]
            return None
        except Exception as e:
            print(f"Error fetching embedding: {e}")
            return None
    
    async def search_similar(
        self,
        embedding: List[float],
        top_k: int = 10,
        exclude_ids: Optional[List[int]] = None,
        filter_dict: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Search for similar articles using vector similarity
        
        Args:
            embedding: Query embedding vector
            top_k: Number of results to return
            exclude_ids: Article IDs to exclude from results
            filter_dict: Additional metadata filters
        
        Returns:
            List of results with article_id and score
        """
        try:
            # Build filter
            query_filter = filter_dict or {}
            if exclude_ids:
                # Pinecone doesn't support NOT directly, so we'll filter after
                pass
            
            # Perform search
            results = self.index.query(
                vector=embedding,
                top_k=top_k * 2 if exclude_ids else top_k,  # Get more to filter
                include_metadata=True,
                filter=query_filter if query_filter else None
            )
            
            # Process results
            similar_articles = []
            for match in results["matches"]:
                article_id = match["metadata"].get("article_id")
                
                # Skip excluded IDs
                if exclude_ids and article_id in exclude_ids:
                    continue
                
                if article_id:
                    similar_articles.append({
                        "article_id": article_id,
                        "score": match["score"],
                        "metadata": match["metadata"]
                    })
                
                # Stop when we have enough results
                if len(similar_articles) >= top_k:
                    break
            
            return similar_articles
            
        except Exception as e:
            print(f"Error searching similar articles: {e}")
            return []
    
    async def delete_embedding(self, embedding_id: str):
        """Delete embedding from Pinecone"""
        try:
            self.index.delete(ids=[embedding_id])
        except Exception as e:
            print(f"Error deleting embedding: {e}")
    
    async def delete_by_article_id(self, article_id: int):
        """Delete embedding by article ID"""
        embedding_id = f"article_{article_id}"
        await self.delete_embedding(embedding_id)


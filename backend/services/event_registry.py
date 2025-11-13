import httpx
import os
from typing import List, Dict, Optional
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

class EventRegistryService:
    """Service for fetching news articles from Event Registry API"""
    
    def __init__(self):
        self.api_key = os.getenv("EVENT_REGISTRY_API_KEY")
        if not self.api_key:
            raise ValueError("EVENT_REGISTRY_API_KEY environment variable is required")
        self.base_url = "https://eventregistry.org/api/v1/article/getArticles"
        self.timeout = 30.0
    
    async def fetch_articles(
        self,
        keyword: str,
        articles_count: int = 100,
        articles_page: int = 1,
        source_locations: Optional[List[str]] = None
    ) -> List[Dict]:
        """
        Fetch articles from Event Registry API
        
        Args:
            keyword: Search keyword
            articles_count: Number of articles to fetch (max 100)
            articles_page: Page number
            source_locations: List of source location URIs (optional)
        
        Returns:
            List of article dictionaries
        """
        if source_locations is None:
            source_locations = [
                "http://en.wikipedia.org/wiki/United_States",
                "http://en.wikipedia.org/wiki/Canada",
                "http://en.wikipedia.org/wiki/United_Kingdom"
            ]
        
        request_body = {
            "action": "getArticles",
            "keyword": keyword,
            "sourceLocationUri": source_locations,
            "ignoreSourceGroupUri": "paywall/paywalled_sources",
            "articlesPage": articles_page,
            "articlesCount": min(articles_count, 100),  # API limit
            "articlesSortBy": "date",
            "articlesSortByAsc": False,
            "dataType": ["news", "pr"],
            "forceMaxDataTimeWindow": 31,
            "resultType": "articles",
            "apiKey": self.api_key
        }
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(self.base_url, json=request_body)
                response.raise_for_status()
                data = response.json()
                
                # Parse articles from response
                articles = []
                if "articles" in data and "results" in data["articles"]:
                    for article_data in data["articles"]["results"]:
                        parsed_article = self._parse_article(article_data)
                        if parsed_article:
                            articles.append(parsed_article)
                
                return articles
                
        except httpx.HTTPError as e:
            raise Exception(f"Error fetching articles from Event Registry: {str(e)}")
        except Exception as e:
            raise Exception(f"Unexpected error: {str(e)}")
    
    def _parse_article(self, article_data: Dict) -> Optional[Dict]:
        """Parse article data from Event Registry response"""
        try:
            # Extract title
            title = article_data.get("title", "").strip()
            if not title:
                return None
            
            # Extract content/body
            body = article_data.get("body", "")
            if not body:
                body = article_data.get("text", "")
            
            # Extract image
            image_url = None
            if "images" in article_data and len(article_data["images"]) > 0:
                image_url = article_data["images"][0].get("url")
            
            # Extract published date
            published_date = None
            if "date" in article_data:
                try:
                    # Event Registry returns date in various formats
                    date_str = article_data["date"]
                    if isinstance(date_str, str):
                        # Try parsing common formats
                        for fmt in ["%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"]:
                            try:
                                published_date = datetime.strptime(date_str, fmt)
                                break
                            except ValueError:
                                continue
                except Exception:
                    pass
            
            # Extract source
            source_name = None
            source_uri = None
            if "source" in article_data:
                source_info = article_data["source"]
                if isinstance(source_info, dict):
                    source_name = source_info.get("title") or source_info.get("name")
                    source_uri = source_info.get("uri")
                elif isinstance(source_info, str):
                    source_name = source_info
            
            # Extract URL
            url = article_data.get("url", "")
            
            return {
                "title": title,
                "content": body,
                "image_url": image_url,
                "published_date": published_date,
                "source_name": source_name,
                "source_uri": source_uri,
                "url": url,
                "raw_data": article_data  # Keep raw data for reference
            }
            
        except Exception as e:
            print(f"Error parsing article: {e}")
            return None


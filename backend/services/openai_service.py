import os
from typing import List, Optional
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

class OpenAIService:
    """Service for OpenAI API interactions"""
    
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        self.client = AsyncOpenAI(api_key=api_key)
        self.model = "gpt-4-turbo-preview"  # or "gpt-3.5-turbo" for faster/cheaper
        self.embedding_model = "text-embedding-3-small"  # or "text-embedding-ada-002"
    
    async def generate_summary(self, title: str, content: str) -> str:
        """Generate a concise summary of the article"""
        prompt = f"""Write a concise, informative summary of the following news article in 2-3 sentences.

Title: {title}

Content: {content[:2000]}

Summary:"""
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional news summarizer. Create clear, concise summaries."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating summary: {e}")
            return f"Summary of: {title}"
    
    async def generate_tags(self, title: str, content: str) -> List[str]:
        """Generate SEO tags/keywords for the article"""
        prompt = f"""Extract 5-10 relevant keywords/tags for this news article. Return only a comma-separated list of tags, no explanations.

Title: {title}

Content: {content[:2000]}

Tags:"""
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an SEO expert. Extract relevant keywords and tags."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.5
            )
            tags_str = response.choices[0].message.content.strip()
            # Parse comma-separated tags
            tags = [tag.strip() for tag in tags_str.split(",") if tag.strip()]
            return tags[:10]  # Limit to 10 tags
        except Exception as e:
            print(f"Error generating tags: {e}")
            return []
    
    async def generate_caption(self, title: str, content: str) -> str:
        """Generate an engaging social media caption"""
        prompt = f"""Create an engaging social media caption for this news article. Make it:
- 1-2 sentences
- Attention-grabbing
- Include relevant hashtags (3-5)
- Suitable for Twitter, Facebook, LinkedIn

Title: {title}

Content: {content[:2000]}

Caption:"""
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a social media content creator. Write engaging captions."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.8
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating caption: {e}")
            return f"Check out: {title}"
    
    async def generate_image_prompt(self, title: str, content: str) -> str:
        """Generate a detailed image prompt for DALL·E"""
        prompt = f"""Create a detailed, vivid image generation prompt for DALL·E based on this news article. The prompt should:
- Be specific and descriptive
- Include visual elements, style, and mood
- Be suitable for a news article thumbnail
- Be 1-2 sentences

Title: {title}

Content: {content[:2000]}

Image Prompt:"""
        
        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert at creating detailed image generation prompts."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error generating image prompt: {e}")
            return f"News article illustration about {title}"
    
    async def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding vector for text (1024 dimensions for Pinecone compatibility)"""
        try:
            # Truncate text if too long (embedding models have token limits)
            max_chars = 8000  # Safe limit for most embedding models
            text = text[:max_chars]
            
            # Use text-embedding-3-small with dimension reduction to 1024
            # If dimension parameter is not supported, we'll use the full embedding and truncate
            try:
                response = await self.client.embeddings.create(
                    model="text-embedding-3-small",
                    input=text,
                    dimensions=1024  # Match Pinecone index dimension
                )
                return response.data[0].embedding
            except Exception as dim_error:
                # Fallback: use default embedding and truncate/pad to 1024
                print(f"Warning: Could not set dimensions to 1024, using default: {dim_error}")
                response = await self.client.embeddings.create(
                    model="text-embedding-3-small",
                    input=text
                )
                embedding = response.data[0].embedding
                # Truncate or pad to 1024 dimensions
                if len(embedding) > 1024:
                    return embedding[:1024]
                elif len(embedding) < 1024:
                    # Pad with zeros (not ideal, but works)
                    return embedding + [0.0] * (1024 - len(embedding))
                return embedding
        except Exception as e:
            print(f"Error generating embedding: {e}")
            raise
    
    async def generate_image(self, prompt: str) -> Optional[str]:
        """Generate an image using DALL·E"""
        try:
            print(f"🎨 Calling DALL·E API with prompt: {prompt[:100]}...")
            response = await self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                n=1,
                size="1024x1024",
                quality="standard"
            )
            
            if response and response.data and len(response.data) > 0:
                image_url = response.data[0].url
                print(f"✅ DALL·E image generated successfully: {image_url[:50]}...")
                return image_url
            else:
                print("⚠️ DALL·E response is empty")
                return None
        except Exception as e:
            print(f"❌ Error generating DALL·E image: {e}")
            import traceback
            traceback.print_exc()
            return None


import { useState, useEffect } from 'react';
import { Article, processArticleAI, getSocialPost } from '../lib/api';
import { format } from 'date-fns';
import SocialPostModal from './SocialPostModal';
import Link from 'next/link';

interface ArticleCardProps {
  article: Article;
  onUpdate?: (updatedArticle: Article) => void;
}

export default function ArticleCard({ article, onUpdate }: ArticleCardProps) {
  const [currentArticle, setCurrentArticle] = useState<Article>(article);
  const [processingAI, setProcessingAI] = useState(false);
  const [showSocialModal, setShowSocialModal] = useState(false);
  const [socialPost, setSocialPost] = useState<{ caption: string; image_url?: string } | null>(null);
  const [loadingSocial, setLoadingSocial] = useState(false);

  // Update local state when article prop changes
  useEffect(() => {
    setCurrentArticle(article);
  }, [article]);

  const handleProcessAI = async () => {
    setProcessingAI(true);
    try {
      const updatedArticle = await processArticleAI(currentArticle.id);
      if (updatedArticle) {
        // Update local state immediately
        setCurrentArticle(updatedArticle);
        // Update parent component's article state without reloading
        if (onUpdate) {
          onUpdate(updatedArticle);
        }
        // Show success message
        alert('Article processed with AI successfully! Summary, tags, and caption generated.');
      }
    } catch (error: any) {
      console.error('Error processing article with AI:', error);
      const errorMsg = error.response?.data?.detail || error.message || 'Failed to process article with AI.';
      if (errorMsg.includes('Database not available')) {
        alert('Database is required for AI processing. Please ensure database is connected.');
      } else {
        alert(`Error: ${errorMsg}`);
      }
    } finally {
      setProcessingAI(false);
    }
  };

  const handleGenerateSocialPost = async () => {
    setLoadingSocial(true);
    setShowSocialModal(true);
    // Show modal immediately with loading state
    setSocialPost({
      caption: currentArticle.ai_caption || currentArticle.title,
      image_url: undefined, // Will be updated when image is generated
    });
    
    try {
      console.log('🔄 Generating social post for article:', currentArticle.id);
      const post = await getSocialPost(currentArticle.id);
      console.log('✅ Social post generated:', { 
        hasCaption: !!post.caption, 
        hasImage: !!post.image_url 
      });
      
      setSocialPost({
        caption: post.caption || currentArticle.ai_caption || currentArticle.title,
        image_url: post.image_url || undefined,
      });
      
      if (!post.image_url) {
        console.warn('⚠️ No image URL returned from API');
      }
    } catch (error: any) {
      console.error('❌ Error generating social post:', error);
      const errorMsg = error.response?.data?.detail || error.message || 'Failed to generate social post.';
      
      // Still show modal with available data
      setSocialPost({
        caption: currentArticle.ai_caption || currentArticle.title,
        image_url: undefined,
      });
      
      if (!errorMsg.includes('not found') && !errorMsg.includes('AI')) {
        alert(`Error generating social post: ${errorMsg}`);
      }
    } finally {
      setLoadingSocial(false);
    }
  };

  const formatDate = (dateString?: string) => {
    if (!dateString) return 'Date not available';
    try {
      return format(new Date(dateString), 'MMM dd, yyyy');
    } catch {
      return dateString;
    }
  };

  return (
    <>
      <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-xl transition-shadow duration-300">
        {/* Image */}
        {currentArticle.image_url ? (
          <div className="relative w-full h-48 bg-gray-200 overflow-hidden">
            <img
              src={currentArticle.image_url}
              alt={currentArticle.title}
              className="w-full h-full object-cover"
              loading="lazy"
              onError={(e) => {
                const target = e.target as HTMLImageElement;
                target.style.display = 'none';
                // Show placeholder
                const parent = target.parentElement;
                if (parent) {
                  parent.innerHTML = '<div class="w-full h-full flex items-center justify-center text-gray-400"><svg class="w-16 h-16" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg></div>';
                }
              }}
            />
          </div>
        ) : (
          <div className="w-full h-48 bg-gray-200 flex items-center justify-center">
            <svg className="w-16 h-16 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"></path>
            </svg>
          </div>
        )}

        {/* Content */}
        <div className="p-6">
          {/* Source and Date */}
          <div className="flex items-center justify-between text-sm text-gray-500 mb-2">
            <span>{currentArticle.source?.name || 'Unknown Source'}</span>
            <span>{formatDate(currentArticle.published_date)}</span>
          </div>

          {/* Title */}
          <Link href={`/articles/${currentArticle.id}`}>
            <h3 className="text-xl font-bold text-gray-900 mb-3 hover:text-primary-600 transition-colors cursor-pointer line-clamp-2">
              {currentArticle.title}
            </h3>
          </Link>

          {/* AI Summary or Content Preview */}
          {currentArticle.ai_summary ? (
            <p className="text-gray-600 mb-4 line-clamp-3">{currentArticle.ai_summary}</p>
          ) : currentArticle.content ? (
            <p className="text-gray-600 mb-4 line-clamp-3">{currentArticle.content.substring(0, 200)}...</p>
          ) : null}

          {/* AI Tags */}
          {currentArticle.ai_tags && currentArticle.ai_tags.length > 0 && (
            <div className="flex flex-wrap gap-2 mb-4">
              {currentArticle.ai_tags.slice(0, 5).map((tag, index) => (
                <span
                  key={index}
                  className="px-2 py-1 bg-primary-100 text-primary-700 text-xs rounded-full"
                >
                  {tag}
                </span>
              ))}
            </div>
          )}

          {/* Actions */}
          <div className="flex gap-2 mt-4">
            <button
              onClick={handleProcessAI}
              disabled={processingAI}
              className="flex-1 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors text-sm font-medium"
            >
              {processingAI ? 'Processing...' : currentArticle.ai_summary ? 'Re-process with AI' : 'Process with AI'}
            </button>
            <button
              onClick={handleGenerateSocialPost}
              disabled={loadingSocial}
              className="flex-1 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors text-sm font-medium"
            >
              {loadingSocial ? 'Generating...' : 'Generate Social Post'}
            </button>
          </div>
        </div>
      </div>

      {/* Social Post Modal */}
      {showSocialModal && (
        <SocialPostModal
          caption={socialPost?.caption || currentArticle.ai_caption || ''}
          imageUrl={socialPost?.image_url}
          onClose={() => {
            setShowSocialModal(false);
            setSocialPost(null);
          }}
        />
      )}
    </>
  );
}


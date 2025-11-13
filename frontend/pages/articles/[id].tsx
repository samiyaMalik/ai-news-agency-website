import { useRouter } from 'next/router';
import { useState, useEffect } from 'react';
import { getArticle, getRelatedArticles, Article } from '../../lib/api';
import { format } from 'date-fns';
import Head from 'next/head';
import Link from 'next/link';
import Image from 'next/image';
import RelatedArticles from '../../components/RelatedArticles';

export default function ArticleDetail() {
  const router = useRouter();
  const { id } = router.query;
  const [article, setArticle] = useState<Article | null>(null);
  const [relatedArticles, setRelatedArticles] = useState<Article[]>([]);
  const [loading, setLoading] = useState(true);
  const [loadingRelated, setLoadingRelated] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (id) {
      loadArticle();
    }
  }, [id]);

  const loadArticle = async () => {
    try {
      setLoading(true);
      const articleData = await getArticle(Number(id));
      setArticle(articleData);
      
      // Load related articles if AI metadata exists
      if (articleData.ai_summary) {
        loadRelatedArticles();
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load article');
    } finally {
      setLoading(false);
    }
  };

  const loadRelatedArticles = async () => {
    try {
      setLoadingRelated(true);
      const related = await getRelatedArticles(Number(id), 5);
      setRelatedArticles(related);
    } catch (err: any) {
      console.error('Error loading related articles:', err);
    } finally {
      setLoadingRelated(false);
    }
  };

  const formatDate = (dateString?: string) => {
    if (!dateString) return 'Date not available';
    try {
      return format(new Date(dateString), 'MMMM dd, yyyy');
    } catch {
      return dateString;
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
          <p className="mt-4 text-gray-600">Loading article...</p>
        </div>
      </div>
    );
  }

  if (error || !article) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="text-center">
          <p className="text-xl text-red-600 mb-4">{error || 'Article not found'}</p>
          <Link href="/" className="text-primary-600 hover:underline">
            ← Back to Home
          </Link>
        </div>
      </div>
    );
  }

  return (
    <>
      <Head>
        <title>{article.title} - AI News Agency</title>
        <meta name="description" content={article.ai_summary || article.content?.substring(0, 160)} />
      </Head>

      <main className="min-h-screen bg-gray-50">
        <div className="container mx-auto px-4 py-8 max-w-4xl">
          {/* Back Button */}
          <Link
            href="/"
            className="inline-flex items-center text-primary-600 hover:text-primary-700 mb-6"
          >
            ← Back to Home
          </Link>

          {/* Article */}
          <article className="bg-white rounded-lg shadow-lg overflow-hidden">
            {/* Image */}
            {article.image_url && (
              <div className="relative w-full h-96">
                <Image
                  src={article.image_url}
                  alt={article.title}
                  fill
                  className="object-cover"
                />
              </div>
            )}

            {/* Content */}
            <div className="p-8">
              {/* Meta */}
              <div className="flex items-center justify-between text-sm text-gray-500 mb-4">
                <span>{article.source?.name || 'Unknown Source'}</span>
                <span>{formatDate(article.published_date)}</span>
              </div>

              {/* Title */}
              <h1 className="text-4xl font-bold text-gray-900 mb-4">
                {article.title}
              </h1>

              {/* AI Tags */}
              {article.ai_tags && article.ai_tags.length > 0 && (
                <div className="flex flex-wrap gap-2 mb-6">
                  {article.ai_tags.map((tag, index) => (
                    <span
                      key={index}
                      className="px-3 py-1 bg-primary-100 text-primary-700 text-sm rounded-full"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              )}

              {/* AI Summary */}
              {article.ai_summary && (
                <div className="bg-blue-50 border-l-4 border-primary-500 p-4 mb-6">
                  <h2 className="font-semibold text-gray-900 mb-2">AI Summary</h2>
                  <p className="text-gray-700">{article.ai_summary}</p>
                </div>
              )}

              {/* Content */}
              {article.content && (
                <div className="prose max-w-none mb-6">
                  <p className="text-gray-700 leading-relaxed whitespace-pre-wrap">
                    {article.content}
                  </p>
                </div>
              )}

              {/* AI Caption Preview */}
              {article.ai_caption && (
                <div className="mt-8 pt-6 border-t border-gray-200">
                  <h3 className="font-semibold text-gray-900 mb-2">Social Media Caption</h3>
                  <p className="text-gray-600 italic">{article.ai_caption}</p>
                </div>
              )}
            </div>
          </article>

          {/* Related Articles */}
          {article.ai_summary && (
            <RelatedArticles
              articleId={article.id}
              relatedArticles={relatedArticles}
              loading={loadingRelated}
              onLoadMore={loadRelatedArticles}
            />
          )}
        </div>
      </main>
    </>
  );
}


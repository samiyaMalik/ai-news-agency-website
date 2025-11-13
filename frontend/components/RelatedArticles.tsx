import { Article } from '../lib/api';
import ArticleCard from './ArticleCard';
import Link from 'next/link';

interface RelatedArticlesProps {
  articleId: number;
  relatedArticles: Article[];
  loading: boolean;
  onLoadMore: () => void;
}

export default function RelatedArticles({
  articleId,
  relatedArticles,
  loading,
  onLoadMore,
}: RelatedArticlesProps) {
  if (loading && relatedArticles.length === 0) {
    return (
      <div className="mt-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Related Articles</h2>
        <div className="text-center py-8">
          <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
          <p className="mt-2 text-gray-600">Finding related articles...</p>
        </div>
      </div>
    );
  }

  if (relatedArticles.length === 0) {
    return null;
  }

  return (
    <div className="mt-8">
      <h2 className="text-2xl font-bold text-gray-900 mb-4">Related Articles</h2>
      <p className="text-gray-600 mb-6">
        Discover similar articles using AI-powered semantic search
      </p>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {relatedArticles
          .filter((article) => article.id !== articleId)
          .slice(0, 6)
          .map((article) => (
            <ArticleCard key={article.id} article={article} />
          ))}
      </div>
    </div>
  );
}


import { useState } from 'react';
import { fetchNews, Article } from '../lib/api';
import ArticleCard from '../components/ArticleCard';
import Head from 'next/head';

export default function Home() {
  const [keyword, setKeyword] = useState('');
  const [articles, setArticles] = useState<Article[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [searchPerformed, setSearchPerformed] = useState(false);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!keyword.trim()) return;

    setLoading(true);
    setError(null);
    setSearchPerformed(true);

    try {
      const response = await fetchNews({
        keyword: keyword.trim(),
        articles_count: 100,
        articles_page: 1,
      });
      setArticles(response.articles);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch news articles');
      setArticles([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Head>
        <title>AI News Agency</title>
        <meta name="description" content="AI-powered news agency with semantic search" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        <div className="container mx-auto px-4 py-8">
          {/* Header */}
          <div className="text-center mb-8">
            <h1 className="text-5xl font-bold text-gray-900 mb-2">
              AI News Agency
            </h1>
            <p className="text-xl text-gray-600">
              Discover news powered by AI and semantic search
            </p>
          </div>

          {/* Search Form */}
          <div className="max-w-2xl mx-auto mb-8">
            <form onSubmit={handleSearch} className="flex gap-4">
              <input
                type="text"
                value={keyword}
                onChange={(e) => setKeyword(e.target.value)}
                placeholder="Enter keyword (e.g., India, Technology, Sports...)"
                className="flex-1 px-6 py-4 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent text-lg text-gray-900 bg-white placeholder-gray-500"
                disabled={loading}
              />
              <button
                type="submit"
                disabled={loading || !keyword.trim()}
                className="px-8 py-4 bg-primary-600 text-white rounded-lg font-semibold hover:bg-primary-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
              >
                {loading ? 'Searching...' : 'Search'}
              </button>
            </form>
          </div>

          {/* Error Message */}
          {error && (
            <div className="max-w-2xl mx-auto mb-6 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg">
              {error}
            </div>
          )}

          {/* Loading State */}
          {loading && (
            <div className="text-center py-12">
              <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
              <p className="mt-4 text-gray-600">Fetching news articles...</p>
            </div>
          )}

          {/* Results */}
          {!loading && searchPerformed && (
            <div className="mb-6 text-center">
              <p className="text-lg text-gray-700">
                Found <span className="font-bold text-primary-600">{articles.length}</span> articles
              </p>
            </div>
          )}

          {/* Articles Grid */}
          {!loading && articles.length > 0 && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {articles.map((article) => (
                <ArticleCard 
                  key={article.id} 
                  article={article}
                  onUpdate={(updatedArticle) => {
                    // Update article in the list without reloading
                    setArticles(prevArticles =>
                      prevArticles.map(a =>
                        a.id === updatedArticle.id ? updatedArticle : a
                      )
                    );
                  }}
                />
              ))}
            </div>
          )}

          {/* No Results */}
          {!loading && searchPerformed && articles.length === 0 && !error && (
            <div className="text-center py-12">
              <p className="text-xl text-gray-600">No articles found for "{keyword}"</p>
              <p className="text-gray-500 mt-2">Try a different keyword</p>
            </div>
          )}

          {/* Initial State */}
          {!searchPerformed && !loading && (
            <div className="text-center py-12">
              <div className="max-w-md mx-auto">
                <div className="text-6xl mb-4">📰</div>
                <h2 className="text-2xl font-semibold text-gray-800 mb-2">
                  Search for News Articles
                </h2>
                <p className="text-gray-600">
                  Enter a keyword above to fetch the latest news articles from Event Registry.
                  Each article can be processed with AI to generate summaries, tags, and social media content.
                </p>
              </div>
            </div>
          )}
        </div>
      </main>
    </>
  );
}


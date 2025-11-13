"""
Initial database schema migration
Creates sources, articles, and ai_metadata tables
"""
from sqlalchemy import text

def upgrade(connection):
    """Create initial schema"""
    # Create sources table
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS sources (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            uri VARCHAR(500),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_name (name)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """))
    
    # Create articles table
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS articles (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(500) NOT NULL,
            content TEXT,
            image_url VARCHAR(1000),
            published_date DATETIME,
            source_id INT,
            ai_summary TEXT,
            ai_tags JSON,
            ai_caption TEXT,
            ai_image_prompt TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_title (title(255)),
            INDEX idx_published_date (published_date),
            INDEX idx_source_id (source_id),
            FOREIGN KEY (source_id) REFERENCES sources(id) ON DELETE SET NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """))
    
    # Create ai_metadata table
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS ai_metadata (
            id INT AUTO_INCREMENT PRIMARY KEY,
            article_id INT NOT NULL UNIQUE,
            embedding_id VARCHAR(255),
            similarity_scores JSON,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_embedding_id (embedding_id),
            INDEX idx_article_id (article_id),
            FOREIGN KEY (article_id) REFERENCES articles(id) ON DELETE CASCADE
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """))

def downgrade(connection):
    """Drop all tables"""
    connection.execute(text("DROP TABLE IF EXISTS ai_metadata;"))
    connection.execute(text("DROP TABLE IF EXISTS articles;"))
    connection.execute(text("DROP TABLE IF EXISTS sources;"))


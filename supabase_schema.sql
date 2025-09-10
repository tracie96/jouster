
CREATE TABLE IF NOT EXISTS analyses (
    id SERIAL PRIMARY KEY,
    original_text TEXT NOT NULL,
    summary TEXT NOT NULL,
    title VARCHAR(255),
    topics JSONB NOT NULL,
    sentiment VARCHAR(20) NOT NULL CHECK (sentiment IN ('positive', 'neutral', 'negative')),
    keywords JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_analyses_created_at ON analyses(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_analyses_sentiment ON analyses(sentiment);
CREATE INDEX IF NOT EXISTS idx_analyses_topics ON analyses USING GIN(topics);
CREATE INDEX IF NOT EXISTS idx_analyses_keywords ON analyses USING GIN(keywords);


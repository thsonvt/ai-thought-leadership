-- Supabase RPC function for semantic search
-- Run this in Supabase SQL Editor: Database → SQL Editor → New Query

-- Function: match_articles
-- Performs vector similarity search using pgvector
CREATE OR REPLACE FUNCTION match_articles(
    query_embedding VECTOR(1536),
    match_threshold FLOAT DEFAULT 0.5,
    match_count INT DEFAULT 10,
    filter_authors TEXT[] DEFAULT NULL,
    filter_topics TEXT[] DEFAULT NULL,
    filter_diataxis_type TEXT DEFAULT NULL,
    filter_date_from DATE DEFAULT NULL,
    filter_date_to DATE DEFAULT NULL
)
RETURNS TABLE (
    id UUID,
    url TEXT,
    title TEXT,
    author TEXT,
    author_id TEXT,
    published DATE,
    summary TEXT,
    topics TEXT[],
    key_quotes JSONB,
    diataxis_type TEXT,
    tags TEXT[],
    similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        a.id,
        a.url,
        a.title,
        a.author,
        a.author_id,
        a.published,
        a.summary,
        a.topics,
        a.key_quotes,
        a.diataxis_type,
        a.tags,
        1 - (a.embedding <=> query_embedding) AS similarity
    FROM articles a
    WHERE
        -- Similarity threshold
        1 - (a.embedding <=> query_embedding) > match_threshold
        -- Optional author filter
        AND (filter_authors IS NULL OR a.author_id = ANY(filter_authors))
        -- Optional topic filter (array overlap)
        AND (filter_topics IS NULL OR a.topics && filter_topics)
        -- Optional diataxis type filter
        AND (filter_diataxis_type IS NULL OR a.diataxis_type = filter_diataxis_type)
        -- Optional date range filters
        AND (filter_date_from IS NULL OR a.published >= filter_date_from)
        AND (filter_date_to IS NULL OR a.published <= filter_date_to)
    ORDER BY similarity DESC
    LIMIT match_count;
END;
$$;

-- Grant execute permission to anon role (for API access)
GRANT EXECUTE ON FUNCTION match_articles TO anon;
GRANT EXECUTE ON FUNCTION match_articles TO authenticated;

-- Example usage:
-- SELECT * FROM match_articles(
--     '[0.1, 0.2, ...]'::vector(1536),  -- query embedding
--     0.5,                               -- threshold
--     10,                                -- limit
--     ARRAY['dan-shipper-every'],        -- authors filter
--     ARRAY['Claude Code'],              -- topics filter
--     'explanation',                     -- diataxis filter
--     '2026-01-01',                      -- date from
--     NULL                               -- date to
-- );

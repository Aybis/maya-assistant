-- Migration Script: Add Memory System to Existing Database
-- Safe to run multiple times (idempotent)

-- ============================================================================
-- STEP 1: Alter existing tables to add new columns
-- ============================================================================

-- Add new columns to conversations table
DO $$
BEGIN
    -- Add summary column if it doesn't exist
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'conversations' AND column_name = 'summary'
    ) THEN
        ALTER TABLE conversations ADD COLUMN summary TEXT;
    END IF;

    -- Add tags column if it doesn't exist
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'conversations' AND column_name = 'tags'
    ) THEN
        ALTER TABLE conversations ADD COLUMN tags TEXT[] DEFAULT '{}';
    END IF;

    -- Add message_count column if it doesn't exist
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.columns
        WHERE table_name = 'conversations' AND column_name = 'message_count'
    ) THEN
        ALTER TABLE conversations ADD COLUMN message_count INTEGER DEFAULT 0;
    END IF;
END $$;

-- Update messages role constraint to include 'system'
DO $$
BEGIN
    -- Drop old constraint if it exists
    IF EXISTS (
        SELECT 1 FROM information_schema.constraint_column_usage
        WHERE table_name = 'messages' AND constraint_name = 'messages_role_check'
    ) THEN
        ALTER TABLE messages DROP CONSTRAINT messages_role_check;
    END IF;

    -- Add new constraint
    ALTER TABLE messages ADD CONSTRAINT messages_role_check
    CHECK (role IN ('user', 'assistant', 'system'));
EXCEPTION
    WHEN duplicate_object THEN NULL;
END $$;

-- ============================================================================
-- STEP 2: Create new tables
-- ============================================================================

-- User Memory table
CREATE TABLE IF NOT EXISTS user_memory (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE NOT NULL,
  memory_type VARCHAR(50) NOT NULL CHECK (memory_type IN ('preference', 'fact', 'goal', 'context', 'interest')),
  key TEXT NOT NULL,
  value TEXT NOT NULL,
  confidence DECIMAL(3,2) DEFAULT 1.0 CHECK (confidence >= 0 AND confidence <= 1),
  source_conversation_id UUID REFERENCES conversations(id) ON DELETE SET NULL,
  metadata JSONB DEFAULT '{}',
  last_accessed_at TIMESTAMP DEFAULT NOW(),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(user_id, key)
);

-- Conversation Summaries table
CREATE TABLE IF NOT EXISTS conversation_summaries (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE NOT NULL UNIQUE,
  short_summary TEXT NOT NULL,
  detailed_summary TEXT,
  key_topics TEXT[] DEFAULT '{}',
  entities JSONB DEFAULT '{}',
  sentiment VARCHAR(20) CHECK (sentiment IN ('positive', 'neutral', 'negative', 'mixed')),
  importance_score DECIMAL(3,2) DEFAULT 0.5 CHECK (importance_score >= 0 AND importance_score <= 1),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Memory Context table
CREATE TABLE IF NOT EXISTS memory_context (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE NOT NULL,
  memory_id UUID REFERENCES user_memory(id) ON DELETE CASCADE NOT NULL,
  relevance_score DECIMAL(3,2) DEFAULT 0.5 CHECK (relevance_score >= 0 AND relevance_score <= 1),
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(conversation_id, memory_id)
);

-- ============================================================================
-- STEP 3: Create indexes
-- ============================================================================

-- Indexes for conversations (only new ones)
CREATE INDEX IF NOT EXISTS idx_conversations_tags ON conversations USING GIN(tags);

-- Indexes for user_memory
CREATE INDEX IF NOT EXISTS idx_user_memory_user_id ON user_memory(user_id);
CREATE INDEX IF NOT EXISTS idx_user_memory_type ON user_memory(memory_type);
CREATE INDEX IF NOT EXISTS idx_user_memory_last_accessed ON user_memory(last_accessed_at DESC);

-- Indexes for conversation_summaries
CREATE INDEX IF NOT EXISTS idx_conversation_summaries_conversation_id ON conversation_summaries(conversation_id);
CREATE INDEX IF NOT EXISTS idx_conversation_summaries_importance ON conversation_summaries(importance_score DESC);
CREATE INDEX IF NOT EXISTS idx_conversation_summaries_topics ON conversation_summaries USING GIN(key_topics);

-- Indexes for memory_context
CREATE INDEX IF NOT EXISTS idx_memory_context_conversation_id ON memory_context(conversation_id);
CREATE INDEX IF NOT EXISTS idx_memory_context_memory_id ON memory_context(memory_id);
CREATE INDEX IF NOT EXISTS idx_memory_context_relevance ON memory_context(relevance_score DESC);

-- ============================================================================
-- STEP 4: Enable Row Level Security
-- ============================================================================

ALTER TABLE user_memory ENABLE ROW LEVEL SECURITY;
ALTER TABLE conversation_summaries ENABLE ROW LEVEL SECURITY;
ALTER TABLE memory_context ENABLE ROW LEVEL SECURITY;

-- ============================================================================
-- STEP 5: Create RLS Policies
-- ============================================================================

-- User Memory Policies
DO $$
BEGIN
    -- Drop existing policies if they exist
    DROP POLICY IF EXISTS "Users can view their own memory" ON user_memory;
    DROP POLICY IF EXISTS "Users can insert their own memory" ON user_memory;
    DROP POLICY IF EXISTS "Users can update their own memory" ON user_memory;
    DROP POLICY IF EXISTS "Users can delete their own memory" ON user_memory;

    -- Create policies
    CREATE POLICY "Users can view their own memory"
      ON user_memory FOR SELECT
      USING (auth.uid() = user_id);

    CREATE POLICY "Users can insert their own memory"
      ON user_memory FOR INSERT
      WITH CHECK (auth.uid() = user_id);

    CREATE POLICY "Users can update their own memory"
      ON user_memory FOR UPDATE
      USING (auth.uid() = user_id);

    CREATE POLICY "Users can delete their own memory"
      ON user_memory FOR DELETE
      USING (auth.uid() = user_id);
END $$;

-- Conversation Summaries Policies
DO $$
BEGIN
    DROP POLICY IF EXISTS "Users can view summaries from their conversations" ON conversation_summaries;
    DROP POLICY IF EXISTS "Service can manage conversation summaries" ON conversation_summaries;

    CREATE POLICY "Users can view summaries from their conversations"
      ON conversation_summaries FOR SELECT
      USING (
        EXISTS (
          SELECT 1 FROM conversations
          WHERE conversations.id = conversation_summaries.conversation_id
          AND conversations.user_id = auth.uid()
        )
      );

    CREATE POLICY "Service can manage conversation summaries"
      ON conversation_summaries FOR ALL
      USING (true)
      WITH CHECK (true);
END $$;

-- Memory Context Policies
DO $$
BEGIN
    DROP POLICY IF EXISTS "Users can view memory context from their conversations" ON memory_context;
    DROP POLICY IF EXISTS "Service can manage memory context" ON memory_context;

    CREATE POLICY "Users can view memory context from their conversations"
      ON memory_context FOR SELECT
      USING (
        EXISTS (
          SELECT 1 FROM conversations
          WHERE conversations.id = memory_context.conversation_id
          AND conversations.user_id = auth.uid()
        )
      );

    CREATE POLICY "Service can manage memory context"
      ON memory_context FOR ALL
      USING (true)
      WITH CHECK (true);
END $$;

-- ============================================================================
-- STEP 6: Create triggers for updated_at
-- ============================================================================

-- Trigger for user_memory
DROP TRIGGER IF EXISTS update_user_memory_updated_at ON user_memory;
CREATE TRIGGER update_user_memory_updated_at
  BEFORE UPDATE ON user_memory
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- Trigger for conversation_summaries
DROP TRIGGER IF EXISTS update_conversation_summaries_updated_at ON conversation_summaries;
CREATE TRIGGER update_conversation_summaries_updated_at
  BEFORE UPDATE ON conversation_summaries
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- STEP 7: Verify migration
-- ============================================================================

-- Display success message
DO $$
BEGIN
    RAISE NOTICE '✅ Memory system migration completed successfully!';
    RAISE NOTICE 'New tables created: user_memory, conversation_summaries, memory_context';
    RAISE NOTICE 'Conversations table updated with: summary, tags, message_count';
    RAISE NOTICE 'Messages table now supports: user, assistant, system roles';
END $$;

-- Show table counts
SELECT
    'user_memory' as table_name,
    COUNT(*) as row_count
FROM user_memory
UNION ALL
SELECT
    'conversation_summaries' as table_name,
    COUNT(*) as row_count
FROM conversation_summaries
UNION ALL
SELECT
    'memory_context' as table_name,
    COUNT(*) as row_count
FROM memory_context;

-- Create memory_context table if missing
-- Safe to run multiple times

CREATE TABLE IF NOT EXISTS memory_context (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE NOT NULL,
  memory_id UUID REFERENCES user_memory(id) ON DELETE CASCADE NOT NULL,
  relevance_score DECIMAL(3,2) DEFAULT 0.5 CHECK (relevance_score >= 0 AND relevance_score <= 1),
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE(conversation_id, memory_id)
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_memory_context_conversation_id ON memory_context(conversation_id);
CREATE INDEX IF NOT EXISTS idx_memory_context_memory_id ON memory_context(memory_id);
CREATE INDEX IF NOT EXISTS idx_memory_context_relevance ON memory_context(relevance_score DESC);

-- Enable RLS
ALTER TABLE memory_context ENABLE ROW LEVEL SECURITY;

-- Drop existing policies
DROP POLICY IF EXISTS "Users can view memory context from their conversations" ON memory_context;
DROP POLICY IF EXISTS "Service can manage memory context" ON memory_context;

-- Create policies
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

-- Show success
SELECT 'memory_context table ready!' as status;

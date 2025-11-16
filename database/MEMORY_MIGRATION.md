# Memory System Migration Guide

This guide will help you migrate your database to support the new advanced memory system that enables cross-chat context understanding.

## Overview

The memory system adds the following capabilities:
- **User Memory**: Persistent storage of user preferences, facts, goals, and interests
- **Conversation Summaries**: AI-generated summaries of past conversations
- **Memory Context**: Links between conversations and relevant memories
- **Cross-Chat Understanding**: AI can reference information from previous conversations

## Database Changes

### New Tables
1. **user_memory** - Stores persistent user information
2. **conversation_summaries** - Stores conversation summaries
3. **memory_context** - Links memories to conversations

### Updated Tables
1. **conversations** - Added `summary`, `tags`, and `message_count` fields
2. **messages** - Added `system` role type

## Migration Steps

### Step 1: Run the Migration SQL

**IMPORTANT**: Use the migration script, not the full schema!

1. Open your Supabase Dashboard
2. Navigate to the SQL Editor
3. Copy and paste the contents of `/database/migration_add_memory.sql`
4. Click "Run" to execute the migration

The migration is **idempotent** and **safe** - it:
- Checks if columns exist before adding them
- Uses `CREATE TABLE IF NOT EXISTS` for new tables
- Only drops and recreates policies (not data)
- Can be run multiple times without errors

### Step 2: Verify the Migration

Run this query to verify all tables exist:

```sql
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
AND table_name IN (
  'user_memory',
  'conversation_summaries',
  'memory_context',
  'conversations',
  'messages'
);
```

You should see all 5 tables listed.

### Step 3: Check Indexes

Verify indexes were created:

```sql
SELECT indexname, tablename
FROM pg_indexes
WHERE schemaname = 'public'
AND tablename IN (
  'user_memory',
  'conversation_summaries',
  'memory_context'
);
```

### Step 4: Verify RLS Policies

Check that Row Level Security policies are enabled:

```sql
SELECT schemaname, tablename, policyname
FROM pg_policies
WHERE schemaname = 'public'
AND tablename IN (
  'user_memory',
  'conversation_summaries',
  'memory_context'
);
```

## API Endpoints

### Memory Management

- `GET /api/memory` - Get all user memories
- `POST /api/memory` - Create a new memory
- `GET /api/memory/relevant` - Get relevant memories for context
- `GET /api/memory/{memory_id}` - Get specific memory
- `PUT /api/memory/{memory_id}` - Update a memory
- `DELETE /api/memory/{memory_id}` - Delete a memory

### Conversation Summaries

- `POST /api/summaries` - Create a conversation summary
- `GET /api/summaries/recent` - Get recent summaries
- `GET /api/summaries/{conversation_id}` - Get summary for a conversation
- `PUT /api/summaries/{conversation_id}` - Update a summary

## Usage Examples

### Creating a User Memory

```json
POST /api/memory
{
  "memory_type": "preference",
  "key": "language_preference",
  "value": "Prefers Python over JavaScript",
  "confidence": 1.0
}
```

### Creating a Conversation Summary

```json
POST /api/summaries
{
  "conversation_id": "uuid-here",
  "short_summary": "Discussion about building a REST API",
  "key_topics": ["REST API", "FastAPI", "Python"],
  "importance_score": 0.8
}
```

## How Memory Works in Chat

When a user sends a message:

1. The system retrieves relevant memories (preferences, facts, goals, interests)
2. It fetches recent conversation summaries
3. This context is injected into the system prompt
4. The AI uses this context to provide personalized responses

### Example System Prompt with Memory

```
You are a helpful AI assistant...

[CONTEXT FROM PREVIOUS INTERACTIONS]
User Preferences:
- Prefers Python over JavaScript
- Likes detailed explanations

About the User:
- Working as a full-stack developer
- Learning machine learning

Recent Conversations:
- Discussion about building a REST API
- Questions about database optimization
[END CONTEXT]

Please use this context to provide more personalized responses.
```

## Testing the Migration

### Test 1: Create a Memory

```bash
curl -X POST http://localhost:8000/api/memory \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "memory_type": "fact",
    "key": "test_fact",
    "value": "This is a test memory",
    "confidence": 1.0
  }'
```

### Test 2: Retrieve Memories

```bash
curl http://localhost:8000/api/memory \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Test 3: Start a New Chat

Send a message in a new conversation and verify that the AI references information from previous chats.

## Rollback (If Needed)

If you need to rollback the migration:

```sql
-- WARNING: This will delete all memory data!

DROP TABLE IF EXISTS memory_context CASCADE;
DROP TABLE IF EXISTS conversation_summaries CASCADE;
DROP TABLE IF EXISTS user_memory CASCADE;

-- Revert conversations table changes
ALTER TABLE conversations
DROP COLUMN IF EXISTS summary,
DROP COLUMN IF EXISTS tags,
DROP COLUMN IF EXISTS message_count;

-- Revert messages role check
ALTER TABLE messages
DROP CONSTRAINT IF EXISTS messages_role_check;

ALTER TABLE messages
ADD CONSTRAINT messages_role_check
CHECK (role IN ('user', 'assistant'));
```

## Performance Considerations

1. **Indexes**: All critical columns are indexed for fast queries
2. **GIN Indexes**: Used for array and JSONB columns (tags, key_topics)
3. **Pagination**: Memory and summary APIs support limit/offset
4. **Caching**: Consider implementing Redis caching for frequently accessed memories

## Next Steps

1. **AI-Powered Memory Extraction**: Implement LLM-based memory extraction from conversations
2. **AI-Powered Summarization**: Use AI to generate better conversation summaries
3. **Semantic Search**: Implement vector embeddings for semantic memory retrieval
4. **Memory Decay**: Implement confidence decay for old memories
5. **Memory Clustering**: Group related memories together

## Support

If you encounter issues during migration:
1. Check Supabase logs for errors
2. Verify RLS policies are correctly configured
3. Ensure the backend service has the correct Supabase keys
4. Test API endpoints with the provided examples

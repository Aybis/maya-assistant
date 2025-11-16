# Testing the Memory System

This guide shows you how to populate and test the memory system.

## Prerequisites

1. ✅ Migration completed (`migration_add_memory.sql` ran successfully)
2. ✅ Backend restarted
3. ✅ You have at least one conversation with messages
4. ✅ You have a valid auth token

## Quick Test Flow

### Step 1: Check Current Memory Stats

```bash
curl http://localhost:8000/api/memory-utils/stats \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Expected Output:**
```json
{
  "memories": {
    "total": 0,
    "by_type": {
      "preference": 0,
      "fact": 0,
      "goal": 0,
      "context": 0,
      "interest": 0
    }
  },
  "summaries": {
    "total": 0
  },
  "conversations": {
    "total": X  // your actual conversation count
  }
}
```

### Step 2: Process All Your Existing Conversations

This will automatically extract memories and create summaries:

```bash
curl -X POST "http://localhost:8000/api/memory-utils/process-all-conversations?limit=10" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Expected Output:**
```json
{
  "conversations": 5,
  "memories_extracted": 12,
  "summaries_created": 5,
  "errors": []
}
```

### Step 3: Verify Memory Tables Are Populated

```bash
curl http://localhost:8000/api/memory-utils/stats \
  -H "Authorization: Bearer YOUR_TOKEN"
```

**Now you should see:**
```json
{
  "memories": {
    "total": 12,
    "by_type": {
      "preference": 3,
      "fact": 5,
      "goal": 2,
      "context": 0,
      "interest": 2
    }
  },
  "summaries": {
    "total": 5
  }
}
```

### Step 4: View Your Memories

```bash
curl http://localhost:8000/api/memory \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### Step 5: View Recent Summaries

```bash
curl http://localhost:8000/api/summaries/recent \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Manual Testing: Create Specific Memories

### Create a Preference

```bash
curl -X POST http://localhost:8000/api/memory \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "memory_type": "preference",
    "key": "coding_style",
    "value": "Prefers detailed code comments and functional programming",
    "confidence": 1.0
  }'
```

### Create a Fact

```bash
curl -X POST http://localhost:8000/api/memory \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "memory_type": "fact",
    "key": "user_role",
    "value": "Full-stack developer working on React and Python projects",
    "confidence": 1.0
  }'
```

### Create a Goal

```bash
curl -X POST http://localhost:8000/api/memory \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "memory_type": "goal",
    "key": "learning_goal",
    "value": "Learning machine learning and AI integration",
    "confidence": 0.9
  }'
```

### Create an Interest

```bash
curl -X POST http://localhost:8000/api/memory \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "memory_type": "interest",
    "key": "tech_interest",
    "value": "Interested in database optimization and performance tuning",
    "confidence": 0.8
  }'
```

## Test Cross-Chat Memory

### Step 1: Create some memories (see above)

### Step 2: Start a NEW conversation

```bash
curl -X POST http://localhost:8000/api/conversations \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Test Memory Context",
    "model": "gpt-4"
  }'
```

Save the returned `conversation_id`.

### Step 3: Send a message in the new conversation

```bash
curl -X POST http://localhost:8000/api/conversations/CONVERSATION_ID/messages \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "What do you know about me?"
  }'
```

### Step 4: Check the AI Response

The AI should respond with information from your stored memories! For example:

> "Based on our previous conversations, I know that you're a full-stack developer working on React and Python projects. You prefer detailed code comments and functional programming. You're currently learning machine learning and AI integration, and you're interested in database optimization and performance tuning."

## How Memory Context Works

When you send a message, the system:

1. **Fetches your memories** (up to 10 most relevant)
2. **Fetches recent conversation summaries** (up to 5)
3. **Builds context string**:
   ```
   [CONTEXT FROM PREVIOUS INTERACTIONS]
   User Preferences:
   - Prefers detailed code comments and functional programming

   About the User:
   - Full-stack developer working on React and Python projects

   User Goals:
   - Learning machine learning and AI integration

   User Interests:
   - Interested in database optimization
   [END CONTEXT]
   ```
4. **Injects into system prompt** before sending to AI
5. **AI uses this context** to personalize responses

## Process Individual Conversations

If you want to process a specific conversation:

```bash
# Extract memories from specific conversation
curl -X POST http://localhost:8000/api/memory-utils/extract-from-conversation/CONVERSATION_ID \
  -H "Authorization: Bearer YOUR_TOKEN"

# Create summary for specific conversation
curl -X POST http://localhost:8000/api/memory-utils/summarize-conversation/CONVERSATION_ID \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Verify in Supabase Dashboard

1. Go to Supabase Dashboard
2. Navigate to Table Editor
3. Check these tables:
   - `user_memory` - Should have your memories
   - `conversation_summaries` - Should have summaries
   - `memory_context` - May be empty (populated when memories are linked to conversations)

## Common Issues

### "No memories extracted"
- The keyword-based extraction looks for specific words like "prefer", "like", "I am", etc.
- If your conversations don't contain these phrases, no memories will be extracted
- Solution: Manually create memories using the API

### "Summaries are too generic"
- The current summarization is very basic (counts messages + extracts first message)
- This is intentional for testing
- In production, you'd use an AI model to generate better summaries

### "AI doesn't use memories in responses"
- Check that memories exist: `GET /api/memory`
- Verify the chat endpoint is using MemoryService (check backend logs)
- Try asking explicit questions like "What do you remember about me?"

## What's Next?

Once you confirm memories are working:

1. **Frontend Integration**: Build UI to view/manage memories
2. **AI-Powered Extraction**: Use LLM to extract memories instead of keywords
3. **AI-Powered Summarization**: Use LLM to generate better summaries
4. **Automatic Processing**: Auto-extract memories after each conversation
5. **Semantic Search**: Add vector embeddings for better memory retrieval

## Debug Mode

To see what context is being sent to the AI, check your backend logs when sending a message. You should see:
```
Sending X messages to AI (including system message)
Conversation ID: xxx-xxx-xxx
```

The system message will include the memory context if memories exist.

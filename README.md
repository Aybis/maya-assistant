# Maya Assistant - Multi-AI Chat Application

A full-stack AI chat application that allows users to interact with multiple AI models (OpenAI GPT, Anthropic Claude, Google Gemini) in a single, unified platform.

![Maya Assistant](https://img.shields.io/badge/version-1.0.0-blue)
![Next.js](https://img.shields.io/badge/Next.js-14-black)
![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)
![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-orange)

## Features

- **Multi-AI Support**: Chat with GPT, Claude, and Gemini models in one place
- **Real-time Streaming**: Server-Sent Events (SSE) for streaming AI responses
- **Conversation Management**: Create, update, and delete conversation threads
- **Model Switching**: Change AI models on the fly within conversations
- **Authentication**: Secure OAuth2.0 authentication via Supabase (Google provider)
- **Modern UI**: Beautiful, responsive interface with Tailwind CSS
- **Atomic Design**: Well-organized component architecture
- **Type Safety**: Full TypeScript support across the stack

## Tech Stack

### Backend
- **Framework**: FastAPI 0.104.1
- **Database**: Supabase (PostgreSQL)
- **Authentication**: OAuth2.0 via Supabase
- **AI SDKs**:
  - OpenAI Python SDK
  - Anthropic Python SDK
  - Google Generative AI Python SDK
- **Validation**: Pydantic
- **Server**: Uvicorn

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Zustand + Context API
- **Authentication**: @supabase/auth-helpers-nextjs
- **Markdown**: react-markdown
- **Syntax Highlighting**: react-syntax-highlighter
- **UI Components**: Radix UI, lucide-react

## Project Structure

```
maya-assistant/
├── backend/
│   ├── app/
│   │   ├── api/              # API endpoints
│   │   │   ├── conversations.py
│   │   │   ├── messages.py
│   │   │   └── models.py
│   │   ├── models/           # Pydantic models
│   │   │   ├── conversation.py
│   │   │   └── message.py
│   │   ├── services/         # Business logic
│   │   │   ├── supabase_service.py
│   │   │   ├── ai_service.py
│   │   │   ├── openai_service.py
│   │   │   ├── claude_service.py
│   │   │   └── gemini_service.py
│   │   ├── utils/            # Utilities
│   │   │   └── streaming.py
│   │   ├── config.py
│   │   ├── dependencies.py
│   │   └── main.py
│   ├── requirements.txt
│   └── .env.example
│
├── frontend/
│   ├── src/
│   │   ├── app/              # Next.js app router
│   │   │   ├── auth/
│   │   │   ├── chat/
│   │   │   ├── login/
│   │   │   └── layout.tsx
│   │   ├── components/       # Atomic design
│   │   │   ├── atoms/
│   │   │   ├── molecules/
│   │   │   ├── organisms/
│   │   │   └── templates/
│   │   ├── lib/              # Utilities
│   │   │   ├── api.ts
│   │   │   ├── supabase.ts
│   │   │   └── utils.ts
│   │   ├── store/            # Zustand stores
│   │   │   ├── authStore.ts
│   │   │   ├── conversationStore.ts
│   │   │   └── chatStore.ts
│   │   ├── types/            # TypeScript types
│   │   └── styles/           # Global styles
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   └── .env.local.example
│
├── database/
│   └── schema.sql            # Database schema
│
└── README.md
```

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 18+
- Supabase account
- API keys for at least one AI provider:
  - OpenAI API key
  - Anthropic API key
  - Google AI API key

### 1. Database Setup

1. Create a new Supabase project at [supabase.com](https://supabase.com)

2. Run the database schema in your Supabase SQL Editor:
   ```bash
   # Copy the contents of database/schema.sql
   # Paste and run in Supabase SQL Editor
   ```

3. Enable Google OAuth provider:
   - Go to Authentication > Providers
   - Enable Google provider
   - Configure OAuth credentials

### 2. Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create `.env` file from example:
   ```bash
   cp .env.example .env
   ```

5. Configure environment variables in `.env`:
   ```env
   # Supabase
   SUPABASE_URL=your_supabase_project_url
   SUPABASE_KEY=your_supabase_anon_key
   SUPABASE_JWT_SECRET=your_supabase_jwt_secret

   # AI API Keys (at least one required)
   OPENAI_API_KEY=your_openai_api_key
   ANTHROPIC_API_KEY=your_anthropic_api_key
   GOOGLE_API_KEY=your_google_api_key

   # Server
   CORS_ORIGINS=http://localhost:3000
   ```

6. Run the backend server:
   ```bash
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

   The API will be available at `http://localhost:8000`

### 3. Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Create `.env.local` file:
   ```bash
   cp .env.local.example .env.local
   ```

4. Configure environment variables in `.env.local`:
   ```env
   NEXT_PUBLIC_SUPABASE_URL=your_supabase_project_url
   NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

5. Run the development server:
   ```bash
   npm run dev
   ```

   The app will be available at `http://localhost:3000`

## Usage

1. **Sign In**: Navigate to `http://localhost:3000` and sign in with Google

2. **Create Conversation**: Click "New Chat" to start a conversation

3. **Select Model**: Choose an AI model from the dropdown (GPT, Claude, or Gemini)

4. **Chat**: Type your message and press Enter to send

5. **Manage Conversations**:
   - Click on a conversation to switch to it
   - Hover over a conversation and click the trash icon to delete

## API Endpoints

### Health & Models
- `GET /api/health` - Health check
- `GET /api/models` - List available AI models

### Conversations
- `GET /api/conversations` - Get all conversations
- `POST /api/conversations` - Create new conversation
- `GET /api/conversations/{id}` - Get single conversation
- `PUT /api/conversations/{id}` - Update conversation
- `DELETE /api/conversations/{id}` - Delete conversation

### Messages
- `GET /api/conversations/{id}/messages` - Get messages
- `POST /api/conversations/{id}/messages` - Send message (streaming)

## Environment Variables

### Backend (.env)

| Variable | Description | Required |
|----------|-------------|----------|
| `SUPABASE_URL` | Supabase project URL | Yes |
| `SUPABASE_KEY` | Supabase anon key | Yes |
| `SUPABASE_JWT_SECRET` | Supabase JWT secret | Yes |
| `OPENAI_API_KEY` | OpenAI API key | Optional* |
| `ANTHROPIC_API_KEY` | Anthropic API key | Optional* |
| `GOOGLE_API_KEY` | Google AI API key | Optional* |
| `CORS_ORIGINS` | Allowed CORS origins | Yes |

*At least one AI provider API key is required

### Frontend (.env.local)

| Variable | Description | Required |
|----------|-------------|----------|
| `NEXT_PUBLIC_SUPABASE_URL` | Supabase project URL | Yes |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Supabase anon key | Yes |
| `NEXT_PUBLIC_API_URL` | Backend API URL | Yes |

## Development

### Backend Development

Run with auto-reload:
```bash
cd backend
uvicorn app.main:app --reload
```

### Frontend Development

Run with hot reload:
```bash
cd frontend
npm run dev
```

## Production Build

### Backend

```bash
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd frontend
npm run build
npm start
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/)
- [Next.js](https://nextjs.org/)
- [Supabase](https://supabase.com/)
- [OpenAI](https://openai.com/)
- [Anthropic](https://anthropic.com/)
- [Google AI](https://ai.google/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Zustand](https://zustand-demo.pmnd.rs/)

## Support

For issues, questions, or contributions, please open an issue on GitHub.

---

Built with ❤️ using Next.js, FastAPI, and Supabase

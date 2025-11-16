# Maya Assistant Frontend

Next.js 14 frontend for the Maya Assistant multi-AI chat application.

## Features

- **Next.js 14**: App Router with server components
- **TypeScript**: Full type safety
- **Tailwind CSS**: Utility-first styling
- **Atomic Design**: Organized component architecture
- **Zustand**: Lightweight state management
- **Supabase Auth**: OAuth2.0 authentication
- **Real-time Streaming**: SSE for AI responses

## Installation

```bash
npm install
```

## Running

Development:
```bash
npm run dev
```

Production:
```bash
npm run build
npm start
```

## Project Structure

```
src/
├── app/              # Next.js app router pages
├── components/       # UI components (Atomic Design)
│   ├── atoms/        # Basic components
│   ├── molecules/    # Composite components
│   ├── organisms/    # Complex components
│   └── templates/    # Page templates
├── lib/              # Utilities and helpers
├── store/            # Zustand stores
├── types/            # TypeScript definitions
└── styles/           # Global styles
```

## Component Architecture

Following Atomic Design:

- **Atoms**: Button, Input, Avatar, Spinner
- **Molecules**: MessageBubble, ConversationItem, ChatInput, ModelSelector
- **Organisms**: Sidebar, ChatArea, AuthProvider
- **Templates**: ChatLayout

## State Management

Three Zustand stores:

1. **authStore**: User authentication state
2. **conversationStore**: Conversations and messages
3. **chatStore**: UI state (streaming, input, sidebar)

## Environment Variables

See `.env.local.example` for required variables.

## Styling

Uses Tailwind CSS with custom design tokens defined in `tailwind.config.js`.

Theme variables in `src/styles/globals.css`.

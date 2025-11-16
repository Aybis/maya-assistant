// Root layout

import type { Metadata } from 'next';
import '@/styles/globals.css';
import AuthProvider from '@/components/organisms/AuthProvider';

export const metadata: Metadata = {
  title: 'Maya Assistant - Multi-AI Chat',
  description: 'Chat with multiple AI models in one platform',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="font-sans antialiased">
        <AuthProvider>{children}</AuthProvider>
      </body>
    </html>
  );
}

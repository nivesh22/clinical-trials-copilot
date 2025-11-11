import '../styles/globals.css'
import type { ReactNode } from 'react'
import Link from 'next/link'
import { ThemeToggle } from '@/components/theme-toggle'

export const metadata = {
  title: process.env.NEXT_PUBLIC_APP_NAME || 'Clinical Trials Copilot',
  description: 'RAG over ClinicalTrials.gov',
}

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-white text-gray-900 dark:bg-gray-950 dark:text-gray-100">
        <header className="border-b p-4 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <div className="font-semibold">{process.env.NEXT_PUBLIC_APP_NAME || 'Clinical Trials Copilot'}</div>
            <nav className="text-sm hidden sm:flex gap-3">
              <Link href="/chat" className="hover:underline">Chat</Link>
              <Link href="/status" className="hover:underline">Status</Link>
            </nav>
          </div>
          <div className="flex items-center gap-2">
            <span className="text-xs px-2 py-1 rounded bg-green-100 text-green-700 dark:bg-green-900 dark:text-green-200">OK</span>
            <ThemeToggle />
          </div>
        </header>
        <main className="container mx-auto p-4">{children}</main>
      </body>
    </html>
  )
}

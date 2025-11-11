import '../styles/globals.css'
import type { ReactNode } from 'react'

export const metadata = {
  title: process.env.NEXT_PUBLIC_APP_NAME || 'Clinical Trials Copilot',
  description: 'RAG over ClinicalTrials.gov',
}

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen bg-white text-gray-900">
        <header className="border-b p-4 flex items-center justify-between">
          <div className="font-semibold">{process.env.NEXT_PUBLIC_APP_NAME || 'Clinical Trials Copilot'}</div>
          <div className="text-xs px-2 py-1 rounded bg-green-100 text-green-700">OK</div>
        </header>
        <main className="container mx-auto p-4">{children}</main>
      </body>
    </html>
  )
}

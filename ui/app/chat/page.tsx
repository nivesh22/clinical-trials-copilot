"use client"
import { useState } from 'react'
import { ask } from '@/lib/api'
import { Source } from '@/lib/schemas'

export default function ChatPage() {
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState('')
  const [sources, setSources] = useState<Source[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setAnswer('')
    setSources([])
    try {
      const res = await ask(question)
      setAnswer(res.answer)
      setSources(res.sources)
    } catch (err: any) {
      setError(err?.message || 'Request failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="grid gap-4 md:grid-cols-[1fr_320px]">
      <section className="space-y-3">
        <form onSubmit={onSubmit} className="flex gap-2">
          <input
            className="flex-1 border rounded px-3 py-2"
            placeholder="Ask about clinical trials..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
          />
          <button className="bg-blue-600 text-white px-4 py-2 rounded" disabled={loading}>
            {loading ? 'Asking...' : 'Send'}
          </button>
        </form>
        {error && <div className="text-red-600 text-sm">{error}</div>}
        <div className="border rounded p-3 min-h-[160px] whitespace-pre-wrap">{answer}</div>
      </section>
      <aside className="space-y-2">
        <h2 className="font-semibold">Sources</h2>
        <ul className="space-y-2">
          {sources.map((s) => (
            <li key={s.nct_id + s.tag} className="border rounded p-2">
              <div className="text-sm font-mono">
                <a
                  className="text-blue-700 underline"
                  href={`https://clinicaltrials.gov/study/${s.nct_id}`}
                  target="_blank"
                >{s.nct_id}</a> — {s.tag}
              </div>
              <div className="text-sm text-gray-700">{s.snippet}</div>
            </li>
          ))}
        </ul>
      </aside>
    </div>
  )
}


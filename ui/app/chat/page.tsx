"use client"
import { useState } from 'react'
import { ask } from '@/lib/api'
import { Source } from '@/lib/schemas'
import { ssePost } from '@/lib/stream'
import { Copy, Download } from 'lucide-react'
import { SourcesDrawer } from '@/components/sources-drawer'

export default function ChatPage() {
  const [question, setQuestion] = useState('')
  const [answer, setAnswer] = useState('')
  const [sources, setSources] = useState<Source[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [stream, setStream] = useState(true)

  async function onSubmit(e: React.FormEvent) {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setAnswer('')
    setSources([])
    try {
      if (stream) {
        for await (const evt of ssePost('/api/ask/stream', { question })) {
          if (evt.type === 'token') setAnswer((a) => a + evt.data)
          if (evt.type === 'done') {
            if (evt.data?.sources) setSources(evt.data.sources)
          }
        }
      } else {
        const res = await ask(question)
        setAnswer(res.answer)
        setSources(res.sources)
      }
    } catch (err: any) {
      setError(err?.message || 'Request failed')
    } finally {
      setLoading(false)
    }
  }

  function copyAnswer() {
    navigator.clipboard.writeText(answer)
  }
  function exportJson() {
    const blob = new Blob([JSON.stringify({ question, answer, sources }, null, 2)], { type: 'application/json' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'answer.json'
    a.click()
    URL.revokeObjectURL(url)
  }

  return (
    <div className="grid gap-4 md:grid-cols-[1fr_360px]">
      <section className="space-y-3">
        <form onSubmit={onSubmit} className="flex gap-2 items-center">
          <input
            className="flex-1 border rounded px-3 py-2"
            placeholder="Ask about clinical trials..."
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
          />
          <label className="text-sm flex items-center gap-1">
            <input type="checkbox" checked={stream} onChange={(e) => setStream(e.target.checked)} />
            Stream
          </label>
          <button className="bg-blue-600 text-white px-4 py-2 rounded" disabled={loading}>
            {loading ? 'Asking...' : 'Send'}
          </button>
        </form>
        {error && <div className="text-red-600 text-sm">{error}</div>}
        <div className="flex justify-end gap-2 text-sm">
          <button className="border rounded px-2 py-1 flex items-center gap-1" onClick={copyAnswer}><Copy size={14}/> Copy</button>
          <button className="border rounded px-2 py-1 flex items-center gap-1" onClick={exportJson}><Download size={14}/> Export JSON</button>
        </div>
        <div className="border rounded p-3 min-h-[160px] whitespace-pre-wrap" aria-live="polite">{answer}</div>
      </section>
      <aside className="space-y-2">
        <SourcesDrawer sources={sources} />
      </aside>
    </div>
  )
}

"use client"
import { useState } from 'react'
import { Source } from '@/lib/schemas'

export function SourcesDrawer({ sources }: { sources: Source[] }) {
  const [open, setOpen] = useState(true)
  return (
    <div className="border rounded">
      <button
        className="w-full text-left px-3 py-2 border-b bg-gray-50 hover:bg-gray-100"
        onClick={() => setOpen((v) => !v)}
        aria-expanded={open}
        aria-controls="sources-panel"
      >
        Sources ({sources.length})
      </button>
      {open && (
        <div id="sources-panel" className="p-2 space-y-2">
          {sources.map((s) => (
            <div key={s.nct_id + s.tag} className="border rounded p-2">
              <div className="text-sm font-mono">
                <a
                  className="text-blue-700 underline"
                  href={`https://clinicaltrials.gov/study/${s.nct_id}`}
                  target="_blank"
                >{s.nct_id}</a> — {s.tag}
              </div>
              <div className="text-sm text-gray-700">{s.snippet}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}


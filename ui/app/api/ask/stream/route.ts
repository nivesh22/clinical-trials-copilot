import { NextRequest } from 'next/server'

export async function POST(req: NextRequest) {
  const base = process.env.API_BASE || 'http://localhost:8000'
  const body = await req.text()
  const r = await fetch(base + '/ask/stream', {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body,
  })
  return new Response(r.body, {
    status: r.status,
    headers: { 'content-type': 'text/event-stream' },
  })
}


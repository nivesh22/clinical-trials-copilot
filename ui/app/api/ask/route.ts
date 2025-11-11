import { NextRequest } from 'next/server'

export async function POST(req: NextRequest) {
  const body = await req.json()
  const base = process.env.API_BASE || 'http://localhost:8000'
  const r = await fetch(base + '/ask', {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(body),
  })
  const text = await r.text()
  return new Response(text, { status: r.status, headers: { 'content-type': 'application/json' } })
}


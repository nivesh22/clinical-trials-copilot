import { Sparkline } from '@/components/sparkline'

async function getMeta() {
  const base = process.env.API_BASE || 'http://localhost:8000'
  const res = await fetch(base + '/meta', { next: { revalidate: 60 } })
  if (!res.ok) throw new Error('Failed to load meta')
  return res.json()
}

export default async function StatusPage() {
  const meta = await getMeta()
  // Sample daily counts for sparkline (replace with real data later)
  const counts = [2,4,3,6,8,5,9,12,11,10,14,13,15,18,17,19,21,18,20,22]
  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-semibold">Status</h1>
      <div className="grid sm:grid-cols-3 gap-3">
        <Card label="Embed Model" value={meta.embed_model} />
        <Card label="LLM Model" value={meta.llm_model} />
        <Card label="Index Size (bytes)" value={String(meta.index_size)} />
      </div>
      <div className="space-y-2">
        <div className="text-sm text-gray-600">Airflow DAG status: sample OK</div>
        <div className="border rounded p-3">
          <div className="text-sm text-gray-600 mb-2">Daily ingested counts</div>
          <Sparkline data={counts} />
        </div>
      </div>
    </div>
  )
}

function Card({ label, value }: { label: string; value: string }) {
  return (
    <div className="border rounded p-3">
      <div className="text-xs text-gray-600">{label}</div>
      <div className="font-medium break-all">{value}</div>
    </div>
  )
}

import Link from 'next/link'

export default function Page() {
  return (
    <div className="max-w-2xl space-y-4">
      <h1 className="text-3xl font-bold">Clinical Trials Copilot</h1>
      <p className="text-gray-700">
        Ask questions about public clinical trial data and get answers with citations.
        Runs locally with a privacy-first design.
      </p>
      <div className="flex gap-3">
        <Link href="/chat" className="bg-blue-600 text-white px-4 py-2 rounded">Try the Copilot</Link>
        <Link href="/status" className="border px-4 py-2 rounded">Status</Link>
      </div>
    </div>
  )
}


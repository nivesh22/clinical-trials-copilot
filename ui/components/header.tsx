export function Header() {
  return (
    <header className="border-b p-4 flex items-center justify-between">
      <div className="font-semibold">{process.env.NEXT_PUBLIC_APP_NAME || 'Clinical Trials Copilot'}</div>
      <div className="text-xs px-2 py-1 rounded bg-green-100 text-green-700">OK</div>
    </header>
  )
}


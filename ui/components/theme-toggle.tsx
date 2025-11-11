"use client"
import { useEffect, useState } from 'react'
import { Moon, Sun } from 'lucide-react'

export function ThemeToggle() {
  const [dark, setDark] = useState(false)
  useEffect(() => {
    const isDark = localStorage.getItem('ctc-theme') === 'dark'
    setDark(isDark)
    document.documentElement.classList.toggle('dark', isDark)
  }, [])
  function toggle() {
    const next = !dark
    setDark(next)
    document.documentElement.classList.toggle('dark', next)
    localStorage.setItem('ctc-theme', next ? 'dark' : 'light')
  }
  return (
    <button onClick={toggle} className="p-2 rounded border hover:bg-gray-50 dark:hover:bg-gray-800" aria-label="Toggle theme">
      {dark ? <Sun size={16} /> : <Moon size={16} />}
    </button>
  )
}


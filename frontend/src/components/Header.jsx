import React from 'react'

function Header() {
  const navItems = [
    { label: 'Home', href: '#' },
    { label: 'API Docs', href: '#' },
    { label: 'GitHub', href: 'https://github.com/manisai833-jpg/youtube-channel-hunter' },
  ]

  return (
    <header className="flex items-center justify-between border-b border-slate-200 py-5">
      <a href="#" className="text-lg font-semibold text-slate-900">
        YouTube Channel Hunter
      </a>

      <nav className="flex items-center gap-4 text-sm text-slate-600">
        {navItems.map((item) => (
          <a key={item.label} href={item.href} className="transition hover:text-slate-900">
            {item.label}
          </a>
        ))}
      </nav>
    </header>
  )
}

export default Header

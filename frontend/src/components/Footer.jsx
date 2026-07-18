import React from 'react'

function Footer() {
  return (
    <footer className="border-t border-slate-200 py-6 text-center text-sm text-slate-600">
      <div className="flex flex-col items-center justify-center gap-2 sm:flex-row sm:gap-4">
        <span>Version 1.2</span>
        <span>Powered by FastAPI + FastMCP</span>
        <a href="https://github.com/manisai833-jpg/youtube-channel-hunter" className="text-slate-900 hover:underline">
          GitHub
        </a>
      </div>
    </footer>
  )
}

export default Footer

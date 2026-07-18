import React from 'react'

function EmptyResults() {
  return (
    <div className="rounded-2xl border border-dashed border-slate-300 bg-slate-50 px-8 py-12 text-center">
      <p className="text-lg font-medium text-slate-800">No search yet.</p>
      <p className="mt-2 text-sm text-slate-600">Start by searching for a YouTube channel.</p>
    </div>
  )
}

export default EmptyResults

function EmptyState({ title, description }) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/70 p-6 text-left shadow-sm">
      <h2 className="text-lg font-semibold text-slate-100">{title}</h2>
      <p className="mt-2 text-sm text-slate-400">{description}</p>
    </div>
  )
}

export default EmptyState

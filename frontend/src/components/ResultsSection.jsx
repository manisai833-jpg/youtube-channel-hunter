function ResultsSection({ isLoading, error, channels, query }) {
  if (isLoading) {
    return (
      <div className="rounded-2xl border border-slate-200 bg-white px-6 py-10 text-center text-sm text-slate-600">
        Searching for “{query}”...
      </div>
    )
  }

  if (error) {
    return (
      <div className="rounded-2xl border border-red-200 bg-red-50 px-6 py-8 text-left">
        <p className="text-sm font-medium text-red-700">{error}</p>
      </div>
    )
  }

  if (!channels || channels.length === 0) {
    return null
  }

  return (
    <div className="space-y-4 text-left">
      {channels.map((channel) => (
        <article key={channel.channel_id} className="flex flex-col gap-4 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm sm:flex-row">
          {channel.thumbnail ? (
            <img
              src={channel.thumbnail}
              alt={channel.channel_name}
              className="h-24 w-24 rounded-full object-cover"
            />
          ) : (
            <div className="flex h-24 w-24 items-center justify-center rounded-full bg-slate-100 text-sm text-slate-500">
              No image
            </div>
          )}

          <div className="flex-1">
            <div className="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
              <div>
                <h3 className="text-lg font-semibold text-slate-900">{channel.channel_name}</h3>
                <p className="text-sm text-slate-600">
                  {channel.subscribers?.toLocaleString()} subscribers
                </p>
              </div>
              <a
                href={channel.channel_url}
                target="_blank"
                rel="noreferrer"
                className="rounded-full border border-slate-300 px-3 py-2 text-sm font-medium text-slate-700"
              >
                Open Channel
              </a>
            </div>

            <p className="mt-3 text-sm text-slate-600">
              {channel.description || 'No description available.'}
            </p>
          </div>
        </article>
      ))}
    </div>
  )
}

export default ResultsSection

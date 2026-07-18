function PopularSearches() {
  const items = ['Gaming', 'Cooking', 'Tech', 'Education', 'Finance', 'Anime']

  return (
    <div className="flex flex-wrap justify-center gap-2">
      {items.map((item) => (
        <button
          key={item}
          type="button"
          className="rounded-full border border-slate-300 bg-white px-4 py-2 text-sm text-slate-700"
        >
          {item}
        </button>
      ))}
    </div>
  )
}

export default PopularSearches

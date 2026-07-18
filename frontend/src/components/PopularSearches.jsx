import React from 'react'

function PopularSearches({ categories, selectedCategory, onSelect, isLoading }) {
  return (
    <div className="flex flex-wrap justify-center gap-2">
      {categories.map((item) => {
        const isActive = selectedCategory === item

        return (
          <button
            key={item}
            type="button"
            onClick={() => onSelect(item)}
            disabled={isLoading}
            className={`rounded-full border px-4 py-2 text-sm transition-colors disabled:cursor-not-allowed disabled:opacity-70 ${
              isActive
                ? 'border-slate-900 bg-slate-900 text-white shadow-sm'
                : 'border-slate-300 bg-white text-slate-700 hover:border-slate-400 hover:bg-slate-50'
            }`}
          >
            {item}
          </button>
        )
      })}
    </div>
  )
}

export default PopularSearches

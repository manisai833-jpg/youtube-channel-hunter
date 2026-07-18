import React from 'react'
import { Search } from 'lucide-react'

function SearchBar({ value, onChange, onSearch, isLoading, resultsCount, onResultsCountChange }) {
  const handleKeyDown = (event) => {
    if (event.key === 'Enter') {
      event.preventDefault()
      onSearch()
    }
  }

  return (
    <div className="mx-auto flex w-full max-w-2xl items-center rounded-full border border-slate-300 bg-white px-4 py-3 shadow-sm">
      <Search className="mr-3 h-5 w-5 text-slate-400" />
      <input
        type="text"
        value={value}
        onChange={(event) => onChange(event.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Search YouTube channels..."
        className="w-full border-0 bg-transparent text-base text-slate-800 outline-none placeholder:text-slate-400"
      />
      <div className="ml-3 flex items-center gap-2">
        <label className="sr-only" htmlFor="results-count">
          Results
        </label>
        <select
          id="results-count"
          value={resultsCount}
          onChange={(event) => onResultsCountChange(Number(event.target.value))}
          className="rounded-full border border-slate-300 bg-white px-3 py-2 text-sm text-slate-700 outline-none"
        >
          <option value="5">5</option>
          <option value="10">10</option>
          <option value="25">25</option>
          <option value="50">50</option>
        </select>
        <button
          type="button"
          onClick={onSearch}
          disabled={isLoading}
          className="rounded-full bg-slate-900 px-4 py-2 text-sm font-medium text-white disabled:cursor-not-allowed disabled:opacity-70"
        >
          {isLoading ? 'Searching...' : 'Search'}
        </button>
      </div>
    </div>
  )
}

export default SearchBar

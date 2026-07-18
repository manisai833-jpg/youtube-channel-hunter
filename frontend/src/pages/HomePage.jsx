import React, { useState } from 'react'
import Header from '../components/Header'
import SearchBar from '../components/SearchBar'
import PopularSearches from '../components/PopularSearches'
import EmptyResults from '../components/EmptyResults'
import ResultsSection from '../components/ResultsSection'
import Footer from '../components/Footer'
import { DEFAULT_SUBSCRIBER_RANGE, searchChannels } from '../services/youtubeApi'

const popularCategories = ['Gaming', 'Anime', 'Tech', 'Finance', 'Education', 'Cooking']
const subscriberRanges = [
  { label: 'Any', value: DEFAULT_SUBSCRIBER_RANGE },
  { label: '1K – 10K', value: { min_subs: 1000, max_subs: 10000 } },
  { label: '10K – 100K', value: { min_subs: 10000, max_subs: 100000 } },
  { label: '100K – 1M', value: { min_subs: 100000, max_subs: 1000000 } },
  { label: '1M – 10M', value: { min_subs: 1000000, max_subs: 10000000 } },
  { label: '10M+', value: { min_subs: 10000000, max_subs: 999999999999 } },
]

function HomePage() {
  const [query, setQuery] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')
  const [channels, setChannels] = useState([])
  const [selectedCategory, setSelectedCategory] = useState('')
  const [selectedSubscriberRange, setSelectedSubscriberRange] = useState(DEFAULT_SUBSCRIBER_RANGE)
  const [selectedCountry, setSelectedCountry] = useState('')
  const [resultsCount, setResultsCount] = useState(5)

  const handleSearch = async (searchQuery = query) => {
    const trimmedQuery = searchQuery.trim()

    setQuery(trimmedQuery)

    if (!trimmedQuery) {
      setError('Please enter a search term.')
      setChannels([])
      return
    }

    setIsLoading(true)
    setError('')
    setChannels([])

    try {
      const data = await searchChannels(trimmedQuery, selectedSubscriberRange, resultsCount, selectedCountry)

      if (data?.success === false) {
        setError(data.error || 'No results found.')
        setChannels([])
      } else {
        setChannels(data?.channels || [])
        setError('')
      }
    } catch (err) {
      setError(err.message || 'Something went wrong while searching.')
      setChannels([])
    } finally {
      setIsLoading(false)
    }
  }

  const handleCategoryClick = (category) => {
    setSelectedCategory(category)
    handleSearch(category)
  }

  const handleQueryChange = (value) => {
    setQuery(value)

    if (selectedCategory && value.trim().toLowerCase() !== selectedCategory.toLowerCase()) {
      setSelectedCategory('')
    }
  }

  const handleSubscriberRangeSelect = (range) => {
    setSelectedSubscriberRange(range)
  }

  const handleCountryChange = (value) => {
    setSelectedCountry(value)
  }

  return (
    <div className="min-h-screen bg-white text-slate-900">
      <div className="mx-auto flex min-h-screen max-w-6xl flex-col px-4 sm:px-6 lg:px-8">
        <Header />

        <main className="flex flex-1 flex-col items-center justify-center px-2 py-10 sm:py-16">
          <div className="w-full max-w-3xl text-center">
            <h1 className="text-3xl font-semibold tracking-tight text-slate-900 sm:text-4xl lg:text-5xl">
              YouTube Channel Hunter
            </h1>
            <p className="mx-auto mt-4 max-w-2xl text-base text-slate-600 sm:text-lg">
              Discover YouTube channels for research, outreach, and collaboration.
            </p>

            <div className="mt-8">
              <SearchBar
                value={query}
                onChange={handleQueryChange}
                onSearch={() => handleSearch(query)}
                isLoading={isLoading}
                resultsCount={resultsCount}
                onResultsCountChange={setResultsCount}
              />
            </div>

            <div className="mt-6">
              <p className="mb-3 text-sm font-medium text-slate-500">Popular Searches</p>
              <PopularSearches
                categories={popularCategories}
                selectedCategory={selectedCategory}
                onSelect={handleCategoryClick}
                isLoading={isLoading}
              />
            </div>

            <div className="mt-6">
              <p className="mb-3 text-sm font-medium text-slate-500">Subscriber Range</p>
              <div className="flex flex-wrap justify-center gap-2">
                {subscriberRanges.map((range) => {
                  const isActive =
                    selectedSubscriberRange.min_subs === range.value.min_subs &&
                    selectedSubscriberRange.max_subs === range.value.max_subs

                  return (
                    <button
                      key={range.label}
                      type="button"
                      onClick={() => handleSubscriberRangeSelect(range.value)}
                      disabled={isLoading}
                      className={`rounded-full border px-4 py-2 text-sm transition-colors disabled:cursor-not-allowed disabled:opacity-70 ${
                        isActive
                          ? 'border-slate-900 bg-slate-900 text-white shadow-sm'
                          : 'border-slate-300 bg-white text-slate-700 hover:border-slate-400 hover:bg-slate-50'
                      }`}
                    >
                      {range.label}
                    </button>
                  )
                })}
              </div>
            </div>

            <div className="mt-6">
              <p className="mb-3 text-sm font-medium text-slate-500">Country</p>
              <div className="flex justify-center">
                <label className="sr-only" htmlFor="country-select">
                  Country
                </label>
                <select
                  id="country-select"
                  value={selectedCountry}
                  onChange={(event) => handleCountryChange(event.target.value)}
                  disabled={isLoading}
                  className="w-full max-w-xs rounded-full border border-slate-300 bg-white px-4 py-2 text-sm text-slate-700 outline-none disabled:cursor-not-allowed disabled:opacity-70"
                >
                  <option value="">All Countries</option>
                  <option value="IN">India (IN)</option>
                  <option value="US">United States (US)</option>
                  <option value="GB">United Kingdom (GB)</option>
                  <option value="CA">Canada (CA)</option>
                  <option value="AU">Australia (AU)</option>
                  <option value="JP">Japan (JP)</option>
                  <option value="DE">Germany (DE)</option>
                  <option value="FR">France (FR)</option>
                  <option value="BR">Brazil (BR)</option>
                  <option value="KR">South Korea (KR)</option>
                  <option value="ID">Indonesia (ID)</option>
                  <option value="PH">Philippines (PH)</option>
                  <option value="MX">Mexico (MX)</option>
                  <option value="ES">Spain (ES)</option>
                  <option value="IT">Italy (IT)</option>
                  <option value="NL">Netherlands (NL)</option>
                  <option value="SG">Singapore (SG)</option>
                  <option value="MY">Malaysia (MY)</option>
                </select>
              </div>
            </div>

            <div className="mt-10">
              {isLoading || error || channels.length > 0 ? (
                <ResultsSection isLoading={isLoading} error={error} channels={channels} query={query} />
              ) : (
                <EmptyResults />
              )}
            </div>
          </div>
        </main>

        <Footer />
      </div>
    </div>
  )
}

export default HomePage

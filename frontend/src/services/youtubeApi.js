const API_BASE_URL = 'https://youtube-channel-hunter.onrender.com'

export const DEFAULT_SUBSCRIBER_RANGE = {
  min_subs: 0,
  max_subs: 999999999999,
}

export async function searchChannels(query, range = DEFAULT_SUBSCRIBER_RANGE, limit = 5) {
  const params = new URLSearchParams({
    channel: query.trim(),
    min_subs: String(range?.min_subs ?? DEFAULT_SUBSCRIBER_RANGE.min_subs),
    max_subs: String(range?.max_subs ?? DEFAULT_SUBSCRIBER_RANGE.max_subs),
    limit: String(limit),
  })

  try {
    const response = await fetch(`${API_BASE_URL}/search?${params.toString()}`)
    const data = await response.json().catch(() => null)

    if (!response.ok) {
      if (data && typeof data === 'object' && typeof data.error === 'string' && data.error.trim()) {
        throw new Error(data.error)
      }

      throw new Error('Unable to reach the search service right now.')
    }

    return data
  } catch (error) {
    if (error instanceof Error && error.message) {
      throw error
    }

    throw new Error('Failed to fetch')
  }
}

const API_BASE_URL = 'https://youtube-channel-hunter.onrender.com'

export async function searchChannels(query) {
  const params = new URLSearchParams({ channel: query.trim() })

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

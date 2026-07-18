const API_BASE_URL = 'https://youtube-channel-hunter.onrender.com'

export async function searchChannels(query) {
  const params = new URLSearchParams({ channel: query.trim() })
  const response = await fetch(`${API_BASE_URL}/search?${params.toString()}`)

  if (!response.ok) {
    throw new Error('Unable to reach the search service right now.')
  }

  return response.json()
}

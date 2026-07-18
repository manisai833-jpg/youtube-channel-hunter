import React from 'react'
import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import HomePage from './HomePage'
import { beforeEach, describe, expect, it, vi } from 'vitest'

vi.mock('../services/youtubeApi', () => ({
  DEFAULT_SUBSCRIBER_RANGE: {
    min_subs: 0,
    max_subs: 999999999999,
  },
  searchChannels: vi.fn(),
}))

import { searchChannels } from '../services/youtubeApi'

const anyRange = { min_subs: 0, max_subs: 999999999999 }

describe('HomePage search behavior', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('searches the selected category when a chip is clicked', async () => {
    searchChannels.mockResolvedValue({ success: true, channels: [] })

    render(<HomePage />)

    fireEvent.click(screen.getByRole('button', { name: 'Gaming' }))
    await waitFor(() => expect(searchChannels).toHaveBeenCalledWith('Gaming', anyRange))

    fireEvent.click(screen.getByRole('button', { name: 'Anime' }))
    await waitFor(() => expect(searchChannels).toHaveBeenLastCalledWith('Anime', anyRange))

    fireEvent.click(screen.getByRole('button', { name: 'Tech' }))
    await waitFor(() => expect(searchChannels).toHaveBeenLastCalledWith('Tech', anyRange))
  })

  it('includes the selected subscriber range in every search request', async () => {
    searchChannels.mockResolvedValue({ success: true, channels: [] })

    render(<HomePage />)

    const input = screen.getByPlaceholderText('Search YouTube channels...')
    fireEvent.change(input, { target: { value: 'Gaming' } })
    fireEvent.click(screen.getByRole('button', { name: 'Search' }))

    await waitFor(() => expect(searchChannels).toHaveBeenCalledWith('Gaming', anyRange))

    fireEvent.click(screen.getByRole('button', { name: '10K – 100K' }))
    fireEvent.click(screen.getByRole('button', { name: 'Search' }))

    await waitFor(() =>
      expect(searchChannels).toHaveBeenLastCalledWith('Gaming', {
        min_subs: 10000,
        max_subs: 100000,
      })
    )
  })
})

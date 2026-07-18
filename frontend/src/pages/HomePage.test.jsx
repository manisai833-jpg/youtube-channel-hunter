import React from 'react'
import { fireEvent, render, screen, waitFor } from '@testing-library/react'
import HomePage from './HomePage'
import { beforeEach, describe, expect, it, vi } from 'vitest'

vi.mock('../services/youtubeApi', () => ({
  searchChannels: vi.fn(),
}))

import { searchChannels } from '../services/youtubeApi'

describe('HomePage category chips', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('searches the selected category when a chip is clicked', async () => {
    searchChannels.mockResolvedValue({ success: true, channels: [] })

    render(<HomePage />)

    fireEvent.click(screen.getByRole('button', { name: 'Gaming' }))
    await waitFor(() => expect(searchChannels).toHaveBeenCalledWith('Gaming'))

    fireEvent.click(screen.getByRole('button', { name: 'Anime' }))
    await waitFor(() => expect(searchChannels).toHaveBeenCalledWith('Anime'))

    fireEvent.click(screen.getByRole('button', { name: 'Tech' }))
    await waitFor(() => expect(searchChannels).toHaveBeenCalledWith('Tech'))
  })
})

import { apiClient } from '@/lib/api'

export const useSampleHook = () => {
  const useSample = async () => {
    const response = await apiClient.post('/sample/test', {
      name: 'John',
      value: 10
    })
    
    if (response.success) {
      return response.data || response
    } else {
      throw new Error(response.error || 'Failed to fetch sample data')
    }
  }

  return {
    useSample,
  }
}


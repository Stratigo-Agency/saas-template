const API_BASE_URL = import.meta.env.VITE_BACKEND_URL || import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export interface ApiResponse<T = any> {
  success: boolean
  data?: T
  error?: string
  user?: any
  session?: any
  url?: string
}

class ApiClient {
  private baseUrl: string
  private getAuthToken: (() => string | null) | null = null

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl
  }

  setAuthTokenGetter(getter: () => string | null) {
    this.getAuthToken = getter
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    const url = `${this.baseUrl}${endpoint}`
    const token = this.getAuthToken?.()
    
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers,
    }

    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }

    try {
      const response = await fetch(url, {
        ...options,
        headers,
        credentials: 'include',
      })

      const data = await response.json()

      if (!response.ok) {
        return {
          success: false,
          error: data.detail || data.error || 'Request failed',
        }
      }

      return {
        success: true,
        ...data,
      }
    } catch (error: any) {
      console.error('API request failed:', error)
      return {
        success: false,
        error: error.message || 'Network error',
      }
    }
  }

  async get<T>(endpoint: string): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, { method: 'GET' })
  }

  async post<T>(endpoint: string, body?: any): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: body ? JSON.stringify(body) : undefined,
    })
  }

  async put<T>(endpoint: string, body?: any): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: body ? JSON.stringify(body) : undefined,
    })
  }

  async delete<T>(endpoint: string): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, { method: 'DELETE' })
  }
}

export const apiClient = new ApiClient(API_BASE_URL)



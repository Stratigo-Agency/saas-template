import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { apiClient } from '@/lib/api'

interface User {
  id: string
  email?: string
  user_metadata?: Record<string, any>
  created_at?: string
}

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const accessToken = ref<string | null>(null)
  const loading = ref(true)
  const error = ref<string | null>(null)

  // Load token from localStorage on initialization
  const loadToken = () => {
    const token = localStorage.getItem('access_token')
    if (token) {
      accessToken.value = token
      // Set token getter for API client
      apiClient.setAuthTokenGetter(() => accessToken.value)
    }
  }

  // Save token to localStorage
  const saveToken = (token: string | null) => {
    if (token) {
      localStorage.setItem('access_token', token)
      accessToken.value = token
    } else {
      localStorage.removeItem('access_token')
      accessToken.value = null
    }
    apiClient.setAuthTokenGetter(() => accessToken.value)
  }

  const isAuthenticated = computed(() => !!user.value && !!accessToken.value)

  // Initialize auth state
  const initialize = async () => {
    loading.value = true
    error.value = null

    try {
      // Load token from localStorage
      loadToken()

      // Check if user is already logged in
      if (accessToken.value) {
        const response = await apiClient.get('/auth/session')
        if (response.success && response.user) {
          user.value = response.user
        } else {
          // Token is invalid, clear it
          saveToken(null)
          user.value = null
        }
      }
    } catch (err: any) {
      console.error('Failed to initialize auth:', err)
      error.value = err.message || 'Failed to initialize authentication'
      saveToken(null)
      user.value = null
    } finally {
      loading.value = false
    }
  }

  // Sign up with email and password
  const signUp = async (email: string, password: string) => {
    loading.value = true
    error.value = null

    try {
      const response = await apiClient.post('/auth/signup', { email, password })

      if (!response.success) {
        error.value = response.error || 'Sign up failed'
        return { success: false, error: response.error }
      }

      if (response.user) {
        user.value = response.user
      }
      
      return { success: true, data: response }
    } catch (err: any) {
      console.error('Sign up failed:', err)
      error.value = err.message || 'Sign up failed'
      return { success: false, error: err.message }
    } finally {
      loading.value = false
    }
  }

  // Sign in with email and password
  const signIn = async (email: string, password: string) => {
    loading.value = true
    error.value = null

    try {
      const response = await apiClient.post('/auth/signin', { email, password })

      if (!response.success) {
        error.value = response.error || 'Sign in failed'
        return { success: false, error: response.error }
      }

      if (response.user) {
        user.value = response.user
      }

      // Save access token if provided
      if (response.session?.access_token) {
        saveToken(response.session.access_token)
      }
      
      return { success: true, data: response }
    } catch (err: any) {
      console.error('Sign in failed:', err)
      error.value = err.message || 'Sign in failed'
      return { success: false, error: err.message }
    } finally {
      loading.value = false
    }
  }

  // Sign in with OAuth provider
  const signInWithOAuth = async (provider: 'google' | 'github' | 'facebook') => {
    loading.value = true
    error.value = null

    try {
      const redirectUrl = `${window.location.origin}/auth/callback`
      const response = await apiClient.post('/auth/oauth', { 
        provider, 
        redirect_url: redirectUrl 
      })

      if (!response.success || !response.url) {
        error.value = response.error || 'OAuth sign in failed'
        return { success: false, error: response.error }
      }

      // Redirect to OAuth provider
      window.location.href = response.url
      
      return { success: true, data: response }
    } catch (err: any) {
      console.error('OAuth sign in failed:', err)
      error.value = err.message || 'OAuth sign in failed'
      return { success: false, error: err.message }
    } finally {
      loading.value = false
    }
  }

  // Sign out
  const signOut = async () => {
    loading.value = true
    error.value = null

    try {
      await apiClient.post('/auth/signout')
    } catch (err: any) {
      console.error('Sign out failed:', err)
    } finally {
      // Clear local state regardless of response
      user.value = null
      saveToken(null)
      loading.value = false
    }
    
    return { success: true }
  }

  // Get user profile
  const getUserProfile = async () => {
    if (!accessToken.value) return null

    try {
      const response = await apiClient.get('/auth/profile')
      
      if (response.success) {
        // The profile data is spread into the response object
        const { success, error, ...profile } = response
        return Object.keys(profile).length > 0 ? profile : null
      }
      
      return null
    } catch (err: any) {
      console.error('Failed to get user profile:', err)
      return null
    }
  }

  // Update user profile
  const updateUserProfile = async (profile: any) => {
    if (!accessToken.value) return { success: false, error: 'Not authenticated' }

    try {
      const response = await apiClient.put('/auth/profile', profile)

      if (!response.success) {
        return { success: false, error: response.error }
      }

      // Update the local user state
      if (response.user) {
        user.value = response.user
      }
      
      return { success: true }
    } catch (err: any) {
      console.error('Failed to update profile:', err)
      return { success: false, error: err.message }
    }
  }

  // Initialize token getter on store creation
  loadToken()

  // Initialize token getter on store creation
  loadToken()

  return {
    user,
    loading,
    error,
    isAuthenticated,
    initialize,
    signUp,
    signIn,
    signInWithOAuth,
    signOut,
    getUserProfile,
    updateUserProfile
  }
}) 
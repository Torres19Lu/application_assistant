import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login, register, getUserInfo } from '@/utils/api'

export const useUserStore = defineStore('user', () => {
  const token = ref(localStorage.getItem('token') || '')
  const userInfo = ref(null)
  
  const isAuthenticated = computed(() => !!token.value)
  const isAdmin = computed(() => userInfo.value?.role === 'admin')
  
  const setToken = (newToken) => {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }
  
  const clearToken = () => {
    token.value = ''
    userInfo.value = null
    localStorage.removeItem('token')
  }
  
  const loginUser = async (credentials) => {
    const res = await login(credentials)
    setToken(res.access_token)
    await fetchUserInfo()
    return res
  }
  
  const registerUser = async (data) => {
    return await register(data)
  }
  
  const fetchUserInfo = async () => {
    try {
      const res = await getUserInfo()
      userInfo.value = res
      return res
    } catch (error) {
      clearToken()
      throw error
    }
  }
  
  const logout = () => {
    clearToken()
  }
  
  return {
    token,
    userInfo,
    isAuthenticated,
    isAdmin,
    loginUser,
    registerUser,
    fetchUserInfo,
    logout
  }
})

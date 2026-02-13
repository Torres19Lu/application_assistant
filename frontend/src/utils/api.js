import axios from 'axios'
import { ElMessage } from 'element-plus'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

api.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    const message = error.response?.data?.detail || '请求失败，请稍后重试'
    ElMessage.error(message)
    
    if (error.response?.status === 401) {
      // 登录接口的401不跳转，避免页面刷新导致错误提示消失
      const isLoginRequest = error.config?.url?.includes('/auth/login')
      if (!isLoginRequest) {
        localStorage.removeItem('token')
        window.location.href = '/login'
      }
    }
    
    return Promise.reject(error)
  }
)

// 认证相关
export const login = (data) => {
  // FastAPI OAuth2PasswordRequestForm 需要 form-encoded 格式
  const params = new URLSearchParams()
  params.append('username', data.username)
  params.append('password', data.password)
  return api.post('/auth/login', params, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
  })
}
export const register = (data) => api.post('/auth/register', data)
export const getUserInfo = () => api.get('/auth/me')

// 用户资料
export const updateUserProfile = (data) => api.put('/auth/profile', data)
export const changeUserPassword = (data) => api.put('/auth/password', data)
export const uploadAvatar = (file) => {
  const formData = new FormData()
  formData.append('file', file)
  return api.post('/auth/avatar', formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  })
}

// 管理员 - 用户管理
export const getUsers = (params) => api.get('/auth/users', { params })
export const getUsersCount = (params) => api.get('/auth/users/count', { params })
export const createUser = (data) => api.post('/auth/users', data)
export const updateUser = (id, data) => api.put(`/auth/users/${id}`, data)
export const toggleUserStatus = (id) => api.put(`/auth/users/${id}/toggle`)
export const resetUserPassword = (id, data) => api.put(`/auth/users/${id}/reset-password`, data)
export const deleteUser = (id) => api.delete(`/auth/users/${id}`)

// 院校相关
export const getUniversities = (params) => api.get('/universities', { params })
export const getUniversitiesCount = (params) => api.get('/universities/count', { params })
export const getUniversity = (id) => api.get(`/universities/${id}`)
export const createUniversity = (data) => api.post('/universities', data)
export const updateUniversity = (id, data) => api.put(`/universities/${id}`, data)
export const deleteUniversity = (id) => api.delete(`/universities/${id}`)

// 专业相关
export const getMajors = (params) => api.get('/majors', { params })
export const getMajorsCount = (params) => api.get('/majors/count', { params })
export const getMajor = (id) => api.get(`/majors/${id}`)
export const createMajor = (data) => api.post('/majors', data)
export const updateMajor = (id, data) => api.put(`/majors/${id}`, data)
export const deleteMajor = (id) => api.delete(`/majors/${id}`)

// 收藏相关
export const getCollections = () => api.get('/collections')
export const addCollection = (data) => api.post('/collections', data)
export const removeCollection = (id) => api.delete(`/collections/${id}`)
export const checkCollection = (type, targetId) => api.get(`/collections/check`, { params: { type, id: targetId } })

// 攻略相关
export const getGuides = (params) => api.get('/guides', { params })
export const getGuidesCount = (params) => api.get('/guides/count', { params })
export const getGuide = (id) => api.get(`/guides/${id}`)
export const createGuide = (data) => api.post('/guides', data)
export const updateGuide = (id, data) => api.put(`/guides/${id}`, data)
export const deleteGuide = (id) => api.delete(`/guides/${id}`)
export const likeGuide = (id) => api.post(`/guides/${id}/like`)

// 统计数据
export const getStatistics = () => api.get('/statistics')

// 录取案例相关
export const getCases = (params) => api.get('/cases', { params })
export const getCasesCount = (params) => api.get('/cases/count', { params })
export const getCase = (id) => api.get(`/cases/${id}`)
export const createCase = (data) => api.post('/cases', data)
export const updateCase = (id, data) => api.put(`/cases/${id}`, data)
export const deleteCase = (id) => api.delete(`/cases/${id}`)

// 模糊搜索 (自动完成)
export const searchUniversities = (q, limit = 10) => api.get('/cases/search/universities', { params: { q, limit } })
export const searchMajors = (q, universityId, limit = 20) => api.get('/cases/search/majors', { params: { q, university_id: universityId, limit } })

// AI 智能推荐
export const getRecommendations = (data) => api.post('/cases/recommend', data)

export default api

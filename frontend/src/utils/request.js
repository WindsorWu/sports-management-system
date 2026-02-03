import axios from 'axios'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getToken, removeToken } from './auth'
import router from '@/router'

// 创建axios实例
const service = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json;charset=UTF-8'
  }
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    // 在发送请求之前添加token
    const token = getToken()
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    if (config.data instanceof FormData) {
      delete config.headers['Content-Type']
    }
    return config
  },
  error => {
    console.error('Request error:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  response => {
    const res = response.data

    // 如果返回的状态码不是2xx，则认为是错误
    if (response.status < 200 || response.status >= 300) {
      ElMessage({
        message: res.detail || res.message || 'Error',
        type: 'error',
        duration: 5 * 1000
      })
      return Promise.reject(new Error(res.detail || res.message || 'Error'))
    }

    return res
  },
  error => {
    console.error('Response error:', error)

    if (error.response) {
      const { status, data } = error.response

      switch (status) {
        case 401:
          // Token过期或无效
          ElMessageBox.confirm(
            '登录状态已过期，请重新登录',
            '系统提示',
            {
              confirmButtonText: '重新登录',
              cancelButtonText: '取消',
              type: 'warning'
            }
          ).then(() => {
            removeToken()
            localStorage.clear()
            router.push('/login')
          }).catch(() => {})
          break
        case 403:
          ElMessage({
            message: '没有访问权限',
            type: 'error',
            duration: 3 * 1000
          })
          break
        case 404:
          ElMessage({
            message: '请求的资源不存在',
            type: 'error',
            duration: 3 * 1000
          })
          break
        case 500:
          ElMessage({
            message: data.detail || '服务器内部错误',
            type: 'error',
            duration: 5 * 1000
          })
          break
        default:
          ElMessage({
            message: data.detail || data.message || '请求失败',
            type: 'error',
            duration: 3 * 1000
          })
      }
    } else if (error.request) {
      ElMessage({
        message: '网络连接失败，请检查您的网络',
        type: 'error',
        duration: 3 * 1000
      })
    } else {
      ElMessage({
        message: error.message || '请求失败',
        type: 'error',
        duration: 3 * 1000
      })
    }

    return Promise.reject(error)
  }
)

export default service

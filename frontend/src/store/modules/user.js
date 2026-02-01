import { getUserInfo as getUserInfoApi, login as loginApi, register as registerApi } from '@/api/user'
import { setToken, removeToken } from '@/utils/auth'

export default {
  namespaced: true,
  state: {
    token: localStorage.getItem('token') || '',
    userInfo: JSON.parse(localStorage.getItem('userInfo') || '{}')
  },
  mutations: {
    SET_TOKEN(state, token) {
      state.token = token
      localStorage.setItem('token', token)
    },
    SET_USER_INFO(state, userInfo) {
      state.userInfo = userInfo
      localStorage.setItem('userInfo', JSON.stringify(userInfo))
    },
    CLEAR_USER(state) {
      state.token = ''
      state.userInfo = {}
      localStorage.removeItem('token')
      localStorage.removeItem('userInfo')
    }
  },
  actions: {
    // 登录
    async login({ commit }, loginForm) {
      try {
        const data = await loginApi(loginForm)
        // 后端返回的是access和refresh，不是access_token
        commit('SET_TOKEN', data.access)
        setToken(data.access)
        return data
      } catch (error) {
        throw error
      }
    },
    // 注册
    async register({ commit }, registerForm) {
      try {
        const data = await registerApi(registerForm)
        return data
      } catch (error) {
        throw error
      }
    },
    // 获取用户信息
    async getUserInfo({ commit }) {
      try {
        const data = await getUserInfoApi()
        commit('SET_USER_INFO', data)
        return data
      } catch (error) {
        throw error
      }
    },
    // 退出登录
    logout({ commit }) {
      commit('CLEAR_USER')
      removeToken()
    }
  },
  getters: {
    token: state => state.token,
    userInfo: state => state.userInfo,
    isLogin: state => !!state.token,
    isAdmin: state => state.userInfo?.user_type === 'admin',
    isStaff: state => !!state.userInfo?.is_staff
  }
}

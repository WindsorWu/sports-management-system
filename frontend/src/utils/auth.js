import Cookies from 'js-cookie'

const TokenKey = 'token'  // 与Vuex store保持一致

export function getToken() {
  return localStorage.getItem(TokenKey)
}

export function setToken(token) {
  localStorage.setItem(TokenKey, token)
  return Cookies.set(TokenKey, token)
}

export function removeToken() {
  localStorage.removeItem(TokenKey)
  return Cookies.remove(TokenKey)
}

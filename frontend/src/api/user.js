import request from '@/utils/request'

/**
 * 用户登录
 */
export function login(data) {
  return request({
    url: '/auth/login/',
    method: 'post',
    data: {
      username: data.username,
      password: data.password
    }
  })
}

/**
 * 用户注册
 */
export function register(data) {
  return request({
    url: '/users/register/',
    method: 'post',
    data
  })
}

/**
 * 获取当前用户信息
 */
export function getUserInfo() {
  return request({
    url: '/users/me/',
    method: 'get'
  })
}

/**
 * 更新用户信息
 */
export function updateUserInfo(data) {
  return request({
    url: '/users/me/',
    method: 'put',
    data
  })
}

/**
 * 修改密码
 */
export function changePassword(data) {
  return request({
    url: '/users/me/password/',
    method: 'put',
    data
  })
}

/**
 * 获取用户列表（管理员）
 */
export function getUserList(params) {
  return request({
    url: '/users/',
    method: 'get',
    params
  })
}

/**
 * 获取用户详情（管理员）
 */
export function getUserDetail(id) {
  return request({
    url: `/users/${id}/`,
    method: 'get'
  })
}

/**
 * 更新用户（管理员）
 */
export function updateUser(id, data) {
  return request({
    url: `/users/${id}/`,
    method: 'patch',
    data
  })
}

/**
 * 删除用户（管理员）
 */
export function deleteUser(id) {
  return request({
    url: `/users/${id}/`,
    method: 'delete'
  })
}

/**
 * 启用用户（管理员）
 */
export function activateUser(id) {
  return request({
    url: `/users/${id}/activate/`,
    method: 'put'
  })
}

/**
 * 禁用用户（管理员）
 */
export function deactivateUser(id) {
  return request({
    url: `/users/${id}/deactivate/`,
    method: 'put'
  })
}

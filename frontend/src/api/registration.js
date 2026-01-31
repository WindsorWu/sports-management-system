import request from '@/utils/request'

/**
 * 获取报名列表
 */
export function getRegistrationList(params) {
  return request({
    url: '/registrations/',
    method: 'get',
    params
  })
}

/**
 * 获取我的报名列表
 */
export function getMyRegistrations() {
  return request({
    url: '/registrations/my_registrations/',
    method: 'get'
  })
}

/**
 * 获取报名详情
 */
export function getRegistrationDetail(id) {
  return request({
    url: `/registrations/${id}/`,
    method: 'get'
  })
}

/**
 * 创建报名
 */
export function createRegistration(data) {
  return request({
    url: '/registrations/',
    method: 'post',
    data
  })
}

/**
 * 取消报名
 */
export function cancelRegistration(id) {
  return request({
    url: `/registrations/${id}/cancel/`,
    method: 'put'
  })
}

/**
 * 更新报名状态（管理员）
 */
export function updateRegistrationStatus(id, status) {
  return request({
    url: `/registrations/${id}/status/`,
    method: 'put',
    data: { status }
  })
}

/**
 * 审核报名（管理员）
 */
export function approveRegistration(id, review_remarks) {
  return request({
    url: `/registrations/${id}/approve/`,
    method: 'put',
    data: { review_remarks }
  })
}

/**
 * 拒绝报名（管理员）
 */
export function rejectRegistration(id, review_remarks) {
  return request({
    url: `/registrations/${id}/reject/`,
    method: 'put',
    data: { review_remarks }
  })
}

/**
 * 导出报名数据（管理员）
 */
export function exportRegistrations(params) {
  return request({
    url: '/registrations/export/',
    method: 'get',
    params,
    responseType: 'blob'
  })
}

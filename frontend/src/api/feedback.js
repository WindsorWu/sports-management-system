import request from '@/utils/request'

/**
 * 获取反馈列表
 */
export function getFeedbackList(params) {
  return request({
    url: '/feedback/',
    method: 'get',
    params
  })
}

/**
 * 获取我的反馈
 */
export function getMyFeedback() {
  return request({
    url: '/feedback/me/',
    method: 'get'
  })
}

/**
 * 获取反馈详情
 */
export function getFeedbackDetail(id) {
  return request({
    url: `/feedback/${id}/`,
    method: 'get'
  })
}

/**
 * 创建反馈
 */
export function createFeedback(data) {
  return request({
    url: '/feedback/',
    method: 'post',
    data
  })
}

/**
 * 更新反馈状态（管理员）
 */
export function updateFeedbackStatus(id, status) {
  return request({
    url: `/feedback/${id}/status/`,
    method: 'put',
    data: { status }
  })
}

/**
 * 删除反馈（管理员）
 */
export function deleteFeedback(id) {
  return request({
    url: `/feedback/${id}/`,
    method: 'delete'
  })
}

/**
 * 回复反馈（管理员）
 */
export function replyFeedback(id, reply) {
  return request({
    url: `/feedback/${id}/reply/`,
    method: 'post',
    data: { reply }
  })
}

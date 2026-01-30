import request from '@/utils/request'

/**
 * 获取赛事列表
 */
export function getEventList(params) {
  return request({
    url: '/events/',
    method: 'get',
    params
  })
}

/**
 * 获取赛事详情
 */
export function getEventDetail(id) {
  return request({
    url: `/events/${id}/`,
    method: 'get'
  })
}

/**
 * 创建赛事（管理员）
 */
export function createEvent(data) {
  return request({
    url: '/events/',
    method: 'post',
    data
  })
}

/**
 * 更新赛事（管理员）
 */
export function updateEvent(id, data) {
  return request({
    url: `/events/${id}/`,
    method: 'put',
    data
  })
}

/**
 * 删除赛事（管理员）
 */
export function deleteEvent(id) {
  return request({
    url: `/events/${id}/`,
    method: 'delete'
  })
}

/**
 * 发布赛事（管理员）
 */
export function publishEvent(id) {
  return request({
    url: `/events/${id}/publish/`,
    method: 'post'
  })
}

/**
 * 取消发布赛事（管理员）
 */
export function unpublishEvent(id) {
  return request({
    url: `/events/${id}/unpublish/`,
    method: 'post'
  })
}

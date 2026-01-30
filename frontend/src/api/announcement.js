import request from '@/utils/request'

/**
 * 获取公告列表
 */
export function getAnnouncementList(params) {
  return request({
    url: '/announcements/',
    method: 'get',
    params
  })
}

/**
 * 获取公告详情
 */
export function getAnnouncementDetail(id) {
  return request({
    url: `/announcements/${id}/`,
    method: 'get'
  })
}

/**
 * 创建公告（管理员）
 */
export function createAnnouncement(data) {
  return request({
    url: '/announcements/',
    method: 'post',
    data
  })
}

/**
 * 更新公告（管理员）
 */
export function updateAnnouncement(id, data) {
  return request({
    url: `/announcements/${id}/`,
    method: 'put',
    data
  })
}

/**
 * 删除公告（管理员）
 */
export function deleteAnnouncement(id) {
  return request({
    url: `/announcements/${id}/`,
    method: 'delete'
  })
}

/**
 * 发布公告（管理员）
 */
export function publishAnnouncement(id) {
  return request({
    url: `/announcements/${id}/publish/`,
    method: 'post'
  })
}

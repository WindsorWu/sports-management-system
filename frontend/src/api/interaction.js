import request from '@/utils/request'

/**
 * 点赞
 */
export function like(targetType, targetId) {
  return request({
    url: `/interactions/likes/`,
    method: 'post',
    data: {
      target_type: targetType,
      target_id: targetId
    }
  })
}

/**
 * 取消点赞
 */
export function unlike(targetType, targetId) {
  return request({
    url: `/interactions/likes/unlike/`,
    method: 'post',
    data: {
      target_type: targetType,
      target_id: targetId
    }
  })
}

/**
 * 收藏
 */
export function favorite(targetType, targetId) {
  return request({
    url: `/interactions/favorites/`,
    method: 'post',
    data: {
      target_type: targetType,
      target_id: targetId
    }
  })
}

/**
 * 取消收藏
 */
export function unfavorite(targetType, targetId) {
  return request({
    url: `/interactions/favorites/unfavorite/`,
    method: 'post',
    data: {
      target_type: targetType,
      target_id: targetId
    }
  })
}

/**
 * 获取评论列表
 */
export function getCommentList(params) {
  return request({
    url: '/interactions/comments/',
    method: 'get',
    params
  })
}

/**
 * 创建评论
 */
export function createComment(data) {
  return request({
    url: '/interactions/comments/',
    method: 'post',
    data
  })
}

/**
 * 删除评论
 */
export function deleteComment(id) {
  return request({
    url: `/interactions/comments/${id}/`,
    method: 'delete'
  })
}

/**
 * 审核通过评论
 */
export function approveComment(id) {
  return request({
    url: `/interactions/comments/${id}/approve/`,
    method: 'put'
  })
}

/**
 * 审核拒绝评论
 */
export function rejectComment(id) {
  return request({
    url: `/interactions/comments/${id}/reject/`,
    method: 'put'
  })
}

/**
 * 获取我的收藏列表
 */
export function getMyFavorites() {
  return request({
    url: '/interactions/favorites/',
    method: 'get'
  })
}

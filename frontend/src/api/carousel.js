import request from '@/utils/request'

/**
 * 获取轮播图列表
 */
export function getCarouselList(params) {
  return request({
    url: '/carousels/',
    method: 'get',
    params
  })
}

/**
 * 获取轮播图详情
 */
export function getCarouselDetail(id) {
  return request({
    url: `/carousels/${id}/`,
    method: 'get'
  })
}

/**
 * 创建轮播图（管理员）
 */
export function createCarousel(data) {
  return request({
    url: '/carousels/',
    method: 'post',
    data
  })
}

/**
 * 更新轮播图（管理员）
 */
export function updateCarousel(id, data) {
  return request({
    url: `/carousels/${id}/`,
    method: 'put',
    data
  })
}

/**
 * 删除轮播图（管理员）
 */
export function deleteCarousel(id) {
  return request({
    url: `/carousels/${id}/`,
    method: 'delete'
  })
}

/**
 * 更新轮播图状态（管理员）
 */
export function updateCarouselStatus(id, isActive) {
  return request({
    url: `/carousels/${id}/status/`,
    method: 'put',
    data: { is_active: isActive }
  })
}

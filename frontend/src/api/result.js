import request from '@/utils/request'

/**
 * 获取成绩列表
 */
export function getResultList(params) {
  return request({
    url: '/results/',
    method: 'get',
    params
  })
}

/**
 * 获取我的成绩
 */
export function getMyResults() {
  return request({
    url: '/results/me/',
    method: 'get'
  })
}

/**
 * 获取成绩详情
 */
export function getResultDetail(id) {
  return request({
    url: `/results/${id}/`,
    method: 'get'
  })
}

/**
 * 创建成绩（管理员）
 */
export function createResult(data) {
  return request({
    url: '/results/',
    method: 'post',
    data
  })
}

/**
 * 更新成绩（管理员）
 */
export function updateResult(id, data) {
  return request({
    url: `/results/${id}/`,
    method: 'put',
    data
  })
}

/**
 * 删除成绩（管理员）
 */
export function deleteResult(id) {
  return request({
    url: `/results/${id}/`,
    method: 'delete'
  })
}

/**
 * 批量导入成绩（管理员）
 */
export function importResults(data) {
  return request({
    url: '/results/import/',
    method: 'post',
    data
  })
}

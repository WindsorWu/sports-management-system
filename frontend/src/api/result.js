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
    url: '/results/my_results/',
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
 * 部分更新成绩（管理员）
 */
export function patchResult(id, data) {
  return request({
    url: `/results/${id}/`,
    method: 'patch',
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

/**
 * 发布成绩（管理员）
 */
export function publishResult(id) {
  return request({
    url: `/results/${id}/publish/`,
    method: 'post'
  })
}

/**
 * 导出成绩数据（管理员）
 */
export function exportResults(params) {
  return request({
    url: '/results/export/',
    method: 'get',
    params,
    responseType: 'blob'
  })
}

/**
 * 获取待录成绩数（裁判）
 */
export function getPendingResultsCount() {
  return request({
    url: '/results/pending_results_count/',
    method: 'get'
  })
}

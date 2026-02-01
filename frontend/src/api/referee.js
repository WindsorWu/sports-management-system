import request from '@/utils/request'

/**
 * 获取裁判可访问的赛事访问记录
 */
export function getRefereeAccessList(params) {
  return request({
    url: '/events/referee-access/',
    method: 'get',
    params
  })
}

/**
 * 为裁判分配可访问赛事
 */
export function assignRefereeEvents(data) {
  return request({
    url: '/events/referee-access/assign/',
    method: 'post',
    data
  })
}

/**
 * 获取当前裁判被分配的赛事
 */
export function getMyRefereeEvents() {
  return request({
    url: '/events/referee-access/my_events/',
    method: 'get'
  })
}

/**
 * 获取裁判可访问赛事的汇总
 */
export function getRefereeAccessSummary(params) {
  return request({
    url: '/events/referee-access/summary/',
    method: 'get',
    params
  })
}

import request from '@/utils/request'

export function getList(params) {
  return request({
    url: '/api/v1.0.0/table/list',
    method: 'get',
    params
  })
}

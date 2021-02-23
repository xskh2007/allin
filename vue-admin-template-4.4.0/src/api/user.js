import request from '@/utils/request'

export function login(data) {
  return request({
    url: '/api/v1.0.0/user/login',
    method: 'post',
    data
  })
}

export function getInfo(token) {
  return request({
    url: '/api/v1.0.0/user/userinfo',
    method: 'get'
  })
}

export function logout() {
  return request({
    url: '/vue-admin-template/user/logout',
    method: 'post'
  })
}
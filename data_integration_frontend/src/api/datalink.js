import request from '@/utils/request'
import Qs from 'qs'

export function fetchProjectCluster() {
  return request({
    baseURL: process.env.VUE_APP_BASE_URL,
    url: '/dataIntegration/getProjectCluster/',
    method: 'get'
  })
}

export function fetchList(query) {
  return request({
    baseURL: process.env.VUE_APP_BASE_URL,
    url: '/dataIntegration/getList/',
    method: 'get',
    params: query,
    paramsSerializer: function (params) {
      return Qs.stringify(params, { arrayFormat: 'repeat' })
    }
  })
}

export function fetchBrief(query) {
  return request({
    baseURL: process.env.VUE_APP_BASE_URL,
    url: '/dataIntegration/getBrief/',
    method: 'get',
    params: query
  })
}

export function startScheduler(query) {
  return request({
    baseURL: process.env.VUE_APP_BASE_URL,
    url: '/dataIntegration/startScheduler/',
    method: 'get',
    params: query
  })
}

export function createData(data) {
  return request({
    baseURL: process.env.VUE_APP_BASE_URL,
    url: '/dataIntegration/createData/',
    method: 'post',
    data
  })
}

export function updateData(data) {
  return request({
    baseURL: process.env.VUE_APP_BASE_URL,
    url: '/dataIntegration/updateData/',
    method: 'post',
    data
  })
}

export function deleteData(query) {
  return request({
    baseURL: process.env.VUE_APP_BASE_URL,
    url: '/dataIntegration/deleteData/',
    // url: '/dataIntegration/getList/',
    method: 'get',
    params: query
  })
}

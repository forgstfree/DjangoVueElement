import request from '@/utils/request'

export function fetchList(query) {
    return request({
        baseURL: process.env.VUE_APP_BASE_URL,
        url: '/dblog/show_data/',
        method: 'get',
        params: query
    })
}

export function analysisLog(query) {
    return request({
        baseURL: process.env.VUE_APP_BASE_URL,
        url: '/dblog/analysislog/',
        method: 'get',
        params: query
    })
}

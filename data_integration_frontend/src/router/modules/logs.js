/** When your routing table is too long, you can split it into small modules**/

import Layout from '@/layout'

const logsRouter = {
    path: '/logs',
    component: Layout,
    redirect: 'noRedirect',
    name: 'Logs',
    meta: {
        title: '日志分析',
        icon: 'chart'
    },
    children: [
        {
            path: '/databases',
            name: 'Databases',
            component: () => import('@/views/logs/databases/index'),
            meta: { title: '数据源', icon: 'databases' }
        },

        {
            path: '/upload',
            name: 'Upload',
            component: () => import('@/views/logs/upload/upload'),
            meta: { title: '上传数据', icon: 'upload' }
        },

        {
            path: '/operate',
            name: 'Operate',
            component: () => import('@/views/logs/operate/operate'),
            meta: { title: '内容生成', icon: 's-operation' }
        },
        {
            path: '/time',
            name: 'Time',
            component: () => import('@/views/logs/time/time'),
            meta: { title: '时间演化', icon: 'time' }
        },
        {
            path: '/comp',
            name: 'Comp',
            component: () => import('@/views/logs/comp/comp'),
            meta: { title: '对照分析', icon: 'compare' }
        },
    ]
}

export default logsRouter

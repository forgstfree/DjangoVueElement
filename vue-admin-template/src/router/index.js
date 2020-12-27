import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'/'el-icon-x' the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 */
export const constantRoutes = [
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },

  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },

  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [{
      path: 'dashboard',
      name: 'Dashboard',
      component: () => import('@/views/dashboard/index'),
      meta: { title: '仪表盘', icon: 'dashboard' }
    }]
  },

  {
    path: '/databases',
    // path: '/',
    component: Layout,
    children: [
      {
        path: '',
        name: 'Databases',
        component: () => import('@/views/test/databases/index'),
        meta: { title: '数据源', icon: 'databases' }
      }
    ]
  },

  {
    path: '/upload',
    component: Layout,
    children: [
      {
        path: '',
        name: 'Upload',
        component: () => import('@/views/test/upload/upload'),
        meta: { title: '上传数据', icon: 'upload' }
      }
    ]
  },

  {
    path: '/operate',
    component: Layout,
    children: [
      {
        path: '',
        name: 'Operate',
        component: () => import('@/views/test/operate/operate'),
        meta: { title: '内容生成', icon: 's-operation' }
      }
    ]
  },

  // {
  //   path: '/er',
  //   component: Layout,
  //   children: [
  //     {
  //       path: '',
  //       name: 'ER',
  //       component: () => import('@/views/test/compare/compare'),
  //       meta: { title: '增强ER', icon: 'compare' }
  //     }
  //   ]
  // },

  {
    path: '/time',
    component: Layout,
    children: [
      {
        path: '',
        name: 'Time',
        component: () => import('@/views/test/time/time'),
        meta: { title: '时间演化', icon: 'time' }
      }
    ]
  },
  {
    path: '/comp',
    component: Layout,
    children: [
      {
        path: '',
        name: 'Comp',
        component: () => import('@/views/test/comp/comp'),
        meta: { title: '对照分析', icon: 'compare' }
      }
    ]
  },

  // {
  //   path: '/fuse',
  //   component: Layout,
  //   name: 'Fuse',
  //   meta: {title: '数据融合', icon: 'fuse'},
  //   children: [
  //     {
  //       path: 'attribute',
  //       name: 'Attribute',
  //       component: () => import('@/views/test/fuse/attribute'),
  //       meta: { title: '属性融合', icon: 'attribute' }
  //     },
  //     {
  //       path: 'tuple',
  //       name: 'Tuple',
  //       component: () => import('@/views/test/fuse/tuple'),
  //       meta: { title: '元组融合', icon: 'row' }
  //     },
  //     {
  //       path: 'integrate',
  //       name: 'Integrate',
  //       component: () => import('@/views/test/fuse/integrate'),
  //       meta: { title: '综合融合', icon: 'integrate' }
  //     },

  //   ]
  // },

  {
    path: 'external-link',
    component: Layout,
    hidden: true,
    children: [
      {
        //         path: 'https://panjiachen.github.io/vue-element-admin-site/#/',
        path: 'http://10.9.20.160:8000/polls/',
        meta: { title: 'External Link', icon: 'link' }
      }
    ]
  },


  {
    path: '/test',
    component: Layout,
    name: 'Text',
    hidden: true,
    meta: { title: 'Text', icon: 'user' },
    children: [
      {
        path: 'book',
        name: 'Book',
        component: () => import('@/views/test/book/index'),
        meta: { title: 'Book', icon: 'list' }
      },
    ]
  },

  // 404 page must be placed at the end !!!
  { path: '*', redirect: '/404', hidden: true }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({ y: 0 }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router

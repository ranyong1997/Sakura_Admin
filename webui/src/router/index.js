import { createRouter, createWebHashHistory } from 'vue-router'
import myFun from '../utils/myFun'
import { ElMessage } from 'element-plus'
import NProgress from 'nprogress' //加载进度条
import 'nprogress/nprogress.css'
// 进度条配置项
NProgress.configure({
  showSpinner: false
})

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    meta: {
      title: '登录'
    },
    component: () => import('../views/login.vue')
  },
  {
    path: '/main',
    meta: {
      title: '基础'
    },
    // redirect: '/homePage',
    component: () => import('../views/main.vue'),
    children: [
      {
        path: '/homePage',
        meta: {
          title: '首页'
        },
        component: () => import('../views/homePage.vue')
      },
      // 功能
      {
        path: '/dialogDrag',
        meta: {
          title: '可拖拽弹框'
        },
        component: () => import('../views/content/dialogDrag.vue')
      },
      {
        path: '/wartermark',
        meta: {
          title: '添加水印'
        },
        component: () => import('../views/content/wartermark.vue')
      },
      {
        path: '/timePicker',
        meta: {
          title: '时间选择器'
        },
        component: () => import('../views/content/timePicker.vue')
      },
      {
        path: '/copy',
        meta: {
          title: '复制'
        },
        component: () => import('../views/content/copy.vue')
      },
      {
        path: '/qrcode',
        meta: {
          title: '二维码'
        },
        component: () => import('../views/content/qrcode.vue')
      },
      // {
      //   path: '/map',
      //   meta: {
      //     title: '地图'
      //   },
      //   component: () => import('../views/content/map.vue')
      // },
      {
        path: '/computerMonitor',
        meta: {
          title: '监测电脑信息'
        },
        component: () => import('../views/content/computerMonitor.vue')
      },
      // 模板
      {
        path: '/easyForm',
        meta: {
          title: '基础表单'
        },
        component: () => import('../views/form/easyForm.vue')
      },
      {
        path: '/tableOperation',
        meta: {
          title: '表格操作'
        },
        component: () => import('../views/form/tableOperation.vue')
      },
      {
        path: '/cardList',
        meta: {
          title: '基础表单'
        },
        component: () => import('../views/form/cardList.vue')
      },
      // 编辑器
      {
        path: '/textEditor',
        meta: {
          title: '富文本编辑器'
        },
        component: () => import('../views/editor/textEditor.vue')
      },
      // 异常页面
      {
        path: '/403',
        meta: {
          title: '403'
        },
        component: () => import('../views/abnormal/403.vue')
      },
      {
        path: '/404',
        meta: {
          title: '404'
        },
        component: () => import('../views/abnormal/404.vue')
      },
      {
        path: '/noData',
        meta: {
          title: '暂无数据'
        },
        component: () => import('../views/abnormal/noData.vue')
      },
      {
        path: '/build',
        meta: {
          title: '功能建设中'
        },
        component: () => import('../views/abnormal/build.vue')
      },
      {
        path: '/networkError',
        meta: {
          title: '网络不可用'
        },
        component: () => import('../views/abnormal/networkError.vue')
      },
      // 结果
      {
        path: '/successTip',
        meta: {
          title: '成功'
        },
        component: () => import('../views/tip/success.vue')
      },
      {
        path: '/errorTip',
        meta: {
          title: '错误'
        },
        component: () => import('../views/tip/error.vue')
      },
      {
        path: '/warningTip',
        meta: {
          title: '警告'
        },
        component: () => import('../views/tip/warning.vue')
      },
      // 工作流程
      {
        path: '/workflow',
        meta: {
          title: '工作流程'
        },
        component: () => import('../views/workflow/index.vue')
      },
      // 消息中心
      {
        path: '/messageCenter',
        meta: {
          title: '消息中心'
        },
        component: () => import('../views/message/messageCenter.vue')
      },
      // 权限管理
      {
        path: '/user',
        meta: {
          title: '用户管理'
        },
        component: () => import('../views/setting/user.vue')
      },
      {
        path: '/role',
        meta: {
          title: '角色管理'
        },
        component: () => import('../views/setting/role.vue')
      },
      {
        path: '/resource',
        meta: {
          title: '资源管理'
        },
        component: () => import('../views/setting/resource.vue')
      },
      // 新手引导
      {
        path: '/noviceGuide',
        meta: {
          title: '新手引导'
        },
        component: () => import('../views/noviceGuide/index.vue')
      }
    ]
  }
]
const router = createRouter({
  history: createWebHashHistory(),
  routes
})

//手动跳转的页面白名单
const whiteList = ['/login', '/404', '/403']

router.beforeEach((to, from, next) => {
  document.title = `lansoft | ${to.meta.title}` //添加title
  const user = myFun.getAccessToken() //获取token to.path !== '/login'
  NProgress.start() // 路由跳转前钩子函数中 - 执行进度条开始加载
  if (!to.matched.length) {
    next('/404')
  }
  if (user) {
    // console.log(user, '-=????')
    if (to.path === '/' || to.path === '/login') {
      next()
    } else {
      next()
    }
  } else {
    // console.log('bushi')
    if (whiteList.includes(to.path)) {
      console.log('-=whiteList?')
      //如果是白名单无须token则直接进入
      next()
    } else {
      console.log('-=!!!!!!!!!!!!!!!!!whiteList???')
      next('/login')
      ElMessage.error('无登陆凭证,无法访问,请先登陆!')
    }
  }
})

// 路由跳转后钩子函数中 - 执行进度条加载结束
router.afterEach(() => {
  NProgress.done()
})

export default router

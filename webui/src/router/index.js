/*
 * @Descripttion: 
 * @version: 
 * @Author: 冉勇
 * @Date: 2022-07-07 17:23:31
 * @LastEditTime: 2022-07-07 17:35:45
 */
import {
    createRouter,
    createWebHistory
} from 'vue-router'

const routerHistory = createWebHistory()

const router = createRouter({
    history: routerHistory,
    routes: [{
        path: '/',
    }, {
        path: '/foo',
        components: () => import('../views/foo.vue')
    }, {
        path: '/bar',
        components: () => import('../views/bar.vue')
    }]
})
export default router
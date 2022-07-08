/*
 * @Descripttion: 
 * @version: 
 * @Author: 冉勇
 * @Date: 2022-07-07 17:23:31
 * @LastEditTime: 2022-07-08 10:08:44
 */
import {
    createRouter,
    createWebHistory
} from 'vue-router'

const routerHistory = createWebHistory('/aProject/')

const router = createRouter({
    history: routerHistory,
    routes: [
        {
            path: '/',
        },
        {
            path: '/foo',
            component: () => import('../views/foo.vue')
        },
        {
            path: '/bar',
            component: () => import('../views/bar.vue')
        }
    ]
})
export default router
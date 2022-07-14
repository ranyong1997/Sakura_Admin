/*
 * @Descripttion: 
 * @version: 
 * @Author: 冉勇
 * @Date: 2022-07-08 16:14:04
 * @LastEditTime: 2022-07-13 10:55:10
 */
import { createApp } from 'vue'
import { createPinia } from 'pinia'   // 引入pinia
import ElementPlus from 'element-plus'
import store from './store/index.js'
import 'element-plus/dist/index.css'
import './assets/css/font-awesome.min.css' //font 样式
import animated from 'animate.css' //动画库
import * as ELIcons from '@element-plus/icons-vue' // 引入图标
import { ElMessage } from 'element-plus' // 消息提示
import * as _public from './utils/utils' //一些全局方法
import filters from './filters' //全局过滤器
import { dialogDrag, copy } from './directives/index' //自定义指令
import moment from 'moment' //日期时间格式化
import '@wangeditor/editor/dist/css/style.css' // 富文本编辑器样式

import App from './App.vue'
import router from './router'

const app = createApp(App)

app.config.globalProperties._public = _public //公共方法
app.config.globalProperties.$filters = filters //公共过滤器
app.config.globalProperties.$message = ElMessage // 全局消息提示
app.config.globalProperties.$moment = moment // 时间格式化

for (let iconName in ELIcons) {
  app.component(iconName, ELIcons[iconName])
}
app.use(dialogDrag) // 引入拖拽指令
app.use(createPinia()) // 引入pinia
app.use(copy) // 引入复制指令
app.use(animated) // 引入动画库
app.use(ElementPlus)  // 引入element-plus
app.use(router) // 引入路由
app.use(store)  // 引入vuex
app.mount('#app')

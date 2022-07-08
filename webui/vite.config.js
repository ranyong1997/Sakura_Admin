/*
 * @Descripttion: 
 * @version: 
 * @Author: 冉勇
 * @Date: 2022-07-07 17:17:22
 * @LastEditTime: 2022-07-08 10:09:04
 */
import {
  defineConfig
} from 'vite'
import vue from '@vitejs/plugin-vue'
import Components from 'unplugin-vue-components/vite'
import AutoImport from 'unplugin-auto-import/vite'
import {
  ElementPlusResolver
} from 'unplugin-vue-components/resolvers'
// https://vitejs.dev/config/
export default defineConfig({
  base:'/aProject/',
  plugins: [vue(),
  AutoImport({//这里
    resolvers: [ElementPlusResolver()],
  }),
  Components({//这里
    resolvers: [ElementPlusResolver()],
  }),
  ]
})
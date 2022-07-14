/*
 * @Descripttion: 
 * @version: 
 * @Author: 冉勇
 * @Date: 2022-07-07 17:17:22
 * @LastEditTime: 2022-07-11 15:56:41
 */
import { defineConfig } from 'vite' // 引入vite
import vue from '@vitejs/plugin-vue'  // 导入vue插件
import path from 'path' // 路径
export default defineConfig({
  plugins: [vue()],

  // 配置dev服务
  server: {
    host: '0.0.0.0',
    port: 3000
  },
  resolve: {
    // 别名,避免在文件中引入别的组件的时候写太长的路径
    alias: {
      // eslint-disable-next-line no-undef
      '@': path.join(__dirname, 'src'),
      // eslint-disable-next-line no-undef
      '~': path.join(__dirname, 'node_modules'),
      // eslint-disable-next-line no-undef
      api: path.resolve(__dirname, 'src/api'),
      // eslint-disable-next-line no-undef
      components: path.resolve(__dirname, 'src/components'),
      // eslint-disable-next-line no-undef
      image: path.resolve(__dirname, 'src/assets/image'),
      // eslint-disable-next-line no-undef
      styles: path.resolve(__dirname, 'src/styles'),
      // eslint-disable-next-line no-undef
      utils: path.resolve(__dirname, 'src/utils'),
      // eslint-disable-next-line no-undef
      views: path.resolve(__dirname, 'src/views')
    }
  },
  // 反向代理
  proxy: {
    '/api': {
      target: 'http://localhost:3000',
      changeOrigin: true,
      rewrite: (path) => path.replace(/^\/api/, '')
    }
  }
})
/*
 * @Descripttion: 封装axios
 * @version: 
 * @Author: 冉勇
 * @Date: 2022-07-09 08:33:10
 * @LastEditTime: 2022-07-12 16:52:16
 */
import axios from 'axios'

// axios 全局配置
axios.defaults.timeout = 7 * 24 * 60 // 超时时间
axios.defaults.withCredentials = false // 跨域凭证
// axios.defaults.baseURL = 'http://192.168.1.196:9527'  //自动加在url前面
axios.defaults.baseURL = 'http://127.0.0.1:8001'  //自动加在url前面 本地服务
// 注意,实例中无法使用全局拦截器

// request拦截器
axios.interceptors.request.use(
  (config) => {
    return config
  }, (error) => {
    console.log('request拦截器报错');
    return Promise.reject(error)
  }
)

// respone拦截器
axios.interceptors.response.use(
  (response) => {
    return response
  }, (error) => {
    console.log('respone拦截器报错');
    return Promise.reject(error)
  }
)

export default axios

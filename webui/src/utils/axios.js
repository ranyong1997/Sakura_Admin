/*
 * @Descripttion: 
 * @version: 
 * @Author: 冉勇
 * @Date: 2022-07-09 08:33:10
 * @LastEditTime: 2022-07-09 10:33:18
 */
import axios from 'axios'

// axios 全局配置
axios.defaults.timeout = 7*24*60 // 超时时间
axios.defaults.withCredentials = false // 是否携带cookie

// 注意,实例中无法使用全局拦截器

// request拦截器
axios.interceptors.request.use(
  (config) => {
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// respone拦截器
axios.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    return Promise.reject(error)
  }
)

export default axios

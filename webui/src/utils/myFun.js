/*
 * @Descripttion: 
 * @version: 
 * @Author: 冉勇
 * @Date: 2022-07-08 16:14:04
 * @LastEditTime: 2022-07-08 16:29:38
 */
import lscache from 'lscache'
import { ElLoading } from 'element-plus'

// 设置lscache缓存时间以秒计,并自动清除过期的缓存
lscache.setExpiryMilliseconds(1000)
lscache.flushExpired()

/**
 * 获取接口基本地址
 */
function getBaseApiUrl() {
  let res = ''
  if (typeof GLOBAL_API_URL !== undefined && GLOBAL_API_URL !== '') {
    res = GLOBAL_API_URL
  } else {
    res = import.meta.env.VITE_API_URL
  }
  return res
}

/**
 * 获取lscache对象
 * @returns lscache
 */
function getCache() {
  return lscache
}

/**
 * 清空lscache缓存
 */
function clearCache() {
  lscache.flush()
}

// 显示loading
function showLoading() {
  return ElLoading.service({
    lock: false,
    text: '加载中···',
    spinner: 'el-icon-loading',
    background: 'rgba(0, 0, 0, 0.7)'
  })
}

// 防抖(防止重复提交)
const debounce = (function () {
  let timer = 0
  return function (callback, ms) {
    clearTimeout(timer)
    timer = setTimeout(callback, ms)
  }
})()

/**
 * 设置用户accessToken令牌到浏览器存储
 * @param {string} token 用户令牌
 * @param {int} ttl 有效期,秒
 */
const setAccessToken = function (token, ttl) {
  lscache.set('accessToken', token, parseInt(ttl, 10))
}

/**
 * 获取用户的accessToken令牌
 */
const getAccessToken = function () {
  let res = lscache.get('accessToken')
  if (!res) res = ''
  return res
}

/**
 * 删除用户的accessToken令牌
 */
const delAccessToken = function () {
  lscache.remove('accessToken')
}

export default {
  getBaseApiUrl,
  getCache,
  clearCache,
  showLoading,
  debounce,
  setAccessToken,
  getAccessToken,
  delAccessToken
}

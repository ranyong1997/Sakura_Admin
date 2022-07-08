import Qs from 'qs'
import axios from './axios'
import myFun from './myFun'
import router from '../router'
import { ElMessage } from 'element-plus'
import Kdatetime from '@kakuilan/js-helper/lib/datetime'
import Kencrypt from '@kakuilan/js-helper/lib/encrypt'

const pendingMap = new Map()
let loading = null

export default function (config, options) {
  //判断是否要展示loading 需要配置则在增加{loading:true} 默认false
  let loadingStatus = options?.loading || undefined
  //判断是否要展示消息 需要配置则在增加{message:true} 默认false
  let messageStatus = options?.message || undefined
  //判断是否展示未格式化的数据 需要配置则在增加{rawData:true} 默认false
  let rawData = options?.rawData || false
  let url = config.url ?? ''

  // 创建axios实例用于请求接口
  // xhr,即为XMLHttpRequest请求对象
  const xhr = axios.create({
    timeout: 5000,
    baseURL: myFun.getBaseApiUrl(),
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8'
    }
  })

  // request拦截器
  xhr.interceptors.request.use(
    (config) => {
      removePending(config)
      addPending(config)
      //发起请求的时候 展示loading
      !loadingStatus || (loading = myFun.showLoading())

      // 请求时间
      let time = Kdatetime.nowMilli()
      let token = myFun.getAccessToken()

      if (typeof config.params === 'object') {
        config.params['client_time'] = time
        config.params['access_token'] = token
      } else {
        config.params = {
          client_time: time,
          access_token: token
        }
      }

      if (!import.meta.env.PROD) {
        console.log('xhr request:', url, config)
      }

      // 在请求之前对请求数据进行操作
      config.transformRequest = [
        (data) => {
          // data类型:string , Buffer, ArrayBuffer, FormData or Stream
          if (data instanceof FormData) {
            return data
          }

          data = Qs.stringify(data)
          return data
        }
      ]

      // 在传递给 then/catch 前,允许修改响应数据
      config.transformResponse = [
        function (data) {
          // 对 data 进行任意转换处理
          try {
            let res = JSON.parse(data) //返回数据类型转换

            if (res.code === 200) {
              !messageStatus || ElMessage.success(res.msg)
            } else if (res.code === 500) {
              !messageStatus || ElMessage.error(res.msg)
            } else {
              !messageStatus || ElMessage.warning(res.msg)
            }
          } catch (e) {}
          return data
        }
      ]

      return config
    },
    (error) => {
      return Promise.reject(error)
    }
  )

  // 响应拦截器
  xhr.interceptors.response.use(
    (response) => {
      //返回请求的时候关闭loading
      !loadingStatus || loading.close(), (loading = null)
      if (!import.meta.env.PROD) {
        console.log('xhr response:', url, response)
      }

      //http状态码
      if (response.status === 200) {
        //接口状态码
        let data = JSON.parse(response.data)
        if (data.code === 200) {
          //如果返回成功则返回数据 错误只能拿到null
          return rawData ? response : data
        } else {
          httpErrorStatusHandle(data.code, data.msg, null)
          return null
        }
      } else {
        return null
      }
    },
    (error) => {
      //返回请求的时候关闭loading
      !loadingStatus || loading.close(), (loading = null)
      if (!import.meta.env.PROD) {
        console.log('xhr error:', url, error)
      }

      //失败处理
      httpErrorStatusHandle(null, null, error)
      return Promise.reject(error)
    }
  )

  return xhr(config)
}

/**
 * 生成唯一的每个请求的唯一key
 * @param config 请求配置
 * @returns {string|*}
 */
function getPendingKey(config) {
  let { url, method, params, data } = config

  // response里面返回的config.data是个字符串对象
  if (typeof data === 'string') data = JSON.parse(data)

  let str = [url, method, JSON.stringify(params), JSON.stringify(data)].join()

  return Kencrypt.md5(str)
}

/**
 * 储存每个请求的唯一cancel回调, 以此为标识
 * @param {*} config
 */
function addPending(config) {
  const pendingKey = getPendingKey(config)
  config.cancelToken =
    config.cancelToken ||
    new axios.CancelToken((cancel) => {
      if (!pendingMap.has(pendingKey)) {
        pendingMap.set(pendingKey, cancel)
      }
    })
}

/**
 * 删除重复的请求
 * @param {*} config
 */
function removePending(config) {
  const pendingKey = getPendingKey(config)
  if (pendingMap.has(pendingKey)) {
    const cancelToken = pendingMap.get(pendingKey)
    cancelToken(pendingKey)
    pendingMap.delete(pendingKey)
  }
}

function httpErrorStatusHandle(status, msg, error) {
  console.log('--------------err', status, msg, error)
  if (!status) {
    status = error.response.status ?? 500
  }
  if (!msg) {
    msg = ''
  }

  // 处理被取消的请求
  if (error && axios.isCancel(error)) {
    return console.warn('请求的重复请求：' + error.message)
  }

  if (status && !msg) {
    switch (status) {
      case 302:
        msg = '接口重定向了！'
        break
      case 400:
        msg = '参数不正确！'
        break
      case 401:
        msg = '您未登录，或者登录已经超时，请先登录！'
        break
      case 403:
        msg = '您没有权限操作！'
        break
      case 404:
        msg = `请求地址不存在: ${error.response.config.url}`
        break // 在正确域名下
      case 408:
        msg = '请求超时！'
        break
      case 409:
        msg = '系统已存在相同数据！'
        break
      case 500:
        msg = '服务器内部错误！'
        break
      case 501:
        msg = '服务未实现！'
        break
      case 502:
        msg = '网关错误！'
        break
      case 503:
        msg = '服务不可用！'
        break
      case 504:
        msg = '服务暂时无法访问，请稍后再试！'
        break
      case 505:
        msg = 'HTTP版本不受支持！'
        break
      default:
        msg = '异常问题，请联系管理员！'
        break
    }
  }

  if (error) {
    if (error.message.includes('timeout')) msg = '网络请求超时！'
    if (error.message.includes('Network'))
      msg = window.navigator.onLine ? '服务端异常！' : '你断网了！'
  }

  let denyStatus = [401, 402, 403]
  if (denyStatus.includes(status)) {
    ElMessage.info(msg)

    //如果登陆失效立马回到登录页
    setTimeout(() => {
      router.push({
        path: '/login'
      })
    }, 2500)
  } else {
    ElMessage.error(msg)
  }
}

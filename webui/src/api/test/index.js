import xhr from '../../utils/xhr'
import store from '../../store'

// 测试接口
const ApiTest = {
  //get方法
  get: function (data) {
    return xhr(
      {
        url: '/test/home/index',
        method: 'get',
        params: data
      },
      {
        message: true
      }
    )
  },
  //post方法
  post: function (data) {
    return xhr(
      {
        url: '/test/home/post',
        method: 'post',
        data: data
      },
      {
        message: true
      }
    )
  },
  //不存在的接口
  notfound: function () {
    return xhr({
      url: '/test/home/notfound',
      method: 'get'
    })
  }
}

export default ApiTest

import myFun from '../../utils/myFun'
const auth = {
  state: {
    logined: false,
    avatar: '',
    uid: 0,
    nickName: '',
    accessToken: ''
  },
  getters: {
    logined: (state) => state.logined
  },
  //mutations的方法名统一大写
  mutations: {
    //使用 commit('SET_ACCESS_TOKEN', [accessToken, ttl])
    SET_ACCESS_TOKEN: (state, [accessToken, ttl]) => {
      state.accessToken = accessToken
      if (accessToken !== '') {
        myFun.setAccessToken(accessToken, ttl)
        state.logined = true
      } else {
        myFun.delAccessToken()
        state.logined = false
      }
    }
  },
  actions: {}
}
export default auth

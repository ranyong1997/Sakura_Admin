<template>
  <div class="login-container">
    <div class="login-body">
      <div class="logo">
        <img alt src="../assets/image/LG.png" />
        <p>Sakura_Admin</p>
      </div>
      <div>
        <ElForm ref="loginRef" :model="param" :rules="loginRules" hide-required-asterisk @submit.prevent>
          <ElFormItem prop="username">
            <ElInput v-model.trim="param.username" clearable placeholder="请输入用户名" prefix-icon=""></ElInput>
          </ElFormItem>
          <ElFormItem prop="password">
            <ElInput v-model.trim="param.password" clearable placeholder="请输入密码" prefix-icon="" show-password
              @keyup.enter="submitForm"></ElInput>
          </ElFormItem>
          <ElFormItem>
            <ElButton :loading="loading" style="width: 100%" type="primary" @click="submitForm()">登录</ElButton>
          </ElFormItem>
        </ElForm>
      </div>
    </div>
  </div>
</template>
<script>
import {
  defineComponent,
  getCurrentInstance,
  toRefs,
  reactive,
  ref,
  onMounted
} from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from 'vuex'
import myFun from '../utils/myFun.js'
import axios from '.././utils/axios'
export default defineComponent({
  setup() {
    const store = useStore() //vuex仓库
    let { proxy } = getCurrentInstance() // vue原型
    const loginRef = ref(null) //登录ref
    const registerRef = ref(null) //注册ref
    const router = useRouter() //路由
    const state = reactive({
      param: {
        username: 'admin',
        password: '123456'
      }, //登录账号
      loginRules: {
        //登陆验证
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' }
        ],
        password: [{ required: true, message: '请输入密码', trigger: 'blur' }]
      },
      loading: false //缓冲
    })
    onMounted(() => {
      document.onkeydown = function (e) {
        let el = e || event || window.event
        if (el && el.keyCode === 13) {
          submitForm()
        }
      }
    })
    const submitForm = () => {
      state.loading = true
      //登陆
      loginRef.value.validate((valid) => {
        if (valid) {
          let formdata = new FormData()
          formdata.append('username', "admin")
          formdata.append('password', "123456")
          axios.post('/api/admin/login/access_token/', formdata)
            .then(function (response) {
              proxy._public.debounce(() => {
                myFun.setAccessToken(state.param.username, 2000)
                router.push({ path: '/homePage' })
                state.loading = false
              }, 300)
            })
            .catch(function (error) {
              console.log(error);
            });
        }
      })
    }
    return {
      ...toRefs(state),
      loginRef,
      registerRef,
      submitForm
    }
  }
})
</script>
<style lang="scss" scoped>
.login-container {
  position: relative;
  width: 100%;
  height: 100vh;
  background-size: cover;
  background-image: url('image/n-y.jpg');

  .login-body {
    box-shadow: 0px 0px 10px 0px #646464;
    border-radius: 5px;
    background: radial-gradient(white, transparent);
    position: absolute;
    left: 50%;
    top: 50%;
    width: 400px;
    overflow: hidden;
    padding: 0 26px 24px 26px;
    box-sizing: border-box;
    margin-left: -198px;
    margin-top: -255px;

    .logo {
      padding: 12px;
      text-align: center;

      img {
        height: 55px;
      }

      p {
        font-size: 24px;
        padding: 2px 0px;
      }

      span {
        font-size: 14px;
        color: #909399;
      }
    }

    .l-title {
      padding: 8px 0 24px 0;
      font-size: 20px;
      color: #121212;
      font-weight: 550;
      text-align: center;
    }
  }

  .other-content {
    display: flex;
    justify-content: space-between;
  }
}
</style>

<template>
  <div class="zan-header">
    <div class="collapse-btn" @click="switchCollapse">
      <i v-if="collapse" class="fa fabtn fa-indent"></i>
      <i v-else class="fa fabtn fa-dedent"></i>
    </div>
    <div class="collapse-right">
      <ElTooltip class="item" effect="dark" content="全屏" placement="bottom">
        <span class="faSpan">
          <i class="fa fa-arrows-alt" @click="requestFullScreen('body')"></i>
        </span>
      </ElTooltip>

      <ElTooltip
        class="item"
        effect="dark"
        content="消息中心"
        placement="bottom"
      >
        <span class="faSpan">
          <ElBadge is-dot class="item">
            <i class="fa faPad fa-bell-o" @click="toGetMessage"></i>
          </ElBadge>
        </span>
      </ElTooltip>
      <!-- 用户名下拉菜单 -->
      <ElDropdown size="small" trigger="click" @command="handleCommand">
        <span class="el-dropdown-link btn_username_group">
          <span class="btn_username" :title="username">{{ username }}</span>
          <ElIcon><CaretBottom /></ElIcon>
        </span>
        <template #dropdown>
          <ElDropdownMenu>
            <ElDropdownItem divided command="signOut">退出登录</ElDropdownItem>
            <ElDropdownItem command="versionLog" divided
              >版本日志</ElDropdownItem
            >
            <ElDropdownItem command="baseInfo" divided>基本信息</ElDropdownItem>
            <ElDropdownItem command="checkPass" divided
              >修改密码</ElDropdownItem
            >
          </ElDropdownMenu>
        </template>
      </ElDropdown>
      <!-- 用户头像 -->
      <div class="user-avatar">
        <!-- <img src="../../assets/image/LG.png" /> -->
        <img :src="'data:image/svg+xml;utf8,' + generateFromString" />
        <!-- <ElAvatar icon="el-icon-user-solid"> </ElAvatar> -->
      </div>
    </div>
    <CheckPass v-model:passVisible="passVisible"></CheckPass>
    <BaseInfo ref="baseInfoRef" v-model:baseVisible="baseVisible"></BaseInfo>
    <VersionLog v-model:versionVisible="versionVisible"></VersionLog>
  </div>
</template>
<script>
import {
  defineComponent,
  getCurrentInstance,
  toRefs,
  reactive,
  ref,
  computed
} from 'vue'
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import myFun from '../../utils/myFun.js'
import CheckPass from '../Setting/checkPass.vue'
import BaseInfo from '../Setting/baseInfo.vue'
import VersionLog from '../Setting/versionLog.vue'
import { generateFromString } from 'generate-avatar' // 自动生成图片
export default defineComponent({
  name: 'ZanHeader',
  components: {
    CheckPass,
    BaseInfo,
    VersionLog
  },
  setup(context, props) {
    let { proxy } = getCurrentInstance() // vue原型

    const store = useStore() //vuex
    const router = useRouter() //路由
    const baseInfoRef = ref()
    const state = reactive({
      generateFromString: generateFromString(myFun.getAccessToken()),
      collapse: computed(() => store.state.collapse),
      username: computed(() => myFun.getAccessToken()),
      passVisible: false, //修改密码弹框
      baseVisible: false, //基本信息弹框
      versionVisible: false, //版本日志弹框
      driver: null //引导实例
    })

    const requestFullScreen = (element) => {
      //进入全屏 退出全屏
      const isFullScreen =
        document.fullScreen ||
        document.mozFullScreen ||
        document.webkitIsFullScreen ||
        document.msFullscreenElement //判断窗口是否全屏
      let ele = document.querySelector(element) || document.documentElement //获取元素
      if (!isFullScreen) {
        if (ele.requestFullscreen) {
          ele.requestFullscreen()
        } else if (ele.mozRequestFullScreen) {
          ele.mozRequestFullScreen()
        } else if (ele.webkitRequestFullscreen) {
          ele.webkitRequestFullscreen()
        } else if (ele.msRequestFullscreen) {
          ele.msRequestFullscreen()
        }
      } else {
        if (document.exitFullScreen) {
          document.exitFullScreen()
        } else if (document.mozCancelFullScreen) {
          document.mozCancelFullScreen()
        } else if (document.webkitExitFullscreen) {
          document.webkitExitFullscreen()
        } else if (element.msExitFullscreen) {
          element.msExitFullscreen()
        }
      }
    }

    const switchCollapse = () => {
      //菜单栏展开关闭
      setTimeout(() => {
        store.commit('switchCollapse', !state.collapse)
      }, 0)
    }

    const handleCommand = (command) => {
      //用户下拉菜单
      if (command == 'signOut') {
        myFun.delAccessToken() //清空token 1秒后回到登录页
        store.commit('delRightMenu', {
          //退出清空所有菜单
          whiteTags: []
        })
        router.push('/login')
        proxy.$message.success('登出成功')
      } else if (command == 'checkPass') {
        //打开修改密码弹框
        state.passVisible = true
      } else if (command == 'baseInfo') {
        //打开基本信息弹框
        baseInfoRef.value.openBaseInfo(store.state.user.user)
      } else if (command == 'versionLog') {
        //打开版本日志弹框
        state.versionVisible = true
      }
    }

    const toGetMessage = () => {
      //进入消息中心
      router.push('/messageCenter')
    }

    return {
      ...toRefs(state),
      baseInfoRef,
      switchCollapse,
      handleCommand,
      toGetMessage,
      requestFullScreen
    }
  }
})
</script>
<style lang="scss" scoped>
.zan-header {
  box-sizing: border-box;
  width: 100%;
  height: 64px;
  font-size: 18px;
  color: #616161;
  background: #fff;
  display: flex;
  justify-content: space-between;

  .collapse-btn {
    // float: left;
    padding: 0px 15px 0 15px;
    cursor: pointer;
    line-height: 64px;
  }

  .el-icon-s-fold,
  .el-icon-s-unfold {
    font-size: 25px;
    cursor: pointer;
  }

  .collapse-right {
    float: right;
    padding-right: 20px;
    height: 64px;
    display: flex;
    align-items: center;
    justify-content: space-between;
    .faSpan {
      padding-right: 15px;
      cursor: pointer;
    }
  }

  .user-avatar {
    margin: 0 15px 0 5px;
  }

  img {
    display: block;
    width: 40px;
    height: 40px;
    border-radius: 50%;
  }
  .btn_username_group {
    display: flex;
    justify-content: space-between;
    .btn_username {
      text-align: right;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
      width: 60px;
      padding-right: 8px;
    }
  }
}
</style>

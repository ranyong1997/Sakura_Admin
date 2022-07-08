<template>
  <div class="tag_content">
    <div v-if="tagsList.length > 0" class="tags">
      <ElTag
        v-for="(tag, index) in tagsList"
        :key="tag"
        type
        :class="path === tag.path ? 'tag_check' : 'tag_nocheck'"
        :closable="tag.path == '/homePage' ? false : true"
        size="default"
        effect="plain"
        :disable-transitions="false"
        @close="aClosingTag(tag, index)"
        @click="triggerTag(tag, 'go')"
        >{{ tag.title }}</ElTag
      >
    </div>
    <ElDropdown v-if="tagsList.length > 0" placement="top" @command="rightMenu">
      <span class="el-dropdown-link">
        <ElIcon><ArrowDown /></ElIcon>
        <!-- <i class="el-icon-arrow-down el-icon--right"></i> -->
      </span>
      <template #dropdown>
        <ElDropdownMenu>
          <ElDropdownItem command="all">{{ '关闭全部' }}</ElDropdownItem>
          <ElDropdownItem command="other">{{ '关闭其他' }}</ElDropdownItem>
        </ElDropdownMenu>
      </template>
    </ElDropdown>
  </div>
</template>
<script>
import {
  defineComponent,
  getCurrentInstance,
  toRefs,
  reactive,
  ref,
  watch,
  computed,
  onMounted
} from 'vue'
import { useRoute, useRouter, onBeforeRouteUpdate } from 'vue-router'
import { useStore } from 'vuex'
import { ElMessage } from 'element-plus'
// import { transitionLocal } from '../../locales/i18n'
export default defineComponent({
  name: 'Tags',
  setup() {
    const store = useStore() //vuex仓库
    const route = useRoute() //路由
    const router = useRouter() //路由
    let { proxy } = getCurrentInstance() // vue原型
    const state = reactive({
      tagsList: computed(() => store.state.tagsList), //标签仓库
      path: '' //选中标签
    })

    const setTags = (route) => {
      // console.log(route, 'ddddoododoo---------')
      // 设置标签
      const isExist = state.tagsList.some((item) => {
        return item.path === route.fullPath
      })
      if (!isExist) {
        if (state.tagsList.length >= 10) {
          //如果标签到10个再选择就将最初的删除
          store.commit('delTags', { index: 0 })
        }
        store.commit('setTags', {
          name: route.name,
          title: route.meta.title,
          path: route.fullPath
        })
      }
    }
    const aClosingTag = (tag, index) => {
      //删除标签
      if (state.tagsList.length <= 1) {
        //最后一个标签不能删
        ElMessage.warning({
          message: '最后一个标签了哦！',
          type: 'warning'
        })
        return false
      }
      store.commit('delTags', { index: index })
      triggerTag(state.tagsList[state.tagsList.length - 1], 'go')
    }
    const triggerTag = (tag, type) => {
      // console.log(tag, type, '9999999')
      //选择标签
      // debugger
      proxy._public.debounce(() => {
        state.path = tag.path
        if (type) {
          //如果是点击标签则进行路由跳转
          router.push(tag.path)
        }
      }, 100)
    }
    const rightMenu = (menu) => {
      //右菜单操作
      let whiteTags = ['/homePage']
      if (state.path !== whiteTags[0] && menu === 'other') {
        whiteTags.push(state.path)
      }
      store.commit('delRightMenu', {
        whiteTags
      })
      router.push(whiteTags[whiteTags.length - 1])
    }

    onBeforeRouteUpdate((to) => {
      // console.log(to, '00000000000000000')
      //监听路由变动
      setTags(to)
      triggerTag(to)
    })
    onMounted(() => {
      // console.log(route, 'shshshhsh688888888888888888')
      //监听路由变动
      setTags(route)
      triggerTag(route)
    })

    return {
      ...toRefs(state),
      setTags,
      aClosingTag,
      triggerTag,
      rightMenu
    }
  }
})
</script>
<style lang="scss" scoped>
.tag_content {
  padding: 6px 0px;
  margin: 0px 12px;
  box-sizing: border-box;
  white-space: nowrap;
  display: flex;
  justify-content: space-between;
  align-items: center;
  .tags {
    width: calc(100vw - 310px);
    overflow: auto;
    text-align: left;
  }
  .el-tag {
    cursor: pointer;
    margin-right: 8px;
    height: 30px;
    padding: 0px 13px 0 9px;
    line-height: 28px;
    border-radius: 0;
  }
  ::v-deep(.el-tag .el-icon-close) {
    color: rgb(97, 97, 97) !important;
  }
  ::v-deep(.el-tag .el-icon-close:hover) {
    background: none;
  }
  .tag_check {
    background-color: rgb(255, 255, 255) !important;
    border-color: rgb(255, 255, 255) !important;
    color: #409eff !important;
  }
  .tag_nocheck {
    background-color: rgb(255, 255, 255) !important;
    border-color: rgb(255, 255, 255) !important;
    color: rgb(97, 97, 97) !important;
  }
  .el-dropdown-link {
    
    height: 26px;
    display: flex;
    width: 70px;
    background: #fff;
    justify-content: center;
    align-items: center;
  }
}
</style>

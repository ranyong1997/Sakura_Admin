<template>
  <div class="app-wrapper">
    <ElContainer style="height: 100vh">
      <ElAside style="width: auto">
        <SideBar></SideBar>
      </ElAside>
      <ElContainer>
        <ElHeader height="64px">
          <Header></Header>
        </ElHeader>
        <ElMain>
          <Tags></Tags>
          <div class="content">
            <RouterView v-slot="{ Component }">
              <Transition
                appear
                appear-active-class="animate__animated animate__pulse"
                enter-active-class="animate__animated animate__fadeIn"
                name="fade"
              >
                <!--进入 enter-active-class   移出 leave-active-class  初始 appear-active-class-->
                <Component :is="Component" v-if="Component"></Component>
              </Transition>
            </RouterView>
            <ElBacktop target=".content"></ElBacktop>
          </div>
        </ElMain>
      </ElContainer>
    </ElContainer>
  </div>
</template>
<script>
import {
  defineComponent,
  toRefs,
  reactive,
  ref,
  computed,
  watchEffect,
  watch
} from 'vue'
import SideBar from '../components/SideBar/index.vue'
import Header from '../components/Header/index.vue'
import Tags from '../components/Tags/index.vue'
import { useStore } from 'vuex'

export default defineComponent({
  name: 'Main',
  components: {
    SideBar,
    Header,
    Tags
  },
  setup() {
    const store = useStore()

    if (sessionStorage.getItem('store')) {
      store.replaceState(
        Object.assign(
          {},
          store.state,
          JSON.parse(sessionStorage.getItem('store'))
        )
      )
    }
    // 在页面刷新时将store保存到sessionStorage里
    window.addEventListener('beforeunload', () => {
      sessionStorage.setItem('store', JSON.stringify(store.state))
    })
    const state = reactive({})
    return {
      ...toRefs(state)
    }
  }
})
</script>
<style lang="scss" scoped>
.app-wrapper {
  width: 100%;
  height: 100%;
  overflow: hidden;

  .el-aside {
    position: relative;
    overflow: hidden;
  }

  .el-header,
  .el-main {
    padding: 0;
  }

  .el-main {
    background: #f5f7f9;

    .content {
      padding: 24px;
      box-sizing: border-box;
      margin: 0px 8px 0 8px;
      background: #ffffff;
      overflow-x: hidden;
      overflow-y: auto;
      height: calc(100vh - 115px);
      color: #5e6d82;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.12), 0 0 6px rgba(0, 0, 0, 0.04);
    }
  }

  .el-affix--fixed,
  .el-overlay {
    right: 8px !important;
    position: fixed;
  }
}
</style>

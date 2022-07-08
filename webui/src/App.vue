<template>
  <!-- <img alt="Vue logo" src="./assets/logo.png" />
  <HelloWorld msg="Hello Vue 3 + Vite" /> -->
  <ElConfigProvider :locale="locale">
    <RouterView />
  </ElConfigProvider>
</template>
<script>
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup
// import HelloWorld from './components/HelloWorld.vue'
import { defineComponent, toRefs, reactive } from 'vue'
import { ElConfigProvider } from 'element-plus'
import zhCn from 'element-plus/lib/locale/lang/zh-cn'
export default defineComponent({
  name: 'App',
  components: {
    // HelloWorld,
    ElConfigProvider
  },
  setup() {
    const state = reactive({
      locale: zhCn
    })

    return {
      ...toRefs(state)
    }
  }
})
</script>
<style lang="scss">
@import './styles/element-ui.scss';
@import './styles/index.scss';
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
.el-form-item__label {
  line-height: 40px !important;
}
</style>

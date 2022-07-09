<!--
 * @Descripttion: 
 * @version: 
 * @Author: 冉勇
 * @Date: 2022-07-09 08:33:10
 * @LastEditTime: 2022-07-09 09:37:49
-->
<template>
  <ElConfigProvider :locale="locale">
    <RouterView />
  </ElConfigProvider>
</template>
<script>
import { defineComponent, toRefs, reactive } from 'vue'
import { ElConfigProvider } from 'element-plus'
import zhCn from 'element-plus/lib/locale/lang/zh-cn'

export default defineComponent({
  name: 'App',
  components: {
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

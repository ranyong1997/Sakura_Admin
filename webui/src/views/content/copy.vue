<template>
  <ElSpace direction="vertical">
    <ElCard class="box-card" style="width: 60vw">
      <template #header>
        <div class="card-header">
          <span>指令复制</span>
        </div>
      </template>
      <div class="text item">
        <ElButton
          v-copy="'copydir'"
          type="text"
          class="copydir"
          data-clipboard-text="我是指令复制"
          >我是指令复制(点击复制)</ElButton
        >
      </div>
    </ElCard>

    <ElCard class="box-card m-t8" style="width: 60vw">
      <template #header>
        <div class="card-header">
          <span>组件内方法复制</span>
        </div>
      </template>
      <div class="text item">
        <ElButton
          type="text"
          class="copyBtn"
          data-clipboard-text="我是组件内方法复制"
          @click="copy"
          >我是组件内方法复制(点击复制)</ElButton
        >
      </div>
    </ElCard>
  </ElSpace>
</template>
<script>
import Clipboard from 'clipboard'
import { ElMessage } from 'element-plus'
import { defineComponent } from 'vue'
export default defineComponent({
  setup() {
    const copy = () => {
      let clipboard = new Clipboard('.copyBtn')
      clipboard.on('success', (e) => {
        ElMessage({
          message: `组件内方法复制成功`,
          type: 'success'
        })
        // 释放内存
        clipboard.destroy()
      })
      clipboard.on('error', (e) => {
        // 不支持复制
        //console.log('该浏览器不支持自动复制')
        // 释放内存
        clipboard.destroy()
      })
    }
    return {
      copy
    }
  }
})
</script>

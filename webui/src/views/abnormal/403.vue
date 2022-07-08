<template>
  <div class="thereIsNo">
    <ElResult :image-size="400">
      <template #icon>
        <img class="abnormal-img" src="/src/assets/image/403.svg" alt />
      </template>
      <template #extra>
        <h2 class="abnormal-tip">很抱歉，您暂无权限访问</h2>
        <ElButton type="text" @click="router.push({ path: '/homePage' })"
          >返回首页</ElButton
        >
      </template>
    </ElResult>
  </div>
</template>

<script>
import { defineComponent } from 'vue'
import { useRouter } from 'vue-router'

export default defineComponent({
  setup() {
    const router = useRouter() //路由

    return {
      router
    }
  }
})
</script>

<template>
  <ElSpace direction="vertical">
    <ElCard class="box-card" style="width: 60vw">
      <template #header>
        <div class="card-header">
          <span>输入内容展示二维码</span>
        </div>
      </template>
      <div class="text item">
        <ElInput v-model="text" placeholder="输入内容展示二维码" />
        <img v-if="text" :src="qrcode" alt="QR Code" />
      </div>
    </ElCard>
  </ElSpace>
</template>
<script>
import { defineComponent, ref } from 'vue'
import { useQRCode } from '@vueuse/integrations/useQRCode'
export default defineComponent({
  setup() {
    const text = ref('Admin-Frame')
    const qrcode = useQRCode(text)
    return {
      text,
      qrcode
    }
  }
})
</script>

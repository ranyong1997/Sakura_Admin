<template>
  <ElButton
    type="primary"
    size="small"
    style="min-height: 32px; padding: 9px 15px"
  @click="dialogVisible = true"
    >点击打开可拖拽弹框</ElButton
  >
  <div v-dialogdrag>
    <ElDialog
      v-model="dialogVisible"
      title="提示"
      width="30%"
      :before-close="handleClose"
    >
      <div style="text-align: left">
        <span>
          Notice: before dialog gets opened for the first time this node and the
          one bellow will not be rendered
        </span>
        <div>
          <strong>Extra content (Not rendered)</strong>
        </div>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <ElButton @click="dialogVisible = false">取消</ElButton>
          <ElButton type="primary" @click="dialogVisible = false"
            >确认</ElButton
          >
        </span>
      </template>
    </ElDialog>
  </div>
</template>

<script>
import { defineComponent, ref } from 'vue'
import { ElMessageBox } from 'element-plus'

export default defineComponent({
  setup() {
    const dialogVisible = ref(false)

    const handleClose = (done) => {
      ElMessageBox.confirm('Are you sure to close this dialog?')
        .then(() => {
          done()
        })
        .catch(() => {
          // catch error
        })
    }
    return {
      dialogVisible,
      handleClose
    }
  }
})
</script>
<style lang="scss" scoped>

</style>

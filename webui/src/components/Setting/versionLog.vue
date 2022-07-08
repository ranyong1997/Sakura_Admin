<template>
  <ElDialog
    :before-close="close"
    :model-value="versionVisible"
    title="版本日志（Admin Frame 版权所有）"
    width="900px"
  >
    <ul class="v-log-content">
      <li v-for="(item, index) in versionInfo" :key="item.version">
        <div class="v-log-nav df-c">
          <div class="df-c">
            <ElTag v-if="!index" effect="dark" size="small">NEW</ElTag>
            <span
              class="v-n-title"
              :style="{
                paddingLeft: index ? '50px' : '4px'
              }"
              >{{ item.version }}</span
            >
          </div>
          <span class="v-n-date">{{ item.releaseDate }}</span>
        </div>
        <ul class="v-log-body">
          <li v-for="(it, idx) in item.description" :key="idx">
            {{ idx + 1 + '、' + it }}
          </li>
        </ul>
      </li>
    </ul>
    <template #footer>
      <span class="dialog-footer">
        <ElButton size="default" type="primary" plain @click="close"
          >返 回</ElButton
        >
      </span>
    </template>
  </ElDialog>
</template>
<script>
import { defineComponent, toRefs, reactive, ref, computed } from 'vue'
import { versionLog } from '../../assets/js/versionLog'
export default defineComponent({
  name: 'VersionLog',
  props: {
    versionVisible: Boolean
  },
  setup(props, context) {
    const state = reactive({
      versionInfo: computed(() => versionLog) //版本日志记录
    })

    const close = () => {
      //关闭
      context.emit('update:versionVisible', false)
    }

    return {
      ...toRefs(state),
      close
    }
  }
})
</script>
<style lang="scss" scoped>
.v-log-content {
  list-style: none;
  padding: 0 12px;
  height: 500px;
  overflow: auto;
  .v-log-nav {
    justify-content: space-between;
    .v-n-title {
      font-size: 20px;
    }
    .v-n-date {
      font-size: 18px;
    }
  }
  .v-log-body {
    list-style: none;
    padding: 12px 50px;
    text-align: left;
    li {
      font-size: 15px;
      padding-bottom: 6px;
    }
  }
}
</style>

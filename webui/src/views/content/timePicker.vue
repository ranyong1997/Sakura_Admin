<template>
  <ElSpace direction="vertical">
    <ElCard class="box-card" style="width: 60vw">
      <template #header>
        <div class="card-header">
          <span>基础时间选择</span>
        </div>
      </template>
      <div class="text item">
        <ElTimePicker v-model="value" placeholder="请选择"></ElTimePicker>
      </div>
    </ElCard>

    <ElCard class="box-card m-t8" style="width: 60vw">
      <template #header>
        <div class="card-header">
          <span>任意时间范围</span>
        </div>
      </template>
      <div class="text item">
        <ElTimePicker
          v-model="value1"
          is-range
          range-separator=" - "
          start-placeholder="开始时间"
          end-placeholder="结束时间"
        ></ElTimePicker>
      </div>
    </ElCard>

    <ElCard class="box-card m-t8" style="width: 60vw">
      <template #header>
        <div class="card-header">
          <span>时间计算</span>
        </div>
      </template>
      <div class="text item">
        <div class="m-t8">
          <span>选择时间：</span>
          <ElTimePicker
            v-model="value2"
            format="HH:mm"
            placeholder="请选择"
          ></ElTimePicker>
        </div>

        <div class="m-t8">
          <span>添加时间：</span>
          <ElTimePicker
            v-model="value3"
            format="HH:mm"
            placeholder="请选择"
          ></ElTimePicker>
        </div>

        <div class="m-t8">
          <span>结果时间：</span>
          <span style="font-size: 18px">{{ time ? time : '暂无数据' }}</span>
        </div>
      </div>
    </ElCard>
  </ElSpace>
</template>

<script>
import {
  defineComponent,
  reactive,
  toRefs,
  getCurrentInstance,
  watch
} from 'vue'
export default defineComponent({
  setup() {
    let { proxy } = getCurrentInstance() // vue原型
    const state = reactive({
      value: '',
      value1: [],
      value2: '',
      value3: '',
      time: ''
    })

    watch(
      () => [state.value2, state.value3],
      ([nValue2, nValue3], [oValue2, oValue3]) => {
        if (nValue2 && nValue3) {
          calculation()
        } else {
          state.time = ''
        }
      }
    )

    const calculation = () => {
      //时间计算
      if (!state.value2 || !state.value3) return false
      let curTime = new Date(state.value2) //初始
      let addTime = new Date(state.value3) //添加时间
      curTime.setMinutes(curTime.getMinutes() + addTime.getMinutes())
      curTime.setHours(addTime.getHours() + curTime.getHours())
      state.time = proxy.$moment(curTime).format('YYYY-MM-DD hh:mm')
    }
    return {
      ...toRefs(state)
    }
  }
})
</script>

<template>
  <ElForm :model="form" label-width="120px">
    <ElFormItem label="Activity name" inline>
      <ElInput v-model="form.name"></ElInput>
    </ElFormItem>
    <ElFormItem label="Activity zone">
      <ElSelect v-model="form.region" placeholder="please select your zone">
        <ElOption label="Zone one" value="shanghai"></ElOption>
        <ElOption label="Zone two" value="beijing"></ElOption>
      </ElSelect>
    </ElFormItem>
    <ElFormItem label="Activity time">
      <ElCol :span="11">
        <ElDatePicker
          v-model="form.date1"
          type="date"
          placeholder="Pick a date"
          style="width: 100%"
        ></ElDatePicker>
      </ElCol>
      <ElCol class="line" :span="2">-</ElCol>
      <ElCol :span="11">
        <ElTimePicker
          v-model="form.date2"
          placeholder="Pick a time"
          style="width: 100%"
        ></ElTimePicker>
      </ElCol>
    </ElFormItem>
    <ElFormItem label="Instant delivery">
      <ElSwitch v-model="form.delivery"></ElSwitch>
    </ElFormItem>
    <ElFormItem label="Activity type">
      <ElCheckboxGroup v-model="form.type">
        <ElCheckbox label="Online activities" name="type"></ElCheckbox>
        <ElCheckbox label="Promotion activities" name="type"></ElCheckbox>
        <ElCheckbox label="Offline activities" name="type"></ElCheckbox>
        <ElCheckbox label="Simple brand exposure" name="type"></ElCheckbox>
      </ElCheckboxGroup>
    </ElFormItem>
    <ElFormItem label="Resources">
      <ElRadioGroup v-model="form.resource">
        <ElRadio label="Sponsor"></ElRadio>
        <ElRadio label="Venue"></ElRadio>
      </ElRadioGroup>
    </ElFormItem>
    <ElFormItem label="Activity form">
      <ElInput v-model="form.desc" type="textarea"></ElInput>
    </ElFormItem>
    <ElFormItem>
      <ElButton type="primary">Create</ElButton>
      <ElButton>Cancel</ElButton>
    </ElFormItem>
  </ElForm>
</template>

<script>
import { defineComponent, reactive, ref, toRefs } from 'vue'
export default defineComponent({
  name: 'EasyForm',
  setup() {
    const state = reactive({
      form: {
        name: '',
        region: '',
        date1: '',
        date2: '',
        delivery: false,
        type: [],
        resource: '',
        desc: ''
      }
    })

    return {
      ...toRefs(state)
    }
  }
})
</script>

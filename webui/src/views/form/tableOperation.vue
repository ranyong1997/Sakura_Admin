<template>
  <div class="tableOperation">
    <div class="zan-nav">
      <ElForm
        :inline="true"
        :model="queryParams"
        class="demo-form-inline"
        label-position="right"
        label-width="84px"
      >
        <ElFormItem label="姓名：">
          <ElInput
            v-model.trim="queryParams.name"
            clearable
            placeholder="请输入姓名"
            size="large"
            @keyup.enter="getInfo(pagination)"
          ></ElInput>
        </ElFormItem>
        <ElFormItem label="ID：">
          <ElInput
            v-model.trim="queryParams.id"
            clearable
            placeholder="请输入ID"
            size="large"
            @keyup.enter="getInfo(pagination)"
          ></ElInput>
        </ElFormItem>
        <ElFormItem>
          <ElButton
            size="large"
            icon="search"
            type="primary"
            @click="getInfo(pagination)"
            >查 询</ElButton
          >
          <ElButton size="large" type="primary" @click="operation('add', {})"
            >新增</ElButton
          >
        </ElFormItem>
      </ElForm>
    </div>
    <div class="zan-table">
      <ElTable :data="list" height="calc(100vh - 320px)" style="width: 100%">
        <ElTableColumn prop="id" label="ID"></ElTableColumn>
        <ElTableColumn prop="name" label="姓名"></ElTableColumn>
        <ElTableColumn prop="address" label="地址"></ElTableColumn>
        <ElTableColumn align="center" label="操作">
          <template #default="scope">
            <ElSpace spacer="|" style="color: #dedede">
              <ElButton type="text" @click="operation('edit', scope.row)"
                >编辑</ElButton
              >
              <ElButton type="text" @click="toEnable(scope.row)">
                {{ scope.row.enabled === '0' ? '启用' : '禁用' }}
              </ElButton>
              <ElButton type="text" @click="del(scope.row.id)">删除</ElButton>
            </ElSpace>
          </template>
        </ElTableColumn>
      </ElTable>
      <Component
        :is="components.pagination"
        class="zan-pagination"
        @change="getInfo"
      ></Component>
    </div>
    <ElDialog
      v-model="openDialog"
      :title="logTitle"
      :before-close="close"
      width="1000px"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
      top="8vh"
    >
      <ElForm ref="tableRef" :model="form" :rules="rules" label-width="108px">
        <ElRow :gutter="20">
          <ElCol :span="12">
            <ElFormItem label="姓名：" prop="name">
              <ElInput
                v-model="form.name"
                placeholder="请输入姓名"
                clearable
              ></ElInput>
            </ElFormItem>
          </ElCol>
          <ElCol :span="12">
            <ElFormItem label="英文名：" prop="englishName">
              <ElInput
                v-model="form.englishName"
                placeholder="请输入英文名"
                clearable
              ></ElInput>
            </ElFormItem>
          </ElCol>
        </ElRow>

        <ElRow :gutter="20">
          <ElCol :span="12">
            <ElFormItem label="身高（cm）：" prop="height">
              <ElInput
                v-model="form.height"
                placeholder="请输入身高"
                clearable
              ></ElInput>
            </ElFormItem>
          </ElCol>
          <ElCol :span="12">
            <ElFormItem label="体重（kg）：" prop="weight">
              <ElInput
                v-model="form.weight"
                placeholder="请输入体重"
                clearable
              ></ElInput>
            </ElFormItem>
          </ElCol>
        </ElRow>
        <ElRow :gutter="20">
          <ElCol :span="24">
            <ElFormItem label="地址：" prop="address">
              <ElInput
                v-model="form.address"
                placeholder="请输入地址"
                clearable
              ></ElInput>
            </ElFormItem>
          </ElCol>
        </ElRow>
        <ElRow :gutter="20">
          <ElCol :span="24">
            <ElFormItem label="基本介绍：" prop="introduction">
              <ElInput
                v-model="form.introduction"
                type="textarea"
                :autosize="{ minRows: 2, maxRows: 5 }"
                placeholder="请输入基本介绍"
              ></ElInput>
            </ElFormItem>
          </ElCol>
        </ElRow>
        <ElRow :gutter="20">
          <ElCol :span="24">
            <ElFormItem label="备注：" prop="marks">
              <ElInput
                v-model="form.marks"
                type="textarea"
                :autosize="{ minRows: 3, maxRows: 5 }"
              ></ElInput>
            </ElFormItem>
          </ElCol>
        </ElRow>
      </ElForm>
      <template #footer>
        <span class="dialog-footer">
          <ElButton size="large" @click="close">取 消</ElButton>
          <ElButton size="large" type="primary" @click="ok">确 定</ElButton>
        </span>
      </template>
    </ElDialog>
  </div>
</template>
<script>
import {
  defineComponent,
  reactive,
  toRefs,
  onMounted,
  ref,
  provide,
  shallowRef
} from 'vue'
import { ElMessageBox } from 'element-plus'
import Pagination from '../../components/Pagination/index.vue'
export default defineComponent({
  name: 'TableOperation',
  components: {
    Pagination
  },
  setup() {
    const tableRef = ref(null)
    const state = reactive({
      type: 'add', //保存状态
      openDialog: false, //log开关
      logTitle: '新增', //log title
      list: [
        {
          id: '8008208828',
          name: '曹植饭',
          address: '南京市雨花台区宁双路19号云密城J栋6楼'
        },
        {
          id: '8008208828',
          name: '曹植饭',
          address: '南京市雨花台区宁双路19号云密城J栋6楼'
        },
        {
          id: '8008208828',
          name: '曹植饭',
          address: '南京市雨花台区宁双路19号云密城J栋6楼'
        },
        {
          id: '8008208828',
          name: '曹植饭',
          address: '南京市雨花台区宁双路19号云密城J栋6楼'
        },
        {
          id: '8008208828',
          name: '曹植饭',
          address: '南京市雨花台区宁双路19号云密城J栋6楼'
        }
      ],
      queryParams: {
        name: '',
        id: ''
      },
      form: {
        name: '',
        address: '',
        englishName: '',
        height: '',
        weight: '',
        introduction: '',
        marks: ''
      },
      pagination: {
        total: 1,
        page: 1
      },
      rules: {
        name: [{ required: true, message: '请输入姓名', trigger: 'blur' }]
      }
    })
    provide('pagination', state.pagination) //父子传参
    const components = shallowRef({
      //子组件注册
      pagination: Pagination
    })
    onMounted(() => {
      getInfo()
    })
    const getInfo = (val) => {
      //查询列表
    }
    const operation = (type, target) => {
      //打开新增 编辑
      state.type = type
      state.openDialog = true
      const titleWare = {
        add: '新增',
        edit: '编辑'
      }
      state.logTitle = titleWare[type]
      if (type == 'edit') {
        state.form = { ...target }
      }
    }
    const ok = () => {
      //判断新增 编辑
      const item = {
        add: save,
        edit: edit
      }
      tableRef.value.validate((vaild) => {
        if (vaild) {
          item[state.type]()
        }
      })
    }
    const save = () => {
      //新增
    }
    const edit = () => {
      //编辑
    }
    const del = (id) => {
      //删除
      ElMessageBox.confirm('此操作将永久删除本条记录, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(() => {})
        .catch(() => {})
    }
    const toEnable = (data) => {
      //启用 禁用
    }
    const close = () => {
      //关闭
      tableRef.value.resetFields()
      state.form = {
        name: '',
        address: '',
        englishName: '',
        height: '',
        weight: '',
        introduction: '',
        marks: ''
      }
      state.openDialog = false
    }
    return {
      ...toRefs(state),
      tableRef,
      components,
      close,
      getInfo,
      operation,
      toEnable,
      ok,
      del
    }
  }
})
</script>
<style lang="scss" scoped></style>

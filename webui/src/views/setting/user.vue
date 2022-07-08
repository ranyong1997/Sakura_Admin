<template>
  <div>
    <div class="zan-nav">
      <ElForm
        label-position="right"
        label-width="84px"
        :inline="true"
        :model="queryParams"
        class="demo-form-inline"
      >
        <ElFormItem label="用户姓名：">
          <ElInput
            v-model.trim="queryParams.staffName"
            size="large"
            clearable
            placeholder="请输入姓名"
            @keyup.enter="getInfo"
          ></ElInput>
        </ElFormItem>
        <ElFormItem label="用户ID：">
          <ElInput
            v-model.trim="queryParams.staffId"
            size="large"
            clearable
            placeholder="请输入ID"
            @keyup.enter="getInfo"
          ></ElInput>
        </ElFormItem>
        <ElFormItem>
          <ElButton icon="search" size="large" type="primary" @click="getInfo"
            >查 询</ElButton
          >
        </ElFormItem>
      </ElForm>
    </div>
    <div class="zan-table">
      <ElTable
        :data="userList"
        height="calc(100vh - 320px)"
        style="width: 100%"
      >
        <ElTableColumn prop="staffName" label="用户姓名"></ElTableColumn>
        <ElTableColumn prop="staffId" label="用户ID"></ElTableColumn>
        <ElTableColumn prop="username" label="用户名"></ElTableColumn>
        <ElTableColumn prop="sex" label="性别">
          <template #default="scope">
            {{ $filters.Gender(scope.row.sex) }}
          </template>
        </ElTableColumn>
        <ElTableColumn prop="phone" label="手机号码"></ElTableColumn>
        <ElTableColumn prop="address" label="用户住址"></ElTableColumn>
        <ElTableColumn prop="createTime" label="注册时间"></ElTableColumn>
        <ElTableColumn align="center" label="操作">
          <template #default="scope">
            <ElSpace spacer="|" style="color: #dedede">
              <ElButton type="text" @click="baseInfoEdit(scope.row)"
                >编辑</ElButton
              >
              <ElButton type="text" @click="deleteUser(scope.row)"
                >删除</ElButton
              >
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
    <BaseInfo ref="baseInfoRef" v-model:baseVisible="baseVisible"></BaseInfo>
  </div>
</template>
<script>
import {
  defineComponent,
  ref,
  reactive,
  toRefs,
  onMounted,
  shallowRef,
  provide
} from 'vue'
import { ElMessageBox } from 'element-plus'
import BaseInfo from '../../components/Setting/baseInfo.vue'
import Pagination from '../../components/Pagination/index.vue'

export default defineComponent({
  name: 'User',
  components: {
    Pagination,
    BaseInfo
  },
  setup() {
    const baseInfoRef = ref('null')
    const state = reactive({
      userList: [
        {
          staffName: '曹植饭',
          staffId: '8008208820',
          username: 'user',
          sex: 0,
          phone: '8008208820',
          address: '南京市雨花台区宁双路19号云密城J栋6楼',
          createTime: new Date()
        },
        {
          staffName: '曹植饭',
          staffId: '8008208820',
          username: 'user',
          sex: 0,
          phone: '8008208820',
          address: '南京市雨花台区宁双路19号云密城J栋6楼',
          createTime: new Date()
        },
        {
          staffName: '曹植饭',
          staffId: '8008208820',
          username: 'user',
          sex: 0,
          phone: '8008208820',
          address: '南京市雨花台区宁双路19号云密城J栋6楼',
          createTime: new Date()
        },
        {
          staffName: '曹植饭',
          staffId: '8008208820',
          username: 'user',
          sex: 0,
          phone: '8008208820',
          address: '南京市雨花台区宁双路19号云密城J栋6楼',
          createTime: new Date()
        },
        {
          staffName: '曹植饭',
          staffId: '8008208820',
          username: 'user',
          sex: 0,
          phone: '8008208820',
          address: '南京市雨花台区宁双路19号云密城J栋6楼',
          createTime: new Date()
        },
        {
          staffName: '曹植饭',
          staffId: '8008208820',
          username: 'user',
          sex: 0,
          phone: '8008208820',
          address: '南京市雨花台区宁双路19号云密城J栋6楼',
          createTime: new Date()
        }
      ], //存储用户信息
      baseVisible: false, //基本信息弹框
      queryParams: {
        staffName: '',
        staffId: ''
      },
      pagination: {
        total: 1,
        page: 1
      }
    })

    provide('pagination', state.pagination) //父子传参

    const components = shallowRef({
      //子组件注册
      pagination: Pagination
    })

    const getInfo = (val) => {
      //查询
    }

    const reFresh = (val) => {
      //刷新
      if (val) getInfo()
    }

    const baseInfoEdit = (row) => {
      //打开编辑信息弹框
      baseInfoRef.value.openBaseInfo(row)
    }

    const deleteUser = (row) => {
      //删除用户
      ElMessageBox.confirm('此操作将注销该用户, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(() => {})
        .catch(() => {})
    }

    onMounted(() => {
      getInfo()
    })

    return {
      ...toRefs(state),
      components,
      baseInfoRef,
      getInfo,
      deleteUser,
      baseInfoEdit
    }
  }
})
</script>

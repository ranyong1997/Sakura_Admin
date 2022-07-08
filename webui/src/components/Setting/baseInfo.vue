<template>
  <ElDrawer
    :before-close="close"
    :model-value="baseVisible"
    title="基本信息"
    size="800px"
    @open="getInit"
  >
    <ElForm
      ref="baseInfoRef"
      :model="baseInfo"
      :rules="baseInfoRules"
      label-width="114px"
    >
      <ElRow>
        <ElCol :span="10">
          <ElFormItem label="姓名：">
            <ElInput v-model="baseInfo.staffName"></ElInput>
          </ElFormItem>
        </ElCol>
        <ElCol :span="10">
          <ElFormItem label="用户名：" prop="username">
            <ElInput v-model="baseInfo.username"></ElInput>
          </ElFormItem>
        </ElCol>
      </ElRow>
      <ElRow>
        <ElCol :span="10">
          <ElFormItem label="性别：">
            <ElSelect v-model="baseInfo.sex" placeholder="请选择性别">
              <ElOption label="女" value="0"></ElOption>
              <ElOption label="男" value="1"></ElOption>
            </ElSelect>
          </ElFormItem>
        </ElCol>
        <ElCol :span="10">
          <ElFormItem label="手机号码：">
            <ElInput v-model="baseInfo.phone"></ElInput>
          </ElFormItem>
        </ElCol>
      </ElRow>
      <ElRow>
        <ElCol :span="10">
          <ElFormItem label="出生日期：">
            <ElDatePicker
              v-model="baseInfo.birthDate"
              placeholder="选择日期"
              type="date"
            ></ElDatePicker>
          </ElFormItem>
        </ElCol>
      </ElRow>
      <ElRow>
        <ElCol :span="10">
          <ElFormItem label="账号状态：">
            <ElSelect v-model="baseInfo.userState" placeholder="请选择">
              <ElOption label="正常" value="0"></ElOption>
              <ElOption label="冻结" value="1"></ElOption>
            </ElSelect>
          </ElFormItem>
        </ElCol>
        <ElCol :span="10">
          <ElFormItem label="权限分配：" prop="jurisdiction">
            <ElSelect
              v-model="baseInfo.jurisdiction"
              multiple
              placeholder="请选择"
            >
              <ElOption
                v-for="item in roleList"
                :key="item.roleId"
                :label="item.marks"
                :value="item.roleId"
              ></ElOption>
            </ElSelect>
          </ElFormItem>
        </ElCol>
      </ElRow>
      <ElRow>
        <ElCol :span="20">
          <ElFormItem label="家庭住址：">
            <ElInput v-model="baseInfo.address"></ElInput>
          </ElFormItem>
        </ElCol>
      </ElRow>
      <ElRow>
        <ElCol :span="20">
          <ElFormItem label="个人说明：">
            <ElInput
              v-model="baseInfo.marks"
              :autosize="{ minRows: 4, maxRows: 6 }"
              type="textarea"
            ></ElInput>
          </ElFormItem>
        </ElCol>
      </ElRow>
      <ElRow>
        <ElCol :span="20">
          <div class="baseInfo_footer">
            <ElFormItem>
              <ElButton size="default" @click="close">取消</ElButton>
              <ElButton size="default" type="primary" @click="saveBaseInfo"
                >确定</ElButton
              >
            </ElFormItem>
          </div>
        </ElCol>
      </ElRow>
    </ElForm>
  </ElDrawer>
</template>

<script>
import { defineComponent, reactive, ref, toRefs } from 'vue'
import { useStore } from 'vuex'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import myFun from '../../utils/myFun.js'

export default defineComponent({
  name: 'BaseInfo',
  props: {
    baseVisible: Boolean
  },
  emits: ['reFresh'],
  setup(props, context) {
    const store = useStore() //vuex
    const router = useRouter() //路由
    const baseInfoRef = ref(null) //基本信息ref
    const state = reactive({
      baseInfo: {
        username: '',
        sex: '',
        staffName: '',
        phone: '',
        marks: '',
        birthDate: '',
        address: '',
        userState: '',
        jurisdiction: '',
        image: ''
      },
      baseInfoRules: {
        username: [
          { required: true, message: '请输入用户名', trigger: 'blur' }
        ],
        jurisdiction: [
          { required: true, message: '请至少选择一个角色', trigger: 'change' }
        ]
      },
      roleList: [
        {
          marks: '普通用户',
          roleId: '1'
        },
        {
          marks: '系统管理员',
          roleId: '2'
        },
        {
          marks: '超级管理员',
          roleId: '3'
        }
      ] //角色列表
    })

    const getInit = () => {
      //基本信息初始化
      console.log('基本信息初始化')
    }
    const close = () => {
      context.emit('update:baseVisible', false)
    }

    const openBaseInfo = (row) => {
      context.emit('update:baseVisible', true)
      state.baseInfo = Object.assign({ ...row }, {})
    }

    const saveBaseInfo = () => {
      //保存用户信息
      ElMessage.warning({
        message: '检测到您修改了本账号的信息，3秒后回到登陆页',
        type: 'warning'
      })
      setTimeout(() => {
        router.push({ path: '/login' })
        context.emit('reFresh', false)
        myFun.delAccessToken() //清空token 回到登录页
      }, 3000)
      close()
    }

    return {
      ...toRefs(state),
      close,
      saveBaseInfo,
      openBaseInfo,
      baseInfoRef,
      getInit
    }
  }
})
</script>
<style lang="scss" scoped>
.baseInfo_footer {
  text-align: right;
}
</style>

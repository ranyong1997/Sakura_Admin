<template>
  <div class="role">
    <div class="zan-nav">
      <ElForm
        :inline="true"
        :model="queryParams"
        class="demo-form-inline"
        label-position="right"
        label-width="84px"
      >
        <ElFormItem label="角色名：">
          <ElInput
            v-model.trim="queryParams.roleName"
            clearable
            placeholder="请输入角色名"
            size="large"
            @keyup.enter="getInfo"
          ></ElInput>
        </ElFormItem>
        <ElFormItem label="角色ID：">
          <ElInput
            v-model.trim="queryParams.roleId"
            clearable
            placeholder="请输入角色ID"
            size="large"
            @keyup.enter="getInfo"
          ></ElInput>
        </ElFormItem>
        <ElFormItem>
          <ElButton icon="search" size="large" type="primary" @click="getInfo"
            >查 询</ElButton
          >
          <ElButton type="primary" size="large" @click="openLog({}, 'add')"
            >新增角色</ElButton
          >
        </ElFormItem>
      </ElForm>
    </div>
    <div class="zan-table">
      <ElTable
        :data="roleList"
        height="calc(100vh - 320px)"
        stripe
        style="width: 100%"
      >
        <ElTableColumn label="角色名称" prop="roleName"></ElTableColumn>
        <ElTableColumn label="备注" prop="marks"></ElTableColumn>
        <ElTableColumn label="是否默认" prop="grant">
          <template #default="scope">
            <ElTag v-if="scope.row.grant === '1'" effect="dark" type="success"
              >是</ElTag
            >
            <ElTag v-else effect="dark" type="danger">否</ElTag>
          </template>
        </ElTableColumn>
        <ElTableColumn label="创建时间" prop="createTime"></ElTableColumn>
        <ElTableColumn label="操作">
          <template #default="scope">
            <ElSpace spacer="|" style="color: #dedede">
              <ElButton type="text" @click="openAuthorize(scope.row)"
                >授权</ElButton
              >
              <ElButton type="text" @click="openLog(scope.row, 'edit')"
                >编辑</ElButton
              >
              <ElButton type="text" @click="del(scope.row)">删除</ElButton>
            </ElSpace>
          </template>
        </ElTableColumn>
      </ElTable>
    </div>
    <ElDialog
      v-model="visible"
      :before-close="close"
      title="角色配置"
      width="865px"
    >
      <ElForm
        ref="roleRef"
        :model="roleForm"
        :rules="roleRules"
        class="demo-ruleForm"
        label-width="94px"
      >
        <ElRow>
          <ElCol :span="11">
            <ElFormItem label="角色名称：" prop="roleName">
              <ElInput v-model.trim="roleForm.roleName"></ElInput>
            </ElFormItem>
          </ElCol>
        </ElRow>
        <ElRow>
          <ElCol>
            <ElFormItem label="是否默认：" prop="grant">
              <ElSwitch
                v-model="roleForm.grant"
                active-text="是"
                active-value="1"
                inactive-text="否"
                inactive-value="0"
              ></ElSwitch>
            </ElFormItem>
          </ElCol>
        </ElRow>
        <ElRow>
          <ElCol :span="24">
            <ElFormItem label="说明：" prop="marks">
              <ElInput
                v-model="roleForm.marks"
                :autosize="{ minRows: 3, maxRows: 5 }"
                type="textarea"
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
    <ElDialog
      v-model="distribution"
      :before-close="closeAuthorize"
      title="权限分配"
      width="600px"
    >
      <div class="distribution_content">
        <ElTree
          ref="treeRef"
          :data="resourceList"
          :props="defaultProps"
          check-on-click-node
          default-expand-all
          node-key="resourceId"
          show-checkbox
        ></ElTree>
      </div>
      <template #footer>
        <span class="dialog-footer">
          <ElButton size="large" @click="closeAuthorize">取 消</ElButton>
          <ElButton size="large" type="primary" @click="saveResource"
            >确 定</ElButton
          >
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
  shallowRef,
  provide,
  ref,
  computed
} from 'vue'
import { ElMessageBox } from 'element-plus'
import { useStore } from 'vuex'
import resourceList from '../../assets/js/resource'

export default defineComponent({
  name: 'Role',
  setup() {
    const roleRef = ref(null) //角色ref
    const treeRef = ref(null) //资源树的ref
    const store = useStore()
    const state = reactive({
      roleList: [
        {
          roleName: 'user',
          marks: '普通用户',
          grant: '1',
          createTime: new Date()
        },
        {
          roleName: 'admin',
          marks: '系统管理员',
          grant: '0',
          createTime: new Date()
        },
        {
          roleName: 'super_admin',
          marks: '超级管理员',
          grant: '0',
          createTime: new Date()
        }
      ],
      visible: false,
      distribution: false,
      type: '',
      queryParams: {
        roleName: '',
        roleId: ''
      },
      roleForm: {
        roleName: '',
        grant: '0',
        marks: '',
        roleId: ''
      },
      roleWare: null, //暂存
      roleRules: {
        roleName: [
          { required: true, message: '请输入角色名称', trigger: 'blur' }
        ]
      },
      resourceList,
      defaultProps: {
        //tree 默认配置项
        children: 'children',
        label: 'name'
      }
    })
    onMounted(() => {
      getInfo()
      getAllResource()
    })

    const getInfo = () => {
      //查询列表
    }



    const openLog = (data, type) => {
      //保存 修改
      if (type) state.type = type
      if (type === 'add') {
      } else if (type === 'edit') {
        state.roleForm.roleId = data.roleId
        state.roleForm.roleName = data.roleName
        state.roleForm.grant = data.grant
        state.roleForm.marks = data.marks
      }
      state.visible = true
    }

    const close = () => {
      //关闭
      roleRef.value.resetFields()
      state.roleForm = {
        roleName: '',
        grant: '0',
        marks: '',
        roleId: ''
      }
      state.visible = false
    }

    const save = () => {
      roleRef.value.validate((vaild) => {
        if (vaild) {
          close()
          getInfo()
        }
      })
    }

    const edit = () => {
      roleRef.value.validate((vaild) => {
        if (vaild) {
          close()
          getInfo()
        }
      })
    }

    const ok = () => {
      //保存 or 修改
      const item = {
        add: save,
        edit: edit
      }
      item[state.type]()
    }

    const del = (data) => {
      //删除
      ElMessageBox.confirm('此操作将永久删除该角色, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(() => {
          getInfo()
        })
        .catch(() => {})
    }

    const openAuthorize = (data) => {
      //打开权限分配
      // transitionI18n();
      state.distribution = true
      state.roleWare = data //存储选中信息
    }

    const closeAuthorize = () => {
      //关闭权限分配
      //关闭权限分配
      state.distribution = false
      state.roleWare = null
    }

    const getAllResource = () => {
      //请求所有资源
    }

    const saveResource = () => {
      //授权
      closeAuthorize()
    }

    return {
      ...toRefs(state),
      roleRef,
      treeRef,
      getInfo,
      openLog,
      ok,
      del,
      openAuthorize,
      closeAuthorize,
      saveResource,
      close
    }
  }
})
</script>
<style lang="scss" scoped>
.distribution_content {
  height: 400px;
  overflow: auto;
}
</style>

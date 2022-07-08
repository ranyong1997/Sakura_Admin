<template>
  <div class="resource">
    <div class="zan-nav">
      <ElForm
        ref="baseInfoRef"
        :inline="true"
        :model="queryParams"
        class="demo-form-inline"
        label-position="right"
        label-width="84px"
      >
        <ElFormItem label="资源名称：">
          <ElInput
            v-model.trim="queryParams.resourceName"
            clearable
            placeholder="请输入资源名称"
            size="large"
            @keyup.enter="getInfo"
          ></ElInput>
        </ElFormItem>
        <ElFormItem>
          <ElButton icon="search" size="large" type="primary" @click="getInfo"
            >查 询</ElButton
          >
          <ElButton type="primary" size="large" @click="openLog({}, 'add')"
            >新增资源</ElButton
          >
        </ElFormItem>
      </ElForm>
    </div>
    <div class="zan-table">
      <ElRow :gutter="20">
        <ElCol :span="14">
          <ElTree
            :data="resourceList"
            :expand-on-click-node="false"
            :props="defaultProps"
            default-expand-all
            node-key="resourceId"
          >
            <template #default="{ node, data }">
              <span class="custom-tree-node">
                <span>{{ node.label }}</span>
                <span>
                  <ElSpace spacer="|" style="color: #dedede">
                    <ElButton
                      title="添加子资源"
                      type="text"
                      @click="openLog(data, 'add')"
                      >添加</ElButton
                    >
                    <ElButton
                      title="编辑"
                      type="text"
                      @click="openLog(data, 'edit')"
                      >编辑</ElButton
                    >
                    <ElButton title="删除" type="text" @click="del(data)"
                      >删除</ElButton
                    >
                  </ElSpace>
                </span>
              </span>
            </template>
          </ElTree>
        </ElCol>
      </ElRow>
    </div>
    <ElDialog
      v-model="visible"
      :before-close="close"
      title="资源配置"
      width="865px"
    >
      <ElForm
        ref="resourceRef"
        :model="resourceForm"
        :rules="resourceRules"
        class="demo-ruleForm"
        label-width="74px"
      >
        <ElRow>
          <ElCol :span="12">
            <ElFormItem label="名称：" prop="resourceName">
              <ElInput v-model.trim="resourceForm.resourceName"></ElInput>
            </ElFormItem>
          </ElCol>
          <ElCol :span="12">
            <ElFormItem label="路径：" prop="resourceUrl">
              <ElInput v-model.trim="resourceForm.resourceUrl"></ElInput>
            </ElFormItem>
          </ElCol>
        </ElRow>
        <ElRow>
          <ElCol :span="12">
            <ElFormItem label="图标：" prop="resourceIcon">
              <ElInput v-model="resourceForm.resourceIcon"></ElInput>
            </ElFormItem>
          </ElCol>
          <ElCol :span="12">
            <ElFormItem label="权重：" prop="resourceOrder">
              <ElInputNumber
                v-model="resourceForm.resourceOrder"
                :max="999"
                :min="1"
              ></ElInputNumber>
            </ElFormItem>
          </ElCol>
        </ElRow>
        <ElRow>
          <ElCol :span="12">
            <ElFormItem label="类型：" prop="resourceType">
              <ElSelect
                v-model="resourceForm.resourceType"
                placeholder="请选择资源类型"
              >
                <ElOption label="菜单" value="1"></ElOption>
                <ElOption label="url" value="2"></ElOption>
              </ElSelect>
            </ElFormItem>
          </ElCol>
        </ElRow>
        <ElRow>
          <ElCol :span="24">
            <ElFormItem label="说明：" prop="marks">
              <ElInput
                v-model="resourceForm.marks"
                :rows="2"
                placeholder="请输入说明"
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
  </div>
</template>
<script>
import {
  defineComponent,
  reactive,
  toRefs,
  onMounted,
  ref,
  computed
} from 'vue'
import { ElMessageBox } from 'element-plus'
import { useStore } from 'vuex'
import resourceList from '../../assets/js/resource'

export default defineComponent({
  name: 'Resource',
  setup() {
    const resourceRef = ref(null) //资源ref
    const store = useStore()
    const state = reactive({
      resourceList,
      visible: false,
      defaultProps: {
        //tree 默认配置项
        children: 'children',
        label: 'resourceName'
      },
      queryParams: {
        resourceName: ''
      },
      resourceForm: {
        resourceName: '',
        resourceUrl: '',
        resourceType: '',
        resourceIcon: '',
        resourceOrder: '',
        marks: '',
        resourceId: ''
      },
      resourceRules: {
        resourceName: [
          { required: true, message: '请输入资源名称', trigger: 'blur' }
        ],
        resourceUrl: [
          { required: true, message: '请输入资源路径', trigger: 'blur' }
        ],
        resourceOrder: [
          { required: true, message: '请输入权重', trigger: 'blur' }
        ]
      },
      type: ''
    })

    onMounted(() => {
      getInfo()

    })



    const getInfo = () => {
      //查询列表
    }

    const ok = () => {
      const item = {
        add: save,
        edit: edit
      }
      item[state.type]()
    }

    const save = () => {
      //保存
      resourceRef.value.validate((vaild) => {
        if (vaild) {
          close()
          getInfo()
        }
      })
    }

    const edit = () => {
      //编辑
      resourceRef.value.validate((vaild) => {
        if (vaild) {
          close()
          getInfo()
        }
      })
    }

    const del = (data) => {
      //删除
      ElMessageBox.confirm('此操作将永久删除该资源, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      })
        .then(() => {
          getInfo()
        })
        .catch(() => {})
    }

    const close = () => {
      //关闭
      resourceRef.value.resetFields()
      state.resourceForm = {
        resourceName: '',
        resourceUrl: '',
        resourceType: '',
        resourceIcon: '',
        resourceOrder: '',
        marks: '',
        resourceId: ''
      }
      state.visible = false
    }

    const openLog = (data, type) => {
      //保存 修改
      if (type) state.type = type
      if (type === 'add') {
        state.resourceForm.parentId = data.resourceId ? data.resourceId : 0
      } else if (type === 'edit') {
        state.resourceForm.resourceName = data.resourceName
        state.resourceForm.resourceUrl = data.resourceUrl
        state.resourceForm.resourceType = data.resourceType
        state.resourceForm.resourceIcon = data.resourceIcon
        state.resourceForm.resourceOrder = data.resourceOrder
        state.resourceForm.marks = data.marks
        state.resourceForm.resourceId = data.resourceId
      }
      state.visible = true
      // state.resourceForm = Object.assign({...data},{});
    }

    return {
      ...toRefs(state),
      save,
      edit,
      del,
      ok,
      close,
      openLog,
      getInfo,
      resourceRef
    }
  }
})
</script>
<style lang="scss" scoped>
.resource {
  .custom-tree-node {
    flex: 1;
    display: flex;
    align-items: center;
    justify-content: space-between;
    font-size: 14px;
    padding-right: 8px;
  }
}
</style>

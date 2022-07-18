<!--
 * @Descripttion: 
 * @version: 
 * @Author: 冉勇
 * @Date: 2022-07-18 08:54:59
 * @LastEditTime: 2022-07-18 16:58:56
-->
<template>
    <div class="common-layout">
        <el-container>
            <!-- 左边tree -->
            <el-aside>
                <el-row class="left-page">
                    <el-col :span="14">
                        <el-input v-model="filterText" placeholder="输入要查找的目录" :prefix-icon="Search" />
                    </el-col>
                    <el-col :span="5">
                        <el-button type="primary" :icon="Plus" />
                    </el-col>
                    <el-tree ref="treeRef" class="filter-tree" :data="data" :props="defaultProps" default-expand-all
                        :filter-node-method="filterNode" :icon="Plus" />
                </el-row>
            </el-aside>
            <!-- 右边内容 -->
            <el-main>
                <el-row>
                    <el-col :span="6">
                        <el-form ref="ruleFormRef" :model="ruleForm" :rules="rules" label-width="120px"
                            class="case-ruleForm" :size="formSize" status-icon>
                            <el-form-item label="用例名称:" prop="casename">
                                <el-input v-model="ruleForm.casename" placeholder="请输入用例名称" clearable />
                            </el-form-item>
                        </el-form>
                    </el-col>
                    <el-col :span="6">
                        <el-form>
                            <el-form-item label="创建人:">
                                <el-select v-model="value" class="m-2" placeholder="请选择创建用户" clearable>
                                    <el-option v-for="item in options" :key="item.value" :label="item.label"
                                        :value="item.value" />
                                </el-select>
                            </el-form-item>
                        </el-form>
                    </el-col>
                    <el-col :span="2">
                        <el-button type="primary" :icon="Search" @click="search(ruleFormRef)">查询</el-button>
                    </el-col>
                    <el-button type="info" :icon="Refresh" @click="reset(ruleFormRef)">重置</el-button>
                </el-row>
                <el-row>
                    <el-button type="primary" :icon="Plus">添加用例</el-button>
                </el-row>
                <div class="add-table">
                    <ElTable height="calc(100vh - 320px)" style="width: 100%">
                        <ElTableColumn prop="name" label="名称"></ElTableColumn>
                        <ElTableColumn prop="request-protocol" label="请求协议"></ElTableColumn>
                        <ElTableColumn prop="priority" label="优先级"></ElTableColumn>
                        <ElTableColumn prop="state" label="状态"></ElTableColumn>
                        <ElTableColumn prop="updatetime" label="更新时间"></ElTableColumn>
                        <ElTableColumn align="operation" label="操作">
                            <template #default="scope">
                                <ElSpace spacer="|" style="color: #dedede">
                                    <ElButton type="text">详情</ElButton>
                                    <ElButton type="text">
                                        {{ scope.row.enabled === '0' ? '启用' : '禁用' }}
                                    </ElButton>
                                    <ElButton type="text">执行</ElButton>
                                </ElSpace>
                            </template>
                        </ElTableColumn>
                    </ElTable>
                    <el-pagination v-model:currentPage="currentPage2" v-model:page-size="pageSize2"
                        :page-sizes="[5, 10, 50, 100]" :small="small" :disabled="disabled" :background="background"
                        layout="sizes, prev, pager, next" :total="1000" @size-change="handleSizeChange"
                        @current-change="handleCurrentChange" />
                </div>
            </el-main>
        </el-container>
    </div>
</template>
<script lang="ts" setup>
import { ref, watch, reactive } from 'vue'
import { ElTree, ElLoading, FormInstance, FormRules } from 'element-plus'
import { Search, Plus, Refresh } from '@element-plus/icons-vue'
const formSize = ref('default')
const ruleFormRef = ref<FormInstance>()
const ruleForm = reactive({
    casename: '',
})
const rules = reactive<FormRules>({
    casename: [
        { required: true, message: '请输入用例名称', trigger: 'blur' },
    ],
})
// 查询逻辑
const search = async (formEl: FormInstance | undefined) => {
    if (!formEl) return
    await formEl.validate((valid, fields) => {
        if (valid) {
            const loading = ElLoading.service({
                lock: true,
                text: 'Loading',
                background: 'rgba(0, 0, 0, 0.7)',
            })
            setTimeout(() => {
                loading.close()
            }, 500)
        }
    })

}
// 重置逻辑
const reset = (formEl: FormInstance | undefined) => {
    if (!formEl) return
    formEl.resetFields()
    const loading = ElLoading.service({
        lock: true,
        text: 'Loading',
        background: 'rgba(0, 0, 0, 0.7)',
    })
    setTimeout(() => {
        loading.close()
    }, 500)
}
interface Tree {
    id: number
    label: string
    children?: Tree[]
}

const value = ref('')
const currentPage2 = ref(5)
const pageSize2 = ref(100)
const small = ref(false)
const background = ref(false)
const handleSizeChange = (val: number) => {
    console.log(`${val} items per page`)
}
const handleCurrentChange = (val: number) => {
    console.log(`current page: ${val}`)
}
// 下拉选项框
const options = [
    {
        value: '测试员A',
        label: '测试员A',
    },
    {
        value: '测试员B',
        label: '测试员B',
    },
    {
        value: '测试员C',
        label: '测试员C',
    },
    {
        value: '测试员D',
        label: '测试员D',
    },
    {
        value: '测试员E',
        label: '测试员E',
    },
]
const filterText = ref('')
const treeRef = ref<InstanceType<typeof ElTree>>()

const defaultProps = {
    children: 'children',
    label: 'label',
}

watch(filterText, (val) => {
    treeRef.value!.filter(val)
})

const filterNode = (value: string, data: Tree) => {
    if (!value) return true
    return data.label.includes(value)
}
// 左侧树结构
const data: Tree[] = [
    {
        id: 1,
        label: '北京项目',
        children: [
            {
                id: 4,
                label: '接口自动化',
                children: [
                    {
                        id: 9,
                        label: '接口A',
                    },
                    {
                        id: 10,
                        label: '接口B',
                    },
                ],
            },
        ],
    },
    {
        id: 2,
        label: '重庆项目',
        children: [
            {
                id: 5,
                label: 'UI自动化A',
            },
            {
                id: 6,
                label: 'UI自动化A',
            },
        ],
    },
    {
        id: 3,
        label: '广东项目',
        children: [
            {
                id: 7,
                label: '性能测试A',
            },
            {
                id: 8,
                label: '性能测试B',
            },
        ],
    },
]
</script>

<style lang="scss" scoped>
</style>

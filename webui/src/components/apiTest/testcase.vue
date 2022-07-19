<!--
 * @Descripttion: 
 * @version: 
 * @Author: 冉勇
 * @Date: 2022-07-18 08:54:59
 * @LastEditTime: 2022-07-19 15:43:19
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
                        <el-form ref="ruleFormRef" :model="ruleForm" :rules="rules" label-width="120px" :size="formSize"
                            status-icon>
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
                    <el-dropdown>
                        <el-dropdown>
                            <el-button type="primary" :icon="Plus">添加用例
                                <el-icon>
                                    <arrow-down />
                                </el-icon>
                            </el-button>
                            <template #dropdown>
                                <el-dropdown-menu>
                                    <el-dropdown-item :icon="Plus" @click="commoncase = true">普通用例
                                    </el-dropdown-item>
                                    <el-dropdown-item :icon="Plus" @click="recordcase = true">录制用例
                                    </el-dropdown-item>
                                </el-dropdown-menu>
                            </template>
                        </el-dropdown>
                    </el-dropdown>
                    <!-- 抽屉 -->
                    <el-drawer v-model="commoncase" title="添加用例" direction="rtl" size="64%">
                        <el-row>
                            <el-col :span="12">
                                <span class="title">用例信息</span>
                                <div class="flex-button">
                                    <el-button type="primary" :icon="Document">提交</el-button>
                                    <el-button type="primary" :icon="Cpu">测试</el-button>
                                </div>
                            </el-col>
                        </el-row>
                        <div class="line"></div>
                        <el-button type="danger" @click="commoncase = false" class="close-button">
                            <el-icon class="el-icon--left">
                                <CircleCloseFilled />
                            </el-icon>
                        </el-button>
                        <!-- 表单 -->
                        <el-form ref="ruleFormRef" :model="ruleForm" status-icon :rules="rules" label-width="120px">
                            <el-row :gutter="20">
                                <el-col :span="8">
                                    <el-form-item label="用例名称：" prop="casename" :size="formSize" clearable>
                                        <el-input v-model="ruleForm.casename" placeholder="请输入用例名称" autocomplete="off"
                                            clearable />
                                    </el-form-item>
                                </el-col>
                                <el-col :span="8">
                                    <el-form-item label="优先级：" prop="priority">
                                        <el-select v-model="value" placeholder="请选择用例优先级" clearable>
                                            <el-option v-for="item in priority" :key="item.value" :label="item.label"
                                                :value="item.value" />
                                        </el-select>
                                    </el-form-item>
                                </el-col>
                                <el-col :span="8">
                                    <el-form-item label="用例状态：" prop="state">
                                        <el-select v-model="value" placeholder="请选择用例当前状态" clearable>
                                            <el-option v-for="item in state" :key="item.value" :label="item.label"
                                                :value="item.value" />
                                        </el-select>
                                    </el-form-item>
                                </el-col>
                            </el-row>
                            <el-row :gutter="20">
                                <el-col :span="8">
                                    <el-form-item label="请求类型：" prop="method">
                                        <el-select v-model="value" placeholder="请选择请求类型" clearable>
                                            <el-option v-for="item in method" :key="item.value" :label="item.label"
                                                :value="item.value" />
                                        </el-select>
                                    </el-form-item>
                                </el-col>
                                <el-col :span="8">
                                    <el-form-item label="用例标签：">
                                        <el-tag v-for="tag in dynamicTags" :key="tag" class="mx-1" closable
                                            :disable-transitions="false" @close="handleClose(tag)">
                                            {{ tag }}
                                        </el-tag>
                                        <el-input v-if="inputVisible" ref="InputRef" v-model="inputValue"
                                            class="ml-1 w-20" size="small" @keyup.enter="handleInputConfirm"
                                            @blur="handleInputConfirm" />
                                        <el-button v-else class="button-new-tag ml-1" size="small" @click="showInput">
                                            + 添加新标签页
                                        </el-button>
                                    </el-form-item>
                                </el-col>
                                <el-col :span="8">
                                    <el-form-item label="用例类型：" prop="casetype">
                                        <el-select v-model="value" placeholder="请选择用例类型" clearable>
                                            <el-option v-for="item in casetype" :key="item.value" :label="item.label"
                                                :value="item.value" />
                                        </el-select>
                                    </el-form-item>
                                </el-col>
                            </el-row>
                            <!-- <el-form-item>
                                <el-button type="primary" @click="submitForm(ruleFormRef)">Submit</el-button>
                                <el-button @click="resetForm(ruleFormRef)">Reset</el-button>
                            </el-form-item> -->
                        </el-form>
                    </el-drawer>
                    <!-- 分割线 -->
                    <el-drawer v-model="recordcase" class="title-top" title="录制用例" direction="rtl" size="64%">
                        <el-table :data="gridData">
                            <el-table-column property="date" label="Date" width="150" />
                            <el-table-column property="name" label="Name" width="200" />
                            <el-table-column property="address" label="Address" />
                        </el-table>
                    </el-drawer>
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
                                </ElSpace>New Added use case functionality
                            </template>
                        </ElTableColumn>
                    </ElTable>
                    <el-pagination v-model:currentPage="currentPage2" v-model:page-size="pageSize2"
                        :page-sizes="[5, 10, 50, 100]" :small="small" :background="background"
                        layout="sizes, prev, pager, next" :total="1000" @size-change="handleSizeChange"
                        @current-change="handleCurrentChange" />
                </div>
            </el-main>
        </el-container>
    </div>
</template>

<script lang="ts" setup>
import { ref, watch, reactive, nextTick } from 'vue'
import { ElTree, ElLoading, FormInstance, FormRules, ElButton, ElDrawer, ElInput } from 'element-plus'
import { Search, Plus, Refresh, ArrowDown, CircleCloseFilled, Document, Cpu } from '@element-plus/icons-vue'
const formSize = ref('default')
const ruleFormRef = ref<FormInstance>()
// 表单规则初始化
const ruleForm = reactive({
    casename: '',

})
// 临时
const inputValue = ref('')
const dynamicTags = ref([])
const inputVisible = ref(false)
const InputRef = ref<InstanceType<typeof ElInput>>()

const handleClose = (tag: string) => {
    dynamicTags.value.splice(dynamicTags.value.indexOf(tag), 1)
}

const showInput = () => {
    inputVisible.value = true
    nextTick(() => {
        InputRef.value!.input!.focus()
    })
}
const handleInputConfirm = () => {
    if (inputValue.value) {
        dynamicTags.value.push(inputValue.value)
    }
    inputVisible.value = false
    inputValue.value = ''
}
const checkAge = (rule: any, value: any, callback: any) => {
    if (!value) {
        return callback(new Error('请输入用例名称'))
    }
}
const validatePass = (rule: any, value: any, callback: any) => {
    if (value === '') {
        callback(new Error('请输入用例名称'))
    } else {
        if (ruleForm.checkPass !== '') {
            if (!ruleFormRef.value) return
            ruleFormRef.value.validateField('checkPass', () => null)
        }
        callback()
    }
}
const validatePass2 = (rule: any, value: any, callback: any) => {
    if (value === '') {
        callback(new Error('请输入用例状态'))
    }
}
const submitForm = (formEl: FormInstance | undefined) => {
    if (!formEl) return
    formEl.validate((valid) => {
        if (valid) {
            console.log('submit!')
        } else {
            console.log('error submit!')
            return false
        }
    })
}
const resetForm = (formEl: FormInstance | undefined) => {
    if (!formEl) return
    formEl.resetFields()
}
// 表单验证规则
const rules = reactive<FormRules>({
    casename: [
        { required: true, message: '请输入用例名称', trigger: 'blur' },
    ],
    priority: [
        { required: true, message: '请选择用例优先级', trigger: 'blur' },
    ],
    state: [
        { required: true, message: '请选择用例状态', trigger: 'blur' },
    ],
    method: [
        { required: true, message: '请选择请求类型', trigger: 'blur' },
    ],
    casetype: [
        { required: true, message: '请选择用例类型', trigger: 'blur' },
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
// 抽屉开关
const commoncase = ref(false)
const recordcase = ref(false)
const filterText = ref('')
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
// 用例类型
const casetype = [
    {
        value: '普通用例',
        label: '普通用例',
    },
    {
        value: '前置用例',
        label: '前置用例',
    },
    {
        value: '数据工厂',
        label: '数据工厂',
    },
]
// 请求类型下拉框
const method = [
    {
        value: 'HTTP',
        label: 'HTTP',
    },
]
// 用例状态下拉框
const state = [
    {
        value: '调试中',
        label: '调试中',
    },
    {
        value: '已停用',
        label: '已停用',
    },
    {
        value: '正常',
        label: '正常',
    },
]
// 优先级下拉框
const priority = [
    {
        value: 'P0',
        label: 'P0',
    },
    {
        value: 'P1',
        label: 'P1',
    },
    {
        value: 'P2',
        label: 'P2',
    },
    {
        value: 'P3',
        label: 'P3',
    },
    {
        value: 'P4',
        label: 'P4',
    },
]
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
// 抽屉数据
const gridData = [
    {
        date: '2016-05-02',
        name: 'Peter Parker',
        address: 'Queens, New York City',
    },
    {
        date: '2016-05-04',
        name: 'Peter Parker',
        address: 'Queens, New York City',
    },
    {
        date: '2016-05-01',
        name: 'Peter Parker',
        address: 'Queens, New York City',
    },
    {
        date: '2016-05-03',
        name: 'Peter Parker',
        address: 'Queens, New York City',
    },
]
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
.title {
    color: #253f48;
    font-size: larger;
    float: left;
    margin-top: 5px;
    margin-bottom: 5px;
    font-weight: bold
}

.close-button {
    position: absolute;
    right: 0;
    top: 0;
    padding: 0 10px;
    background: #e74c3c;
    border-radius: 0 0 0 10px;
    cursor: pointer;
}

.flex-button {
    position: absolute;
    right: 0;
}

.line {
    display: flex;
    content: '';
    flex: 1;
    height: 1px;
    background: #b2bec3;
    margin-top: 10px;
    margin-bottom: 10px
}
</style>

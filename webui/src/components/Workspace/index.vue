<template>
    <el-row>
        <el-col :span="24">
            <el-card>
                <div class="select-style">
                    <el-select v-model="value" placeholder="请选择">
                        <el-option v-for="item in items" :key="item.value" :label="item.label" :value="item.value" />
                    </el-select>
                    <el-button type="primary" :icon="Search">查询</el-button>
                    <el-button :icon="Plus" @click="operation('add', {})">创建任务</el-button>
                </div>
                <el-dialog v-model="openDialog" :title="logTitle" :before-close="close" width="1000px"
                    :close-on-click-modal="false" :close-on-press-escape="false" top="8vh">
                    <el-form ref="tableRef" :model="form" :rules="rules" label-width="108px">
                        <el-row :gutter="20">
                            <el-col :span="24">
                                <el-formItem label="任务名称:" prop="taskname">
                                    <el-input v-model="form.name" placeholder="" clearable></el-input>
                                </el-formItem>
                            </el-col>
                        </el-row>
                        <el-row :gutter="20">
                            <el-col :span="24">
                                <el-formItem label="任务描述:" prop="task_description">
                                    <el-input v-model="form.marks" type="textarea"
                                        :autosize="{ minRows: 5, maxRows: 5 }"></el-input>
                                </el-formItem>
                            </el-col>
                        </el-row>
                        <el-row :gutter="20">
                            <el-col :span="12">
                                <el-formItem label="执行人员:" prop="executer">
                                    <el-select v-model="value" clearable placeholder="-请选择-">
                                        <el-option v-for="item in execute" :key="item.value" :label="item.label"
                                            :value="item.value" />
                                    </el-select>
                                </el-formItem>
                            </el-col>
                            <el-col :span="12">
                                <el-formItem label="负责人:" prop="principaler">
                                    <el-select v-model="value" clearable placeholder="-请选择-">
                                        <el-option v-for="item in principal" :key="item.value" :label="item.label"
                                            :value="item.value" />
                                    </el-select>
                                </el-formItem>
                            </el-col>
                        </el-row>
                        <el-row :gutter="20">
                            <el-col :span="12">
                                <el-formItem label="关注者:" prop="follower">
                                    <el-select v-model="value" clearable placeholder="-请选择-">
                                        <el-option v-for="item in follower" :key="item.value" :label="item.label"
                                            :value="item.value" />
                                    </el-select>
                                </el-formItem>
                            </el-col>
                        </el-row>
                        <el-row :gutter="20">
                            <el-col :span="24">
                                <el-formItem label="所属项目" prop="items">
                                    <el-select v-model="value" clearable placeholder="-请选择-">
                                        <el-option v-for="item in items" :key="item.value" :label="item.label"
                                            :value="item.value" />
                                    </el-select>
                                    <el-button :icon="Plus" @click="operation('add', {})">新增项目</el-button>
                                </el-formItem>
                            </el-col>
                        </el-row>
                        <el-row :gutter="20">
                            <el-col :span="12">
                                <el-formItem label="紧急程度:" prop="urgency">
                                    <el-select v-model="value" clearable placeholder="-请选择-">
                                        <el-option v-for="item in urgency" :key="item.value" :label="item.label"
                                            :value="item.value" />
                                    </el-select>
                                </el-formItem>
                            </el-col>
                            <el-col :span="12">
                                <el-formItem label="难易程度:" prop="easy">
                                    <el-select v-model="value" clearable placeholder="-请选择-">
                                        <el-option v-for="item in easy" :key="item.value" :label="item.label"
                                            :value="item.value" />
                                    </el-select>
                                </el-formItem>
                            </el-col>
                        </el-row>
                        <el-row :gutter="20">
                            <el-col :span="12">
                                <el-formItem label="任务类别:" prop="tasktype">
                                    <el-select v-model="value" clearable placeholder="-请选择-">
                                        <el-option v-for="item in tasktype" :key="item.value" :label="item.label"
                                            :value="item.value" />
                                    </el-select>
                                </el-formItem>
                            </el-col>
                            <el-col :span="12">
                                <el-formItem label="工作量(H):" prop="workload">
                                    <el-input v-model="form.name" placeholder="请填写非负整数" clearable></el-input>
                                </el-formItem>
                            </el-col>
                        </el-row>
                        <el-row :gutter="20">
                            <el-col :span="12">
                                <el-formItem label="开始日期:" prop="startdata">
                                    <el-col :span="11">
                                        <el-date-picker v-model="form.startdata" type="date" placeholder="-请选择-"
                                            style="width: 100%"></el-date-picker>
                                    </el-col>
                                </el-formItem>
                            </el-col>
                            <el-col :span="12">
                                <el-formItem label="结束日期:" prop="overdata">
                                    <el-col :span="11">
                                        <el-date-picker v-model="form.overdata" type="date" placeholder="-请选择-"
                                            style="width: 100%"></el-date-picker>
                                    </el-col>
                                </el-formItem>
                            </el-col>
                        </el-row>
                    </el-form>
                    <template #footer>
                        <span class="dialog-footer">
                            <el-button size="large" @click="close">取 消</el-button>
                            <el-button size="large" type="primary" @click="ok">确 定</el-button>
                        </span>
                    </template>
                </el-dialog>
            </el-card>
        </el-col>
    </el-row>
    <el-row>
        <el-col :span="6">
            <div class="grid-content ep-bg-purple" />
            <el-card class="box-card car-col1">
                <div class="title">{{ '未开始(203)' }}
                    <div class="icon1">
                        <el-icon>
                            <Clock />
                        </el-icon>
                    </div>
                </div>
                <el-divider />
                <div class="text item">{{ '新建测试包' }}</div>
            </el-card>
        </el-col>
        <el-col :span="6">
            <div class="grid-content ep-bg-purple" />
            <el-card class="box-card car-col2">
                <div class="title">{{ '进行中(64)' }}
                    <div class="icon2">
                        <el-icon>
                            <Aim />
                        </el-icon>
                    </div>
                </div>
                <el-divider />
                <div class="text item">{{ '新建测试包' }}</div>
            </el-card>
        </el-col>
        <el-col :span="6">
            <div class="grid-content ep-bg-purple" />
            <el-card class="box-card car-col3">
                <div class="title">{{ '完成(24)' }}
                    <div class="icon3">
                        <el-icon>
                            <Checked />
                        </el-icon>
                    </div>
                </div>
                <el-divider />
                <div class="text item">{{ '新建测试包' }}</div>
            </el-card>
        </el-col>
        <el-col :span="6">
            <div class="grid-content ep-bg-purple" />
            <el-card class="box-card car-col4">
                <div class="title">{{ '终止(2) | 暂停(3)' }}
                    <div class="icon4">
                        <el-icon>
                            <Cellphone />
                        </el-icon>
                    </div>
                </div>
                <el-divider />
                <div class="text item">{{ '新建测试包' }}</div>
            </el-card>
        </el-col>
    </el-row>
</template>
<script>
import {
    defineComponent,
    reactive,
    toRefs,
    ref,
    provide,
    shallowRef
} from 'vue'
import Pagination from 'components/Pagination/index.vue'
import { Plus, Search } from '@element-plus/icons-vue'
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
            form: {
                name: '',
                task_description: '',
                executer: '',
                principaler: '',
                startdata: '',
                overdata: '',
                introduction: '',
                marks: ''
            },
            execute: [
                {
                    value: '测试人员A',
                    label: '测试人员A',

                },
                {
                    value: '测试人员B',
                    label: '测试人员B',
                }
            ],
            principal: [{
                value: '测试人A',
                label: '测试人A',
            },
            {
                value: '测试人B',
                label: '测试人B',
            }],
            follower: [{
                value: '关注者A',
                label: '关注者A',
            },
            {
                value: '关注者B',
                label: '关注者B',
            }],
            items: [{
                value: '项目A',
                label: '项目A',
            },
            {
                value: '项目B',
                label: '项目B',
            }],
            urgency: [{
                value: '加急',
                label: '加急',
            },
            {
                value: '一般',
                label: '一般',
            }, {
                value: '低',
                label: '低',
            }, {
                value: '不用管',
                label: '不用管',
            }],
            easy: [{
                value: '很难',
                label: '很难',
            },
            {
                value: '难',
                label: '难',
            }, {
                value: '一般',
                label: '一般',
            }, {
                value: '简单',
                label: '简单',
            }, {
                value: '很简单',
                label: '很简单',
            }],
            tasktype: [{
                value: '运维',
                label: '运维',
            },
            {
                value: '研发',
                label: '研发',
            }, {
                value: '测试',
                label: '测试',
            }, {
                value: '实施',
                label: '实施',
            }, {
                value: '产品',
                label: '产品',
            }, {
                value: 'UI',
                label: 'UI',
            }, {
                value: '交互设计',
                label: '交互设计',
            }, {
                value: '需求',
                label: '需求',
            }],
            rules: {
                taskname: [{ required: true, message: '请输入任务名称', trigger: 'blur' }],
                task_description: [{ required: true, message: '请输入任务描述', trigger: 'blur' }],
                executer: [{ required: true, message: '请选择执行人', trigger: 'blur' }],
                principaler: [{ required: true, message: '请选择负责人', trigger: 'blur' }],
            },
            shortcuts: [],
        })
        const components = shallowRef({
            //子组件注册
        })
        const operation = (type, target) => {
            //打开新增 编辑
            state.type = type
            state.openDialog = true
            const titleWare = {
                add: '创建任务',
            }
            state.logTitle = titleWare[type]
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
        const close = () => {
            //关闭
            tableRef.value.resetFields()
            state.form = {
                taskname: '',
                follower: '',
                height: '',
                executer: '',
                items: '',
                urgency: '',
                introduction: '',
                task_description: '',
                easy: '',
                tasktype: '',
                workload: '',
                startdata: '',
                overdata: '',
            }
            state.openDialog = false
        }
        return {
            ...toRefs(state),
            tableRef,
            components,
            close,
            operation,
            ok,
        }
    }
})
</script>
<style scoped>
.icon4 {
    font-size: 25px;
    color: #9b59b6;
    padding-top: 5px;
}

.icon3 {
    font-size: 25px;
    color: #3498db;
    padding-top: 5px;
}

.icon2 {
    font-size: 25px;
    color: #f1c40f;
    padding-top: 5px;
}

.icon1 {
    font-size: 25px;
    color: #1abc9c;
    padding-top: 5px;
}

.title {
    font-size: 25px;
}

.text {
    font-size: 18px;
}

.item {
    padding: 5px;
}

.box-card {
    width: 399px;
    border-radius: 10px;

}

.car-col1 {
    border-top: 6px solid #1abc9c;
}

.car-col2 {
    border-top: 6px solid #f1c40f;
}

.car-col3 {
    border-top: 6px solid #3498db;

}

.car-col4 {
    border-top: 6px solid #9b59b6;
}


.el-row {
    margin-bottom: 20px;
}

.el-row:last-child {
    margin-bottom: 0;
}

.el-col {
    border-radius: 4px;
}

.grid-content {
    border-radius: 4px;
    min-height: 36px;
}

.select-style {
    padding: 10px;
}
</style>
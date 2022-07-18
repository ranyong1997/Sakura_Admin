<!--
 * @Descripttion: 
 * @version: 
 * @Author: 冉勇
 * @Date: 2022-07-18 08:54:59
 * @LastEditTime: 2022-07-18 15:15:00
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


            </el-main>
        </el-container>
    </div>
</template>
<script lang="ts" setup>
import { ref, watch } from 'vue'
import { ElTree } from 'element-plus'
import { Search, Plus } from '@element-plus/icons-vue'
interface Tree {
    id: number
    label: string
    children?: Tree[]
}

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

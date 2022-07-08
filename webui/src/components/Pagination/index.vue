<template>
  <ElPagination
    :current-page="pagination.currentPage"
    :page-sizes="[10]"
    :page-size="pagination.pageSize"
    layout="total, sizes, prev, pager, next, jumper"
    :total="pagination.total"
    @current-change="currentChange"
  ></ElPagination>
</template>
<script>
import { defineComponent, reactive, toRefs, watch, inject } from 'vue'
export default defineComponent({
  setup(props, context) {
    const pagination = inject('pagination') //接受

    const currentChange = (val) => {
      //切换分页
      context.emit('change', {
        pageSize: 10,
        page: val
      })
    }

    return {
      pagination,
      currentChange
    }
  }
})
</script>

<template>
  <div>
    <ElResult icon="warning" title="提交异常">
      <template #extra>
        <div class="bg-defult p-defult min-w600">
          <div class="t-l">异常原因分析：</div>
          <div class="t-l m-t8">
            您的账号最近3日内交易过于频繁，请尽快
            <span style="color: #409eff; cursor: pointer">联系管理员</span>
            处理异常
          </div>
        </div>
        <div class="m-t8">
          <ElButton type="primary" size="default">返回</ElButton>
          <ElButton type="primary" size="default">联系管理员</ElButton>
        </div>
      </template>
    </ElResult>
  </div>
</template>

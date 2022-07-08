<template>
  <div>
    <ElResult icon="error" title="提交失败">
      <template #extra>
        <div class="bg-defult p-defult min-w600">
          <div class="t-l">失败原因分析：</div>
          <div class="t-l m-t8">
            账号余额不足，
            <span style="color: #409eff; cursor: pointer">请充值</span>。
          </div>
        </div>
        <div class="m-t8">
          <ElButton type="primary" size="default">返回</ElButton>
          <ElButton type="primary" size="default">重新再试</ElButton>
        </div>
      </template>
    </ElResult>
  </div>
</template>

// import { i18n } from '../../locales/i18n'; //国际化
// const { global: { t, tm, locale } } = i18n;
export default [
    //资源信息
    {
        resourceName: '测试总览',
        resourceUrl: "/homePage",
        resourceIcon: 'fa fa-tachometer',
        children: []
    },
    {
        resourceName: '工作空间',
        resourceUrl: "/work",
        resourceIcon: 'fa fa-wrench',
        children: []
    },
    {
        resourceName: "工作空间copy",
        resourceUrl: "/gongneng",
        resourceIcon: 'fa fa-wrench',
        children: [
            {
                resourceName: "可拖拽弹框",
                resourceUrl: "/dialogDrag",
                children: []
            },
            {
                resourceName: "添加水印",
                resourceUrl: "/wartermark",
                children: []
            },
            {
                resourceName: "pinia",
                resourceUrl: "/shop",
                children: []
            },
            {
                resourceName: "时间选择器",
                resourceUrl: "/timePicker",
                children: []
            },
            {
                resourceName: "复制",
                resourceUrl: "/copy",
                children: []
            },
            {
                resourceName: "生成二维码",
                resourceUrl: "/qrcode",
                children: []
            },
            {
                resourceName: "监测电脑信息",
                resourceUrl: "/computerMonitor",
                children: []
            },
        ]
    },
    {
        resourceName: "测试准备",
        resourceUrl: "/content",
        resourceIcon: "fa fa-file-text",
        children: [
            {
                resourceName: "基础表单",
                resourceUrl: "/easyForm",
                children: []
            },
            {
                resourceName: "表格操作",
                resourceUrl: "/tableOperation",
                children: []
            },
            {
                resourceName: "卡片列表",
                resourceUrl: "/cardList",
                children: []
            },
        ]
    },
    {
        resourceName: "测试分工",
        resourceUrl: "/editor",
        resourceIcon: "fa fa-bold",
        children: [
            {
                resourceName: "富文本编辑器",
                resourceUrl: "/textEditor",
                children: []
            },
        ]
    },
    {
        resourceName: "测试环境",
        resourceUrl: "/result",
        resourceIcon: "fa fa-random",
        children: [
            {
                resourceName: "成功",
                resourceUrl: "/successTip",
                children: []
            }, {
                resourceName: "异常",
                resourceUrl: "/warningTip",
                children: []
            },
            {
                resourceName: "异常",
                resourceUrl: "/errorTip",
                children: []
            },
        ]
    },
    {
        resourceName: "测试执行",
        resourceUrl: "/error",
        resourceIcon: "fa fa-exclamation-triangle",
        children: [{
            resourceName: "404",
            resourceUrl: "/404",
            children: []
        },
        {
            resourceName: "403",
            resourceUrl: "/403",
            children: []
        },
        {
            resourceName: "暂无数据",
            resourceUrl: "/noData",
            children: []
        },
        {
            resourceName: "功能建设中",
            resourceUrl: "/build",
            children: []
        },
        {
            resourceName: "网络不可用",
            resourceUrl: "/networkError",
            children: []
        },
        ]
    },
    {
        resourceName: "缺陷跟踪",
        resourceUrl: "/workflow",
        resourceIcon: 'fa fa-crosshairs',
        children: []
    },
    {
        resourceName: "综合事务",
        resourceUrl: "/messageManagement",
        resourceIcon: "fa fa-comment",
        children: [
            {
                resourceName: "消息中心",
                resourceUrl: "/messageCenter",
                children: []
            }
        ]
    },
    {
        resourceName: "测试分析",
        resourceUrl: "/setting",
        resourceIcon: "fa fa-cog",
        children: [
            {
                resourceName: "用户管理",
                resourceUrl: "/user",
                children: []
            },
            {
                resourceName: "角色管理",
                resourceUrl: "/role",
                children: []
            },
            {
                resourceName: "资源管理",
                resourceUrl: "/resource",
                children: []
            },
        ]
    },
    {
        resourceName: "项目总结",
        resourceUrl: "/noviceGuide",
        resourceIcon: 'fa fa-question-circle-o',
        children: []
    },
]
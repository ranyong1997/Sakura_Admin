/*
 * @Descripttion: 
 * @version: 
 * @Author: 冉勇
 * @Date: 2022-07-09 08:33:10
 * @LastEditTime: 2022-07-09 10:21:38
 */
//配置引导设置
const steps = [
    {
        element: '.noviceGuide',
        popover: {
            title: "Hello",
            description: "欢迎来到【波塞冬】的新手引导",
            position: "bottom"
        }
    },
    {
        element: '.zan-sidebar-nav',
        popover: {
            title: "介绍",
            description: "波塞冬 是一款敏捷测试后台管理系统",
            position: "bottom"
        }
    },
    {
        element: '.fa-arrows-alt',
        popover: {
            title: "全屏",
            description: "打开全屏模式",
            position: "left"
        }
    },
    {
        element: '.fa-bell-o',
        popover: {
            title: "消息中心",
            description: "点击查看消息中心",
            position: "left"
        }
    },
    {
        element: '.fabtn',
        popover: {
            title: "菜单开关",
            description: "控制菜单的显示/隐藏",
            position: "right"
        }
    },
    {
        element: '.el-menu',
        popover: {
            title: "快来试试吧~",
            description: "菜单中包含测试总览、工作空间、测试准备、测试分工、测试环境、测试执行、缺陷跟踪、综合事务、测试分析、项目总结等... 详情请点击菜单查看",
            position: "right"
        }
    },
];

export default steps
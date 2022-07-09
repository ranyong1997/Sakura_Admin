<template>
  <div class="homePage">
    <ElRow :gutter="10">
      <ElCol v-for="(item, index) in dataList" :key="index" :xs="24" :sm="24" :md="6" :lg="6" :xl="6">
        <ElCard class="box-card m-t8" shadow="always" :body-style="{ padding: '35px 20px' }">
          <template #header>
            <div class="card-header">
              <span class="card-header-title">{{ item.title }}</span>
              <ElTag :type="item.type" effect="dark" size="small">{{
                  item.labelTitle
              }}</ElTag>
            </div>
          </template>
          <div class="text item card-h-total">{{ item.total }}</div>
        </ElCard>
      </ElCol>
    </ElRow>
    <ElRow :gutter="10">
      <ElCol :xs="24" :sm="24" :md="24" :lg="24" :xl="24">
        <ElCard class="box-card m-t8" shadow="always" :body-style="{ padding: '0' }">
          <template #header>
            <div class="card-header">
              <span class="card-header-title">各时间段流量监控</span>
            </div>
          </template>
          <div class="text item">
            <div id="visitChart" class="home_charts"></div>
          </div>
        </ElCard>
      </ElCol>
    </ElRow>
    <ElRow :gutter="10">
      <ElCol :xs="24" :sm="24" :md="8" :lg="8" :xl="8">
        <ElCard class="box-card m-t8" shadow="always">
          <template #header>
            <div class="card-header">
              <span class="card-header-title">数据来源</span>
            </div>
          </template>
          <div class="text item">
            <div id="originChart" class="home_charts"></div>
          </div>
        </ElCard>
      </ElCol>
      <ElCol :xs="24" :sm="24" :md="8" :lg="8" :xl="8">
        <ElCard class="box-card m-t8" shadow="always">
          <template #header>
            <div class="card-header">
              <span class="card-header-title">周活跃量统计</span>
            </div>
          </template>
          <div class="text item">
            <div id="activeChart" class="home_charts"></div>
          </div>
        </ElCard>
      </ElCol>
      <ElCol :xs="24" :sm="24" :md="8" :lg="8" :xl="8">
        <ElCard class="box-card m-t8" shadow="always">
          <template #header>
            <div class="card-header">
              <span class="card-header-title">用户数据统计</span>
            </div>
          </template>
          <div class="text item">
            <div id="genderChart" class="home_charts"></div>
          </div>
        </ElCard>
      </ElCol>
    </ElRow>
  </div>
</template>
<script>
import {
  onMounted,
  defineComponent,
  reactive,
  toRefs,
  onUnmounted
} from 'vue'
// 引入 echarts 核心模块，核心模块提供了 echarts 使用必须要的接口。
import * as echarts from 'echarts/core';
// 引入柱状图图表，图表后缀都为 Chart
import { BarChart } from 'echarts/charts';
import {
  TitleComponent,
  TooltipComponent,
  GridComponent,
  DatasetComponent,
  TransformComponent,
  LegendComponent
} from 'echarts/components';
// 标签自动布局，全局过渡动画等特性
import { LabelLayout, UniversalTransition } from 'echarts/features';
// 引入 Canvas 渲染器，注意引入 CanvasRenderer 或者 SVGRenderer 是必须的一步
import { CanvasRenderer } from 'echarts/renderers';
import { PieChart, LineChart } from 'echarts/charts';

// 注册必须的组件
echarts.use([
  TitleComponent,
  TooltipComponent,
  GridComponent,
  DatasetComponent,
  TransformComponent,
  BarChart,
  LabelLayout,
  UniversalTransition,
  CanvasRenderer,
  LegendComponent,
  PieChart,
  LineChart,
]);
export default defineComponent({
  name: 'HomePage',
  setup() {
    const state = reactive({
      dataList: [
        {
          title: '接口总数',
          total: '334',
          labelTitle: '总数',
          type: 'danger'
        },
        {
          title: '通过接口数/未通过接口数',
          total: '51/74',
          labelTitle: '总数',
          type: ''
        },
        {
          title: '未测试接口数',
          total: '209',
          labelTitle: '总数',
          type: 'success'
        },
        {
          title: '接口未完成用例包(执行率)',
          total: '24%(113/362)',
          labelTitle: '百分比',
          type: 'warning'
        }
      ]
    })

    onMounted(() => {
      window.onresize = function () {
        //页面尺寸变化 自适应大小
        chartsInit();
      };
      chartsInit();
    })
    onUnmounted(() => { })
    const chartsInit = () => {
      //图标初始化
      loadVisitChart()
      loadOriginChart()
      loadActiveChart()
      loadGenderChart()
    }
    const loadVisitChart = () => {
      //加载访问图表
      let labelware = []
      let dataware = []
      for (let index = 1; index <= 24; index++) {
        labelware.push(`${index}:00`)
        if (index % 2 === 0) {
          dataware.push(index * 200)
        } else {
          dataware.push(index * 26)
        }
      }
      let myChart = echarts.init(document.getElementById('visitChart'))
      let option = {
        xAxis: {
          type: 'category',
          data: labelware
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            data: dataware,
            type: 'line'
          }
        ]
      }
      document.getElementById('visitChart').setAttribute('_echarts_instance_', '')
      myChart.setOption(option)
    }

    const loadOriginChart = () => {
      //加载访问图表
      let myChart = echarts.init(document.getElementById('originChart'))
      let option = {
        tooltip: {
          trigger: 'item'
        },
        legend: {
          top: '5%',
          left: 'center'
        },
        series: [
          {
            name: '访问来源',
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            itemStyle: {
              borderRadius: 10,
              borderColor: '#fff',
              borderWidth: 2
            },
            label: {
              show: false,
              position: 'center'
            },
            emphasis: {
              label: {
                show: true,
                fontSize: '40',
                fontWeight: 'bold'
              }
            },
            labelLine: {
              show: false
            },
            data: [
              { value: 1048, name: '搜索引擎' },
              { value: 735, name: '直接访问' },
              { value: 580, name: '邮件营销' },
              { value: 484, name: '联盟广告' },
              { value: 300, name: '视频广告' }
            ]
          }
        ]
      }
      document.getElementById('originChart').setAttribute('_echarts_instance_', '')
      myChart.setOption(option)
    }

    const loadActiveChart = () => {
      //每周访问量
      let myChart = echarts.init(document.getElementById('activeChart'))
      // 绘制图表
      let option = {
        xAxis: {
          type: 'category',
          data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            data: [300, 200, 150, 80, 70, 110, 130],
            type: 'bar',
            showBackground: true,
            backgroundStyle: {
              color: 'rgba(180, 180, 180, 0.2)'
            }
          }
        ]
      }
      document.getElementById('activeChart').setAttribute('_echarts_instance_', '')
      myChart.setOption(option)
    }


    const loadGenderChart = () => {
      //用户性别统计
      let myChart = echarts.init(document.getElementById('genderChart'))
      // 绘制图表
      let option = {
        xAxis: {
          type: 'category',
          data: ['男生', '女生', '未知']
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            data: [
              {
                value: 12234,
                itemStyle: {
                  color: '#409EFF'
                }
              },
              {
                value: 64132,
                itemStyle: {
                  color: '#7B76D6'
                }
              },
              {
                value: 8755,
                itemStyle: {
                  color: '#C0C4CC'
                }
              }
            ],
            type: 'bar'
          }
        ]
      }
      document.getElementById('genderChart').setAttribute('_echarts_instance_', '')
      myChart.setOption(option)
    }



    return {
      ...toRefs(state)
    }
  }
})
</script>
<style lang="scss" scoped>
.homePage {
  .home_charts {
    height: 380px;
  }

  .card-header {
    display: flex;
    justify-content: space-between;

    .card-header-title {
      font-size: 15px;
    }
  }

  .card-h-total {
    font-size: 28px;
  }
}
</style>

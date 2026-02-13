<template>
  <div class="admin-dashboard">
    <el-container>
      <el-aside width="220px" class="sidebar">
        <div class="logo">
          <el-icon size="28" color="white"><School /></el-icon>
          <span>管理后台</span>
        </div>
        <el-menu
          :default-active="$route.path"
          router
          background-color="#1f2937"
          text-color="#9ca3af"
          active-text-color="white"
        >
          <el-menu-item index="/admin">
            <el-icon><DataLine /></el-icon>
            <span>数据概览</span>
          </el-menu-item>
          <el-menu-item index="/admin/universities">
            <el-icon><School /></el-icon>
            <span>院校管理</span>
          </el-menu-item>
          <el-menu-item index="/admin/majors">
            <el-icon><Reading /></el-icon>
            <span>专业管理</span>
          </el-menu-item>
          <el-menu-item index="/admin/guides">
            <el-icon><Document /></el-icon>
            <span>攻略管理</span>
          </el-menu-item>
          <el-menu-item index="/admin/cases">
            <el-icon><FolderOpened /></el-icon>
            <span>案例管理</span>
          </el-menu-item>
          <el-menu-item index="/admin/users">
            <el-icon><User /></el-icon>
            <span>用户管理</span>
          </el-menu-item>
          <el-divider />
          <el-menu-item index="/">
            <el-icon><HomeFilled /></el-icon>
            <span>返回前台</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      
      <el-container>
        <el-header class="header">
          <div class="header-right">
            <el-dropdown @command="handleCommand">
              <span class="user-info">
                <el-avatar :size="32" :icon="UserFilled" />
                <span>{{ userStore.userInfo?.nickname || '管理员' }}</span>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="logout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </div>
        </el-header>
        
        <el-main>
          <h2>数据概览</h2>
          
          <el-row :gutter="20" class="stats-row">
            <el-col :span="6">
              <el-card class="stat-card">
                <div class="stat-icon" style="background: #dbeafe;">
                  <el-icon size="32" color="#1e40af"><School /></el-icon>
                </div>
                <div class="stat-info">
                  <h3>{{ stats.university_count || 0 }}</h3>
                  <p>院校数量</p>
                </div>
              </el-card>
            </el-col>
            <el-col :span="6">
              <el-card class="stat-card">
                <div class="stat-icon" style="background: #d1fae5;">
                  <el-icon size="32" color="#065f46"><Reading /></el-icon>
                </div>
                <div class="stat-info">
                  <h3>{{ stats.major_count || 0 }}</h3>
                  <p>专业数量</p>
                </div>
              </el-card>
            </el-col>
            <el-col :span="6">
              <el-card class="stat-card">
                <div class="stat-icon" style="background: #fef3c7;">
                  <el-icon size="32" color="#92400e"><User /></el-icon>
                </div>
                <div class="stat-info">
                  <h3>{{ stats.user_count || 0 }}</h3>
                  <p>注册用户</p>
                </div>
              </el-card>
            </el-col>
            <el-col :span="6">
              <el-card class="stat-card">
                <div class="stat-icon" style="background: #fce7f3;">
                  <el-icon size="32" color="#9d174d"><Document /></el-icon>
                </div>
                <div class="stat-info">
                  <h3>{{ stats.guide_count || 0 }}</h3>
                  <p>攻略文章</p>
                </div>
              </el-card>
            </el-col>
          </el-row>
          
          <el-row :gutter="20" class="chart-row">
            <el-col :span="12">
              <el-card>
                <template #header>
                  <span>院校国家分布</span>
                </template>
                <div ref="countryChart" class="chart-container"></div>
              </el-card>
            </el-col>
            <el-col :span="12">
              <el-card>
                <template #header>
                  <span>专业分类统计</span>
                </template>
                <div ref="categoryChart" class="chart-container"></div>
              </el-card>
            </el-col>
          </el-row>
          
          <el-row :gutter="20" class="chart-row">
            <el-col :span="24">
              <el-card>
                <template #header>
                  <span>用户增长趋势</span>
                </template>
                <div ref="userGrowthChart" class="chart-container"></div>
              </el-card>
            </el-col>
          </el-row>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'
import { getStatistics } from '@/utils/api'
import * as echarts from 'echarts'
import { 
  School, Reading, User, Document, DataLine, 
  HomeFilled, UserFilled, FolderOpened 
} from '@element-plus/icons-vue'

const router = useRouter()
const userStore = useUserStore()
const stats = ref({})

const countryChart = ref(null)
const categoryChart = ref(null)
const userGrowthChart = ref(null)

const handleCommand = (command) => {
  if (command === 'logout') {
    userStore.logout()
    ElMessage.success('已退出登录')
    router.push('/login')
  }
}

const initCharts = () => {
  nextTick(() => {
    // 院校国家分布图
    if (countryChart.value && stats.value.country_distribution) {
      const chart1 = echarts.init(countryChart.value)
      const countryData = stats.value.country_distribution.map(item => ({
        name: item.country,
        value: item.count
      }))
      chart1.setOption({
        tooltip: { trigger: 'item' },
        legend: { orient: 'vertical', right: 10, top: 'center' },
        series: [{
          type: 'pie',
          radius: ['40%', '70%'],
          avoidLabelOverlap: false,
          itemStyle: { borderRadius: 10, borderColor: '#fff', borderWidth: 2 },
          label: { show: false },
          data: countryData
        }]
      })
    }
    
    // 专业分类统计图
    if (categoryChart.value && stats.value.category_distribution) {
      const chart2 = echarts.init(categoryChart.value)
      const categoryData = stats.value.category_distribution.map(item => ({
        name: item.category,
        value: item.count
      }))
      chart2.setOption({
        tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
        xAxis: { type: 'category', data: categoryData.map(d => d.name), axisLabel: { rotate: 30 } },
        yAxis: { type: 'value' },
        series: [{
          data: categoryData.map(d => d.value),
          type: 'bar',
          itemStyle: {
            color: {
              type: 'linear',
              x: 0, y: 0, x2: 0, y2: 1,
              colorStops: [
                { offset: 0, color: '#1e40af' },
                { offset: 1, color: '#3b82f6' }
              ]
            },
            borderRadius: [8, 8, 0, 0]
          }
        }]
      })
    }
    
    // 用户增长趋势图
    if (userGrowthChart.value) {
      const chart3 = echarts.init(userGrowthChart.value)
      chart3.setOption({
        tooltip: { trigger: 'axis' },
        xAxis: { type: 'category', data: ['1月', '2月', '3月', '4月', '5月', '6月'] },
        yAxis: { type: 'value' },
        series: [{
          data: [12, 25, 45, 68, 92, 120],
          type: 'line',
          smooth: true,
          itemStyle: { color: '#1e40af' },
          areaStyle: {
            color: {
              type: 'linear',
              x: 0, y: 0, x2: 0, y2: 1,
              colorStops: [
                { offset: 0, color: 'rgba(30, 64, 175, 0.3)' },
                { offset: 1, color: 'rgba(30, 64, 175, 0.05)' }
              ]
            }
          }
        }]
      })
    }
  })
}

onMounted(async () => {
  try {
    const res = await getStatistics()
    stats.value = res
    initCharts()
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
})
</script>

<style lang="scss" scoped>
.admin-dashboard {
  min-height: 100vh;
}

.sidebar {
  background: #1f2937;
  min-height: 100vh;
  
  .logo {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 20px;
    border-bottom: 1px solid #374151;
    
    span {
      color: white;
      font-size: 18px;
      font-weight: 600;
    }
  }
  
  :deep(.el-menu) {
    border-right: none;
  }
}

.header {
  background: white;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  
  .user-info {
    display: flex;
    align-items: center;
    gap: 10px;
    cursor: pointer;
    padding: 4px 12px;
    border-radius: 20px;
    transition: background 0.3s;
    
    &:hover {
      background: #f3f4f6;
    }
  }
}

.el-main {
  background: #f5f7fa;
  
  h2 {
    margin-bottom: 24px;
    color: #1e293b;
  }
}

.stats-row {
  margin-bottom: 24px;
}

.stat-card {
  :deep(.el-card__body) {
    display: flex;
    align-items: center;
    gap: 16px;
  }
  
  .stat-icon {
    width: 64px;
    height: 64px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .stat-info {
    h3 {
      font-size: 28px;
      font-weight: 700;
      color: #1e293b;
      margin-bottom: 4px;
    }
    
    p {
      color: #64748b;
      font-size: 14px;
    }
  }
}

.chart-row {
  margin-bottom: 24px;
}

.chart-container {
  height: 300px;
}
</style>
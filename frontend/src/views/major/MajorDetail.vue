<template>
  <div class="major-detail-page" v-if="major">
    <NavBar />
    
    <!-- 返回导航 -->
    <div class="back-nav">
      <div class="container">
        <el-button link @click="goBack">
          <el-icon><ArrowLeft /></el-icon>
          返回专业列表
        </el-button>
      </div>
    </div>
    
    <!-- 专业头部信息 -->
    <div class="major-header">
      <div class="container">
        <div class="header-content">
          <div class="university-logo" @click="goToUniversity" :style="{ background: !logoLoaded ? getLogoGradient(major.country) : 'white' }">
            <img
              v-if="major.university_logo"
              :src="major.university_logo"
              :alt="major.university_name"
              class="logo-img"
              @load="logoLoaded = true"
              @error="major.university_logo = ''"
            />
            <span v-if="!major.university_logo" class="logo-text">{{ (major.university_name || '?').charAt(0) }}</span>
          </div>
          <div class="major-info">
            <div class="category-tag">
              <el-tag size="small" effect="plain">{{ major.category }}</el-tag>
              <el-tag v-if="major.subcategory" size="small" effect="plain" type="info">{{ major.subcategory }}</el-tag>
            </div>
            <h1>{{ major.name }}</h1>
            <p class="name-en">{{ major.name_en }}</p>
            <div class="meta-info">
              <span class="university" @click="goToUniversity">
                <el-icon><School /></el-icon>
                {{ major.university_name }}
              </span>
              <span class="duration" v-if="major.duration">
                <el-icon><Timer /></el-icon>
                学制: {{ major.duration }}
              </span>
            </div>
            <div class="actions">
              <el-button
                v-if="userStore.isAuthenticated"
                :type="isCollected ? 'primary' : 'default'"
                size="large"
                @click="toggleCollect"
              >
                <el-icon><Star /></el-icon>
                {{ isCollected ? '已收藏' : '收藏专业' }}
              </el-button>
              <el-button v-else size="large" @click="$router.push('/login')">
                <el-icon><Star /></el-icon>
                登录后收藏
              </el-button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 主要内容区 -->
    <div class="container">
      <div class="content-layout">
        <!-- 左侧内容 -->
        <div class="main-content">
          <el-tabs v-model="activeTab" class="major-tabs">
            <el-tab-pane label="专业概况" name="overview">
              <div class="section">
                <h2>专业介绍</h2>
                <p class="description">{{ major.description || '暂无介绍' }}</p>
              </div>
              
              <div class="section" v-if="major.curriculum">
                <h2>课程设置</h2>
                <div class="curriculum-content">{{ major.curriculum }}</div>
              </div>
              
              <div class="section" v-if="major.career_prospects">
                <h2>就业前景</h2>
                <p>{{ major.career_prospects }}</p>
              </div>
            </el-tab-pane>
            
            <el-tab-pane label="申请要求" name="requirements">
              <div class="requirements-grid">
                <div class="req-card" v-if="major.ielts_requirement">
                  <div class="req-icon">
                    <el-icon size="32"><Document /></el-icon>
                  </div>
                  <div class="req-info">
                    <h4>雅思要求</h4>
                    <p class="req-value">{{ major.ielts_requirement }}</p>
                  </div>
                </div>
                
                <div class="req-card" v-if="major.toefl_requirement">
                  <div class="req-icon">
                    <el-icon size="32"><Document /></el-icon>
                  </div>
                  <div class="req-info">
                    <h4>托福要求</h4>
                    <p class="req-value">{{ major.toefl_requirement }}</p>
                  </div>
                </div>
                
                <div class="req-card" v-if="major.gpa_requirement">
                  <div class="req-icon">
                    <el-icon size="32"><Trophy /></el-icon>
                  </div>
                  <div class="req-info">
                    <h4>GPA要求</h4>
                    <p class="req-value">≥ {{ major.gpa_requirement }}</p>
                  </div>
                </div>
                
                <div class="req-card" v-if="major.gre_requirement">
                  <div class="req-icon">
                    <el-icon size="32"><EditPen /></el-icon>
                  </div>
                  <div class="req-info">
                    <h4>GRE要求</h4>
                    <p class="req-value">{{ major.gre_requirement }}</p>
                  </div>
                </div>
                
                <div class="req-card" v-if="major.gmat_requirement">
                  <div class="req-icon">
                    <el-icon size="32"><EditPen /></el-icon>
                  </div>
                  <div class="req-info">
                    <h4>GMAT要求</h4>
                    <p class="req-value">{{ major.gmat_requirement }}</p>
                  </div>
                </div>
                
                <div class="req-card" v-if="major.tuition">
                  <div class="req-icon">
                    <el-icon size="32"><Money /></el-icon>
                  </div>
                  <div class="req-info">
                    <h4>学费</h4>
                    <p class="req-value">{{ major.tuition }}</p>
                  </div>
                </div>
              </div>
            </el-tab-pane>
            
            <el-tab-pane label="录取数据" name="statistics">
              <div class="stats-section">
                <div class="stats-grid">
                  <div class="stat-box">
                    <div class="stat-value" :class="getAdmissionRateClass(major.admission_rate)">
                      {{ major.admission_rate ? major.admission_rate + '%' : '暂无数据' }}
                    </div>
                    <div class="stat-label">录取率</div>
                  </div>
                  <div class="stat-box">
                    <div class="stat-value">{{ major.avg_gpa || '暂无' }}</div>
                    <div class="stat-label">平均GPA</div>
                  </div>
                  <div class="stat-box">
                    <div class="stat-value">{{ major.avg_ielts || '暂无' }}</div>
                    <div class="stat-label">平均雅思</div>
                  </div>
                  <div class="stat-box">
                    <div class="stat-value">{{ major.total_admitted || '暂无' }}</div>
                    <div class="stat-label">录取人数</div>
                  </div>
                </div>
                
                <div class="chart-section" v-if="admissionData">
                  <h3>近年录取趋势</h3>
                  <div ref="admissionChart" class="chart"></div>
                </div>
              </div>
            </el-tab-pane>
          </el-tabs>
        </div>
        
        <!-- 右侧边栏 -->
        <div class="sidebar">
          <div class="sidebar-card">
            <h3>所属院校</h3>
            <div class="uni-info" @click="goToUniversity">
              <div class="sidebar-uni-logo" :style="{ background: !sidebarLogoLoaded ? getLogoGradient(major.country) : 'white' }">
                <img
                  v-if="major.university_logo"
                  :src="major.university_logo"
                  :alt="major.university_name"
                  class="logo-img-sm"
                  @load="sidebarLogoLoaded = true"
                  @error="major.university_logo = ''"
                />
                <span v-if="!major.university_logo" class="logo-text-sm">{{ (major.university_name || '?').charAt(0) }}</span>
              </div>
              <div class="uni-details">
                <h4>{{ major.university_name }}</h4>
                <p>点击查看院校详情</p>
              </div>
            </div>
          </div>
          
          <div class="sidebar-card">
            <h3>相关专业推荐</h3>
            <div class="related-majors">
              <div 
                v-for="related in relatedMajors" 
                :key="related.id"
                class="related-item"
                @click="goToMajor(related.id)"
              >
                <span class="related-name">{{ related.name }}</span>
                <el-icon><ArrowRight /></el-icon>
              </div>
            </div>
          </div>
          
          <div class="sidebar-card">
            <h3>申请工具</h3>
            <div class="tool-links">
              <router-link to="/guides" class="tool-item">
                <el-icon><Document /></el-icon>
                <span>申请攻略</span>
              </router-link>
              <router-link to="/favorites" class="tool-item">
                <el-icon><Star /></el-icon>
                <span>我的收藏</span>
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <Footer />
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import NavBar from '@/components/common/NavBar.vue'
import Footer from '@/components/common/Footer.vue'
import { getMajor, addCollection, removeCollection, checkCollection, getMajors } from '@/utils/api'
import { getLogoGradient } from '@/utils/logoHelper'
import { ElMessage } from 'element-plus'
import * as echarts from 'echarts'
import { 
  ArrowLeft, School, Timer, Star, Document, 
  Trophy, EditPen, Money, ArrowRight 
} from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const major = ref(null)
const activeTab = ref('overview')
const isCollected = ref(false)
const collectionId = ref(null)
const relatedMajors = ref([])
const admissionChart = ref(null)
const admissionData = ref(null)
const logoLoaded = ref(false)
const sidebarLogoLoaded = ref(false)

const getAdmissionRateClass = (rate) => {
  if (!rate) return ''
  if (rate >= 20) return 'high'
  if (rate >= 10) return 'medium'
  return 'low'
}

const fetchMajor = async () => {
  try {
    const res = await getMajor(route.params.id)
    major.value = res
    
    // 获取相关专业
    fetchRelatedMajors(res.category, res.university_id)
  } catch (error) {
    console.error('获取专业详情失败:', error)
    ElMessage.error('获取专业信息失败')
  }
}

const fetchRelatedMajors = async (category, universityId) => {
  try {
    const res = await getMajors({ university_id: universityId, limit: 5 })
    const allMajors = Array.isArray(res) ? res : []
    relatedMajors.value = allMajors
      .filter(m => m.id !== parseInt(route.params.id))
      .slice(0, 4)
  } catch (error) {
    console.error('获取相关专业失败:', error)
  }
}

const checkIfCollected = async () => {
  if (!userStore.isAuthenticated) return
  try {
    const res = await checkCollection('major', parseInt(route.params.id))
    isCollected.value = res.is_collected
    collectionId.value = res.collection_id
  } catch (error) {
    console.error('检查收藏状态失败:', error)
  }
}

const toggleCollect = async () => {
  try {
    if (isCollected.value && collectionId.value) {
      await removeCollection(collectionId.value)
      isCollected.value = false
      collectionId.value = null
      ElMessage.success('已取消收藏')
    } else {
      const res = await addCollection({
        collection_type: 'major',
        target_id: parseInt(route.params.id)
      })
      isCollected.value = true
      collectionId.value = res.id
      ElMessage.success('收藏成功')
    }
  } catch (error) {
    console.error('收藏操作失败:', error)
  }
}

const goBack = () => {
  router.back()
}

const goToUniversity = () => {
  if (major.value?.university_id) {
    router.push(`/universities/${major.value.university_id}`)
  }
}

const goToMajor = (id) => {
  router.push(`/majors/${id}`)
  // 重新加载页面数据
  setTimeout(() => {
    window.location.reload()
  }, 100)
}

const initChart = () => {
  nextTick(() => {
    if (admissionChart.value && major.value?.admission_rate) {
      const chart = echarts.init(admissionChart.value)
      chart.setOption({
        tooltip: { trigger: 'axis' },
        xAxis: { type: 'category', data: ['2024', '2025', '2026'] },
        yAxis: { type: 'value', name: '录取率(%)' },
        series: [{
          data: [
            major.value.admission_rate * 1.2,
            major.value.admission_rate * 1.1,
            major.value.admission_rate
          ],
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

onMounted(() => {
  fetchMajor()
  checkIfCollected()
  initChart()
})
</script>

<style lang="scss" scoped>
.major-detail-page {
  min-height: 100vh;
  background: #f5f7fa;
  padding-top: 70px;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

// 返回导航
.back-nav {
  background: white;
  border-bottom: 1px solid #e2e8f0;
  padding: 12px 0;
  
  .el-button {
    font-size: 14px;
    color: #64748b;
    
    &:hover {
      color: #1e40af;
    }
  }
}

// 头部信息
.major-header {
  background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
  padding: 60px 0;
  color: white;
}

.header-content {
  display: flex;
  gap: 40px;
  align-items: center;
}

.university-logo {
  width: 120px;
  height: 120px;
  border-radius: 16px;
  cursor: pointer;
  transition: transform 0.3s ease;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  
  &:hover {
    transform: scale(1.05);
  }
  
  .logo-img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    padding: 8px;
    border-radius: 16px;
  }
  
  .logo-text {
    font-size: 56px;
    font-weight: 700;
    color: white;
    line-height: 1;
  }
}

.major-info {
  flex: 1;
  
  .category-tag {
    margin-bottom: 12px;
    
    .el-tag {
      margin-right: 8px;
    }
  }
  
  h1 {
    font-size: 36px;
    font-weight: 700;
    margin-bottom: 8px;
  }
  
  .name-en {
    font-size: 18px;
    opacity: 0.9;
    margin-bottom: 16px;
  }
  
  .meta-info {
    display: flex;
    gap: 24px;
    margin-bottom: 20px;
    
    span {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 15px;
      opacity: 0.95;
      
      &.university {
        cursor: pointer;
        
        &:hover {
          text-decoration: underline;
        }
      }
    }
  }
  
  .actions {
    .el-button {
      padding: 12px 24px;
      font-size: 15px;
    }
  }
}

// 内容布局
.content-layout {
  display: grid;
  grid-template-columns: 1fr 340px;
  gap: 24px;
  padding: 40px 0;
}

// 主内容区
.main-content {
  .major-tabs {
    background: white;
    border-radius: 16px;
    padding: 24px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  }
}

.section {
  margin-bottom: 32px;
  
  h2 {
    font-size: 20px;
    font-weight: 600;
    color: #1e293b;
    margin-bottom: 16px;
    padding-bottom: 12px;
    border-bottom: 2px solid #e2e8f0;
  }
  
  .description {
    font-size: 15px;
    line-height: 1.8;
    color: #475569;
  }
  
  .curriculum-content {
    font-size: 15px;
    line-height: 1.8;
    color: #475569;
    white-space: pre-line;
  }
}

// 申请要求网格
.requirements-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.req-card {
  background: #f8fafc;
  border-radius: 12px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  transition: all 0.3s ease;
  
  &:hover {
    background: #e0e7ff;
  }
  
  .req-icon {
    width: 56px;
    height: 56px;
    background: white;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #1e40af;
  }
  
  .req-info {
    h4 {
      font-size: 14px;
      color: #64748b;
      margin-bottom: 4px;
    }
    
    .req-value {
      font-size: 20px;
      font-weight: 700;
      color: #1e293b;
    }
  }
}

// 统计数据
.stats-section {
  .stats-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 32px;
  }
  
  .stat-box {
    background: #f8fafc;
    border-radius: 12px;
    padding: 24px;
    text-align: center;
    
    .stat-value {
      font-size: 28px;
      font-weight: 700;
      color: #1e293b;
      margin-bottom: 8px;
      
      &.high { color: #16a34a; }
      &.medium { color: #d97706; }
      &.low { color: #dc2626; }
    }
    
    .stat-label {
      font-size: 14px;
      color: #64748b;
    }
  }
  
  .chart-section {
    background: #f8fafc;
    border-radius: 12px;
    padding: 24px;
    
    h3 {
      font-size: 16px;
      font-weight: 600;
      margin-bottom: 16px;
    }
    
    .chart {
      height: 250px;
    }
  }
}

// 侧边栏
.sidebar {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.sidebar-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  
  h3 {
    font-size: 16px;
    font-weight: 600;
    color: #1e293b;
    margin-bottom: 16px;
  }
  
  .uni-info {
    display: flex;
    align-items: center;
    gap: 16px;
    cursor: pointer;
    padding: 12px;
    border-radius: 12px;
    transition: background 0.3s ease;
    
    &:hover {
      background: #f8fafc;
    }
    
    .sidebar-uni-logo {
      width: 60px;
      height: 60px;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      
      .logo-img-sm {
        width: 100%;
        height: 100%;
        object-fit: contain;
        padding: 4px;
        border-radius: 8px;
      }
      
      .logo-text-sm {
        font-size: 26px;
        font-weight: 700;
        color: white;
        line-height: 1;
      }
    }
    
    .uni-details {
      h4 {
        font-size: 15px;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 4px;
      }
      
      p {
        font-size: 13px;
        color: #64748b;
      }
    }
  }
  
  .related-majors {
    .related-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 12px 0;
      border-bottom: 1px solid #e2e8f0;
      cursor: pointer;
      transition: all 0.3s ease;
      
      &:last-child {
        border-bottom: none;
      }
      
      &:hover {
        color: #1e40af;
        
        .el-icon {
          transform: translateX(4px);
        }
      }
      
      .related-name {
        font-size: 14px;
      }
      
      .el-icon {
        transition: transform 0.3s ease;
        color: #94a3b8;
      }
    }
  }
  
  .tool-links {
    .tool-item {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 12px;
      border-radius: 8px;
      color: #475569;
      text-decoration: none;
      transition: all 0.3s ease;
      
      &:hover {
        background: #e0e7ff;
        color: #1e40af;
      }
      
      .el-icon {
        color: #1e40af;
      }
    }
  }
}

// 响应式
@media (max-width: 1024px) {
  .content-layout {
    grid-template-columns: 1fr;
  }
  
  .sidebar {
    order: -1;
  }
  
  .requirements-grid {
    grid-template-columns: 1fr;
  }
  
  .stats-grid {
    grid-template-columns: repeat(2, 1fr) !important;
  }
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    text-align: center;
  }
  
  .major-info {
    h1 {
      font-size: 28px;
    }
    
    .meta-info {
      justify-content: center;
      flex-wrap: wrap;
    }
  }
  
  .stats-grid {
    grid-template-columns: 1fr !important;
  }
}
</style>
<template>
  <div class="home-page">
    <NavBar />
    
    <!-- 轮播图 Banner -->
    <section class="hero-banner">
      <el-carousel height="500px" :interval="5000" arrow="always">
        <el-carousel-item v-for="(banner, index) in banners" :key="index">
          <div class="banner-item" :style="{ backgroundImage: `url(${banner.image})` }">
            <div class="banner-overlay"></div>
            <div class="banner-content">
              <h1>{{ banner.title }}</h1>
              <p>{{ banner.subtitle }}</p>
              <el-button type="primary" size="large" @click="handleBannerClick(banner.link)">
                {{ banner.buttonText }}
              </el-button>
            </div>
          </div>
        </el-carousel-item>
      </el-carousel>
    </section>
    
    <!-- 快捷入口 -->
    <section class="quick-access">
      <div class="container">
        <div class="quick-grid">
          <router-link to="/universities" class="quick-item">
            <div class="quick-icon">
              <el-icon :size="32"><School /></el-icon>
            </div>
            <h3>院校库</h3>
            <p>全球顶尖院校</p>
          </router-link>
          <router-link to="/majors" class="quick-item">
            <div class="quick-icon">
              <el-icon :size="32"><Collection /></el-icon>
            </div>
            <h3>专业库</h3>
            <p>热门专业信息</p>
          </router-link>
          <router-link to="/guides" class="quick-item">
            <div class="quick-icon">
              <el-icon :size="32"><Document /></el-icon>
            </div>
            <h3>申请攻略</h3>
            <p>申请经验分享</p>
          </router-link>
          <router-link to="/favorites" class="quick-item">
            <div class="quick-icon">
              <el-icon :size="32"><Star /></el-icon>
            </div>
            <h3>我的收藏</h3>
            <p>收藏院校专业</p>
          </router-link>
        </div>
      </div>
    </section>
    
    <!-- 热门院校推荐 -->
    <section class="section hot-universities">
      <div class="container">
        <div class="section-header">
          <div class="header-left">
            <h2>热门院校推荐</h2>
            <p class="section-desc">精选全球顶尖院校，助你找到梦校</p>
          </div>
          <router-link to="/universities" class="view-more">
            查看全部 <el-icon><ArrowRight /></el-icon>
          </router-link>
        </div>
        
        <!-- 国家筛选标签 -->
        <div class="country-tabs">
          <el-radio-group v-model="selectedCountry" size="large" @change="filterUniversities">
            <el-radio-button label="">全部</el-radio-button>
            <el-radio-button label="美国">美国</el-radio-button>
            <el-radio-button label="英国">英国</el-radio-button>
            <el-radio-button label="新加坡">新加坡</el-radio-button>
            <el-radio-button label="中国香港">中国香港</el-radio-button>
            <el-radio-button label="澳大利亚">澳大利亚</el-radio-button>
            <el-radio-button label="加拿大">加拿大</el-radio-button>
          </el-radio-group>
        </div>
        
        <div class="universities-grid">
          <div 
            v-for="uni in displayedUniversities" 
            :key="uni.id" 
            class="university-card"
            @click="goToUniversity(uni.id)"
          >
            <div class="card-header">
              <div class="uni-logo" :style="{ background: !uni._logoLoaded ? getLogoGradient(uni.country) : 'white' }">
                <img
                  v-if="uni.logo_url"
                  :src="uni.logo_url"
                  :alt="uni.name"
                  class="uni-logo-img"
                  @load="uni._logoLoaded = true"
                  @error="uni.logo_url = ''"
                />
                <span v-if="!uni.logo_url" class="uni-logo-text">{{ uni.name.charAt(0) }}</span>
              </div>
              <div class="rank-badge" v-if="uni.qs_ranking">
                <span class="rank-num">{{ uni.qs_ranking }}</span>
                <span class="rank-label">QS</span>
              </div>
            </div>
            <div class="card-body">
              <h3 class="uni-name">{{ uni.name }}</h3>
              <p class="uni-name-en">{{ uni.name_en }}</p>
              <div class="uni-meta">
                <span class="location">
                  <el-icon><Location /></el-icon>
                  {{ uni.country }} · {{ uni.location }}
                </span>
              </div>
              <div class="uni-tags">
                <el-tag :type="getDifficultyType(uni.difficulty)" size="small">
                  {{ getDifficultyText(uni.difficulty) }}
                </el-tag>
                <el-tag type="info" size="small" v-if="uni.us_news_ranking">
                  US News {{ uni.us_news_ranking }}
                </el-tag>
              </div>
            </div>
            <div class="card-footer">
              <span class="tuition">{{ uni.tuition_range }}</span>
              <el-button link type="primary">查看详情</el-button>
            </div>
          </div>
        </div>
      </div>
    </section>
    
    <!-- 申请季时间轴 -->
    <section class="section timeline-section">
      <div class="container">
        <div class="section-header center">
          <h2>申请季时间轴</h2>
          <p class="section-desc">合理规划申请时间，把握每一个关键节点</p>
        </div>
        
        <div class="timeline-wrapper">
          <div class="timeline-tabs">
            <el-radio-group v-model="selectedTimeline" size="large">
              <el-radio-button label="us">美国</el-radio-button>
              <el-radio-button label="uk">英国</el-radio-button>
              <el-radio-button label="asia">新加坡/香港</el-radio-button>
            </el-radio-group>
          </div>
          
          <div class="timeline-content">
            <el-timeline>
              <el-timeline-item
                v-for="(item, index) in currentTimeline"
                :key="index"
                :type="item.type"
                :color="item.color"
                :icon="item.icon"
                :timestamp="item.time"
                placement="top"
              >
                <div class="timeline-card">
                  <h4>{{ item.title }}</h4>
                  <p>{{ item.content }}</p>
                  <el-tag size="small" :type="item.tagType">{{ item.tag }}</el-tag>
                </div>
              </el-timeline-item>
            </el-timeline>
          </div>
        </div>
      </div>
    </section>
    
    <!-- 热门专业分类 -->
    <section class="section major-categories">
      <div class="container">
        <div class="section-header center">
          <h2>热门专业分类</h2>
          <p class="section-desc">按学科探索适合你的专业方向</p>
        </div>
        
        <div class="categories-grid">
          <div 
            v-for="cat in categories" 
            :key="cat.name"
            class="category-card"
            :style="{ background: cat.gradient }"
            @click="goToMajor(cat.name)"
          >
            <div class="category-icon">
              <el-icon :size="48"><component :is="cat.icon" /></el-icon>
            </div>
            <h3>{{ cat.name }}</h3>
            <p>{{ cat.desc }}</p>
            <div class="category-stats">
              <span>{{ cat.count }}个专业</span>
              <el-icon><ArrowRight /></el-icon>
            </div>
          </div>
        </div>
      </div>
    </section>
    
    <!-- 数据看板 -->
    <section class="section data-dashboard">
      <div class="container">
        <div class="section-header center">
          <h2>申请数据看板</h2>
          <p class="section-desc">近3年录取数据分析，助你制定申请策略</p>
        </div>
        
        <div class="dashboard-grid">
          <!-- 统计卡片 -->
          <div class="stats-cards">
            <div class="stat-card">
              <div class="stat-icon" style="background: #e0e7ff;">
                <el-icon :size="24" color="#4f46e5"><School /></el-icon>
              </div>
              <div class="stat-info">
                <h4>{{ stats.university_count }}</h4>
                <p>合作院校</p>
              </div>
            </div>
            <div class="stat-card">
              <div class="stat-icon" style="background: #dcfce7;">
                <el-icon :size="24" color="#16a34a"><Collection /></el-icon>
              </div>
              <div class="stat-info">
                <h4>{{ stats.major_count }}</h4>
                <p>专业数量</p>
              </div>
            </div>
            <div class="stat-card">
              <div class="stat-icon" style="background: #fef3c7;">
                <el-icon :size="24" color="#d97706"><User /></el-icon>
              </div>
              <div class="stat-info">
                <h4>{{ stats.user_count }}</h4>
                <p>注册用户</p>
              </div>
            </div>
            <div class="stat-card">
              <div class="stat-icon" style="background: #fce7f3;">
                <el-icon :size="24" color="#db2777"><Document /></el-icon>
              </div>
              <div class="stat-info">
                <h4>{{ stats.guide_count }}</h4>
                <p>申请攻略</p>
              </div>
            </div>
          </div>
          
          <!-- 录取率趋势图 -->
          <div class="chart-container">
            <h3>热门专业录取率趋势</h3>
            <div ref="admissionChart" class="chart"></div>
          </div>
          
          <!-- 平均GPA分布 -->
          <div class="chart-container">
            <h3>录取学生平均GPA分布</h3>
            <div ref="gpaChart" class="chart"></div>
          </div>
        </div>
      </div>
    </section>
    
    <!-- 最新攻略 -->
    <section class="section latest-guides">
      <div class="container">
        <div class="section-header">
          <div class="header-left">
            <h2>最新申请攻略</h2>
            <p class="section-desc">前辈经验分享，助你少走弯路</p>
          </div>
          <router-link to="/guides" class="view-more">
            查看全部 <el-icon><ArrowRight /></el-icon>
          </router-link>
        </div>
        
        <div class="guides-grid">
          <div 
            v-for="guide in latestGuides" 
            :key="guide.id"
            class="guide-card"
            @click="goToGuide(guide.id)"
          >
            <div class="guide-category">
              <el-tag size="small" effect="plain">{{ guide.category }}</el-tag>
            </div>
            <h3>{{ guide.title }}</h3>
            <p class="guide-summary">{{ guide.summary }}</p>
            <div class="guide-meta">
              <span class="author">
                <el-icon><User /></el-icon>
                {{ guide.author_name || '匿名' }}
              </span>
              <span class="views">
                <el-icon><View /></el-icon>
                {{ guide.views || 0 }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </section>
    
    <!-- CTA Section -->
    <section class="cta-section">
      <div class="container">
        <div class="cta-content" v-if="!isLoggedIn">
          <h2>开启你的留学申请之旅</h2>
          <p>注册账号，收藏心仪院校，获取个性化申请建议</p>
          <div class="cta-buttons">
            <el-button type="primary" size="large" @click="goToRegister">
              立即注册
            </el-button>
            <el-button size="large" @click="goToUniversities">
              浏览院校
            </el-button>
          </div>
        </div>
        <div class="cta-content" v-else>
          <h2>探索更多留学资源</h2>
          <p>浏览院校专业、查看录取案例、阅读申请攻略</p>
          <div class="cta-buttons">
            <el-button type="primary" size="large" @click="goToUniversities">
              浏览院校
            </el-button>
            <el-button size="large" @click="router.push('/cases')">
              查看案例
            </el-button>
          </div>
        </div>
      </div>
    </section>
    
    <Footer />
  </div>
</template>

<script setup>
import { ref, onMounted, computed, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import NavBar from '@/components/common/NavBar.vue'
import Footer from '@/components/common/Footer.vue'
import { getUniversities, getGuides, getStatistics } from '@/utils/api'
import { getLogoGradient } from '@/utils/logoHelper'
import { ElMessage } from 'element-plus'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const isLoggedIn = computed(() => !!userStore.token)
import * as echarts from 'echarts'
import { 
  Search, ArrowRight, School, Collection, Document, Star, 
  Location, User, View, Cpu, Money, Brush, 
  Reading, FirstAidKit, Monitor 
} from '@element-plus/icons-vue'

const router = useRouter()

// 轮播图数据
const banners = [
  {
    title: '2025硕士申请季开启',
    subtitle: '全球顶尖院校申请指南，助你圆梦名校',
    buttonText: '开始探索',
    link: '/universities',
    image: 'https://images.unsplash.com/photo-1523050854058-8df90110c9f1?w=1920'
  },
  {
    title: '美国常春藤名校申请攻略',
    subtitle: '哈佛、耶鲁、普林斯顿等名校申请经验分享',
    buttonText: '查看攻略',
    link: '/guides',
    image: 'https://images.unsplash.com/photo-1562774053-701939374585?w=1920'
  },
  {
    title: '英国G5院校申请指南',
    subtitle: '牛津、剑桥等英国顶尖院校申请全解析',
    buttonText: '了解更多',
    link: '/universities?country=英国',
    image: 'https://images.unsplash.com/photo-1607237138185-eed4eae9a487?w=1920'
  }
]

// 统计数据
const stats = ref({
  university_count: 0,
  major_count: 0,
  user_count: 0,
  guide_count: 0
})

// 院校数据
const universities = ref([])
const selectedCountry = ref('')
const displayedUniversities = computed(() => {
  let filtered = universities.value
  if (selectedCountry.value) {
    filtered = filtered.filter(u => u.country === selectedCountry.value)
  }
  return filtered.slice(0, 8)
})

// 时间轴数据
const selectedTimeline = ref('us')
const timelines = {
  us: [
    { time: '6-8月', title: '准备阶段', content: '确定目标院校，准备语言考试，开始撰写文书', tag: '关键期', tagType: 'danger', type: 'primary', color: '#1e40af' },
    { time: '9-10月', title: '申请开放', content: '美国院校陆续开放申请，准备提交材料', tag: '高峰期', tagType: 'warning', type: 'warning', color: '#d97706' },
    { time: '11-12月', title: '截止冲刺', content: '大部分院校申请截止，完成所有申请提交', tag: '截止期', tagType: 'danger', type: 'danger', color: '#dc2626' },
    { time: '1-3月', title: '面试阶段', content: '收到面试邀请，准备并参加面试', tag: '面试期', tagType: 'success', type: 'success', color: '#16a34a' },
    { time: '4-5月', title: '录取结果', content: '收到录取通知，确定最终入读院校', tag: '收获期', tagType: 'primary', type: 'primary', color: '#1e40af' }
  ],
  uk: [
    { time: '9-10月', title: '申请开放', content: '英国院校开放申请，建议尽早提交', tag: '黄金期', tagType: 'warning', type: 'primary', color: '#1e40af' },
    { time: '11-12月', title: '首轮截止', content: '部分热门专业首轮申请截止', tag: '关键期', tagType: 'danger', type: 'warning', color: '#d97706' },
    { time: '1-3月', title: '滚动录取', content: '滚动录取阶段，名额逐渐减少', tag: '补申期', tagType: 'info', type: 'info', color: '#6b7280' },
    { time: '4-6月', title: '语言成绩', content: '提交最终语言成绩，换取无条件录取', tag: '冲刺期', tagType: 'success', type: 'success', color: '#16a34a' }
  ],
  asia: [
    { time: '9-11月', title: '秋季申请', content: '新加坡、香港院校秋季入学申请开放', tag: '主申期', tagType: 'primary', type: 'primary', color: '#1e40af' },
    { time: '12-1月', title: '首轮截止', content: '热门专业首轮申请截止', tag: '截止期', tagType: 'danger', type: 'danger', color: '#dc2626' },
    { time: '2-4月', title: '春季申请', content: '部分院校春季入学申请开放', tag: '次申期', tagType: 'info', type: 'info', color: '#6b7280' },
    { time: '5-7月', title: '签证办理', content: '收到录取后办理签证，准备入学', tag: '准备期', tagType: 'success', type: 'success', color: '#16a34a' }
  ]
}
const currentTimeline = computed(() => timelines[selectedTimeline.value])

// 专业分类
const categories = [
  { name: '工科', icon: 'Cpu', desc: '计算机、电子、机械等', count: 25, gradient: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' },
  { name: '商科', icon: 'Money', desc: '金融、管理、市场等', count: 20, gradient: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)' },
  { name: '理科', icon: 'Monitor', desc: '数学、物理、化学等', count: 15, gradient: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)' },
  { name: '文科', icon: 'Reading', desc: '文学、历史、哲学等', count: 12, gradient: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)' },
  { name: '医学', icon: 'FirstAidKit', desc: '临床、药学、护理等', count: 8, gradient: 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)' },
  { name: '艺术', icon: 'Brush', desc: '设计、音乐、美术等', count: 6, gradient: 'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)' }
]

// 攻略数据
const latestGuides = ref([])

// 图表引用
const admissionChart = ref(null)
const gpaChart = ref(null)

const getDifficultyText = (difficulty) => {
  const map = { low: '容易', medium: '中等', high: '困难' }
  return map[difficulty] || difficulty
}

const getDifficultyType = (difficulty) => {
  const map = { low: 'success', medium: 'warning', high: 'danger' }
  return map[difficulty] || 'info'
}

const fetchData = async () => {
  try {
    // 获取院校数据（Axios interceptor 已经 unwrap response.data）
    const uniRes = await getUniversities({ limit: 20 })
    universities.value = Array.isArray(uniRes) ? uniRes : []
    
    // 获取统计数据
    const statsRes = await getStatistics()
    if (statsRes) {
      stats.value = statsRes
    }
    
    // 获取攻略数据
    const guideRes = await getGuides({ limit: 4 })
    latestGuides.value = (Array.isArray(guideRes) ? guideRes : []).slice(0, 4)
  } catch (error) {
    console.error('获取数据失败:', error)
    ElMessage.error('获取数据失败')
  }
}

const initCharts = () => {
  nextTick(() => {
    // 录取率趋势图
    if (admissionChart.value) {
      const chart1 = echarts.init(admissionChart.value)
      chart1.setOption({
        tooltip: { trigger: 'axis' },
        legend: { data: ['计算机科学', '金融工程', '数据科学'] },
        xAxis: { type: 'category', data: ['2024', '2025', '2026'] },
        yAxis: { type: 'value', name: '录取率(%)', max: 30 },
        series: [
          { name: '计算机科学', type: 'line', data: [12, 10, 8], smooth: true, itemStyle: { color: '#1e40af' } },
          { name: '金融工程', type: 'line', data: [15, 13, 11], smooth: true, itemStyle: { color: '#16a34a' } },
          { name: '数据科学', type: 'line', data: [18, 16, 14], smooth: true, itemStyle: { color: '#d97706' } }
        ]
      })
    }
    
    // GPA分布图
    if (gpaChart.value) {
      const chart2 = echarts.init(gpaChart.value)
      chart2.setOption({
        tooltip: { trigger: 'item' },
        legend: { orient: 'vertical', right: 10, top: 'center' },
        series: [{
          name: 'GPA分布',
          type: 'pie',
          radius: ['40%', '70%'],
          avoidLabelOverlap: false,
          itemStyle: { borderRadius: 10, borderColor: '#fff', borderWidth: 2 },
          label: { show: false },
          data: [
            { value: 15, name: '3.8+', itemStyle: { color: '#1e40af' } },
            { value: 35, name: '3.5-3.8', itemStyle: { color: '#3b82f6' } },
            { value: 30, name: '3.2-3.5', itemStyle: { color: '#60a5fa' } },
            { value: 20, name: '3.0-3.2', itemStyle: { color: '#93c5fd' } }
          ]
        }]
      })
    }
  })
}

const handleBannerClick = (link) => {
  router.push(link)
}

const filterUniversities = () => {
  // 筛选逻辑在 computed 中处理
}

const goToUniversity = (id) => {
  router.push(`/universities/${id}`)
}

const goToMajor = (category) => {
  router.push({ path: '/majors', query: { category } })
}

const goToGuide = (id) => {
  router.push(`/guides/${id}`)
}

const goToRegister = () => {
  router.push('/register')
}

const goToUniversities = () => {
  router.push('/universities')
}

onMounted(() => {
  fetchData()
  initCharts()
})
</script>

<style lang="scss" scoped>
.home-page {
  min-height: 100vh;
  background: #f5f7fa;
}

// 轮播图
.hero-banner {
  .banner-item {
    height: 500px;
    background-size: cover;
    background-position: center;
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .banner-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: linear-gradient(135deg, rgba(30, 64, 175, 0.85) 0%, rgba(59, 130, 246, 0.75) 100%);
  }
  
  .banner-content {
    position: relative;
    z-index: 1;
    text-align: center;
    color: white;
    max-width: 700px;
    padding: 0 20px;
    
    h1 {
      font-size: 48px;
      font-weight: 700;
      margin-bottom: 16px;
      text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    p {
      font-size: 20px;
      margin-bottom: 32px;
      opacity: 0.95;
    }
    
    .el-button {
      padding: 16px 40px;
      font-size: 16px;
      border-radius: 8px;
    }
  }
}

// 快捷入口
.quick-access {
  background: white;
  padding: 40px 0;
  margin-top: -40px;
  position: relative;
  z-index: 10;
  border-radius: 24px 24px 0 0;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.quick-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}

.quick-item {
  background: white;
  border-radius: 16px;
  padding: 32px 24px;
  text-align: center;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
  text-decoration: none;
  color: inherit;
  border: 1px solid #e2e8f0;
  
  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
    border-color: #3b82f6;
  }
  
  .quick-icon {
    width: 64px;
    height: 64px;
    background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
    border-radius: 16px;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 16px;
    color: white;
  }
  
  h3 {
    font-size: 18px;
    font-weight: 600;
    color: #1e293b;
    margin-bottom: 8px;
  }
  
  p {
    font-size: 14px;
    color: #64748b;
  }
}

// 通用区块样式
.section {
  padding: 80px 0;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 40px;
  
  &.center {
    text-align: center;
    flex-direction: column;
    align-items: center;
  }
  
  h2 {
    font-size: 32px;
    font-weight: 700;
    color: #1e293b;
    margin-bottom: 8px;
  }
  
  .section-desc {
    font-size: 16px;
    color: #64748b;
  }
  
  .view-more {
    display: flex;
    align-items: center;
    gap: 4px;
    color: #3b82f6;
    font-weight: 500;
    text-decoration: none;
    
    &:hover {
      color: #1e40af;
    }
  }
}

// 热门院校
.hot-universities {
  background: white;
}

.country-tabs {
  margin-bottom: 32px;
  
  .el-radio-group {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
  }
}

.universities-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}

.university-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
  cursor: pointer;
  
  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
  }
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    padding: 20px 20px 0;
    
    .uni-logo {
      width: 64px;
      height: 64px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
      
      .uni-logo-img {
        width: 100%;
        height: 100%;
        object-fit: contain;
        padding: 4px;
      }
      
      .uni-logo-text {
        font-size: 28px;
        font-weight: 700;
        color: white;
        line-height: 1;
      }
    }
    
    .rank-badge {
      background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
      color: white;
      padding: 6px 12px;
      border-radius: 20px;
      text-align: center;
      
      .rank-num {
        font-size: 18px;
        font-weight: 700;
        display: block;
      }
      
      .rank-label {
        font-size: 11px;
        opacity: 0.9;
      }
    }
  }
  
  .card-body {
    padding: 16px 20px;
    
    .uni-name {
      font-size: 18px;
      font-weight: 600;
      color: #1e293b;
      margin-bottom: 4px;
    }
    
    .uni-name-en {
      font-size: 13px;
      color: #94a3b8;
      margin-bottom: 12px;
    }
    
    .uni-meta {
      margin-bottom: 12px;
      
      .location {
        font-size: 13px;
        color: #64748b;
        display: flex;
        align-items: center;
        gap: 4px;
      }
    }
    
    .uni-tags {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }
  }
  
  .card-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 20px;
    border-top: 1px solid #e2e8f0;
    
    .tuition {
      font-size: 13px;
      color: #64748b;
    }
  }
}

// 时间轴
.timeline-section {
  background: linear-gradient(135deg, #f8fafc 0%, #e0e7ff 100%);
}

.timeline-wrapper {
  max-width: 800px;
  margin: 0 auto;
}

.timeline-tabs {
  text-align: center;
  margin-bottom: 40px;
}

.timeline-content {
  background: white;
  border-radius: 16px;
  padding: 40px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.06);
}

.timeline-card {
  h4 {
    font-size: 16px;
    font-weight: 600;
    color: #1e293b;
    margin-bottom: 8px;
  }
  
  p {
    font-size: 14px;
    color: #64748b;
    margin-bottom: 12px;
    line-height: 1.6;
  }
}

// 专业分类
.major-categories {
  background: white;
}

.categories-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.category-card {
  border-radius: 16px;
  padding: 32px;
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.2);
  }
  
  .category-icon {
    margin-bottom: 16px;
  }
  
  h3 {
    font-size: 24px;
    font-weight: 600;
    margin-bottom: 8px;
  }
  
  p {
    font-size: 14px;
    opacity: 0.9;
    margin-bottom: 20px;
  }
  
  .category-stats {
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 14px;
    opacity: 0.9;
  }
}

// 数据看板
.data-dashboard {
  background: #f8fafc;
}

.dashboard-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
}

.stats-cards {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

.stat-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  
  .stat-icon {
    width: 56px;
    height: 56px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  
  .stat-info {
    h4 {
      font-size: 28px;
      font-weight: 700;
      color: #1e293b;
      margin-bottom: 4px;
    }
    
    p {
      font-size: 14px;
      color: #64748b;
    }
  }
}

.chart-container {
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
  
  .chart {
    height: 250px;
  }
}

// 最新攻略
.latest-guides {
  background: white;
}

.guides-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}

.guide-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  border: 1px solid #e2e8f0;
  transition: all 0.3s ease;
  cursor: pointer;
  
  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
  }
  
  .guide-category {
    margin-bottom: 12px;
  }
  
  h3 {
    font-size: 16px;
    font-weight: 600;
    color: #1e293b;
    margin-bottom: 12px;
    line-height: 1.4;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
  
  .guide-summary {
    font-size: 14px;
    color: #64748b;
    line-height: 1.6;
    margin-bottom: 16px;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
  }
  
  .guide-meta {
    display: flex;
    justify-content: space-between;
    font-size: 13px;
    color: #94a3b8;
    
    span {
      display: flex;
      align-items: center;
      gap: 4px;
    }
  }
}

// CTA Section
.cta-section {
  background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
  padding: 80px 0;
  text-align: center;
  color: white;
  
  .cta-content {
    max-width: 600px;
    margin: 0 auto;
    
    h2 {
      font-size: 36px;
      font-weight: 700;
      margin-bottom: 16px;
    }
    
    p {
      font-size: 18px;
      opacity: 0.9;
      margin-bottom: 32px;
    }
    
    .cta-buttons {
      display: flex;
      gap: 16px;
      justify-content: center;
      
      .el-button {
        padding: 16px 40px;
        font-size: 16px;
        border-radius: 8px;
      }
    }
  }
}

// 响应式
@media (max-width: 1024px) {
  .quick-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .categories-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .guides-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .dashboard-grid {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 768px) {
  .hero-banner {
    .banner-content {
      h1 {
        font-size: 32px;
      }
      
      p {
        font-size: 16px;
      }
    }
  }
  
  .quick-grid {
    grid-template-columns: 1fr;
  }
  
  .categories-grid {
    grid-template-columns: 1fr;
  }
  
  .guides-grid {
    grid-template-columns: 1fr;
  }
  
  .stats-cards {
    grid-template-columns: 1fr;
  }
  
  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }
}
</style>
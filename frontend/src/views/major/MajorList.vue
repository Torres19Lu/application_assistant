<template>
  <div class="major-list-page">
    <NavBar />
    
    <div class="page-header">
      <div class="container">
        <h1>专业库</h1>
        <p>探索全球热门硕士专业，了解申请要求和录取数据</p>
      </div>
    </div>
    
    <div class="container">
      <!-- 筛选区域 - 使用卡片式设计 -->
      <div class="filter-card">
        <div class="filter-row">
          <div class="filter-group">
            <label>学科大类</label>
            <el-select v-model="filters.category" placeholder="全部分类" clearable @change="handleFilterChange">
              <el-option label="工科" value="工科" />
              <el-option label="商科" value="商科" />
              <el-option label="文科" value="文科" />
              <el-option label="理科" value="理科" />
              <el-option label="医学" value="医学" />
              <el-option label="艺术" value="艺术" />
            </el-select>
          </div>
          
          <div class="filter-group">
            <label>国家/地区</label>
            <el-select v-model="filters.country" placeholder="全部国家" clearable @change="handleFilterChange">
              <el-option label="美国" value="美国" />
              <el-option label="英国" value="英国" />
              <el-option label="新加坡" value="新加坡" />
              <el-option label="中国香港" value="中国香港" />
              <el-option label="瑞士" value="瑞士" />
              <el-option label="加拿大" value="加拿大" />
              <el-option label="澳大利亚" value="澳大利亚" />
              <el-option label="日本" value="日本" />
              <el-option label="中国" value="中国" />
            </el-select>
          </div>
          
          <div class="filter-group search-group">
            <label>搜索</label>
            <el-input
              v-model="filters.keyword"
              placeholder="搜索专业名称"
              clearable
              @keyup.enter="handleFilterChange"
            >
              <template #append>
                <el-button @click="handleFilterChange">
                  <el-icon><Search /></el-icon>
                </el-button>
              </template>
            </el-input>
          </div>
        </div>
      </div>
      
      <div class="content-section">
        <!-- 结果统计 -->
        <div class="results-header">
          <div class="results-count">
            共找到 <span class="highlight">{{ total }}</span> 个专业
          </div>
          <div class="sort-options">
            <span>排序：</span>
            <el-radio-group v-model="sortBy" size="small" @change="handleSortChange">
              <el-radio-button label="default">默认</el-radio-button>
              <el-radio-button label="ranking">院校排名</el-radio-button>
              <el-radio-button label="admission">录取率</el-radio-button>
            </el-radio-group>
          </div>
        </div>
        
        <!-- 专业卡片网格 -->
        <div class="majors-grid">
          <div 
            v-for="major in majors" 
            :key="major.id" 
            class="major-card"
            @click="goToDetail(major.id)"
          >
            <!-- 卡片头部 - 院校Logo和收藏按钮 -->
            <div class="card-header">
              <div class="university-logo" :style="{ background: (!major._logoLoaded && major.university_logo) ? getLogoGradient(major.country) : 'transparent' }">
                <img
                  v-if="major.university_logo"
                  :src="major.university_logo"
                  :alt="major.university_name"
                  class="logo-img"
                  @load="() => { major._logoLoaded = true; loadedLogos.add(major.university_logo) }"
                  @error="major.university_logo = ''"
                />
                <span v-if="!major.university_logo" class="logo-text">{{ (major.university_name || '?').charAt(0) }}</span>
              </div>
              <el-button
                v-if="userStore.isAuthenticated"
                class="collect-btn"
                :type="isCollected(major.id) ? 'warning' : 'default'"
                :icon="isCollected(major.id) ? StarFilled : Star"
                circle
                size="small"
                @click.stop="toggleCollect(major.id)"
              />
            </div>
            
            <!-- 专业信息 -->
            <div class="major-info">
              <div class="category-tag">
                <el-tag size="small" effect="plain">{{ major.category }}</el-tag>
              </div>
              <h3 class="major-name">{{ major.name }}</h3>
              <p class="university-name">{{ major.university_name }}</p>
            </div>
            
            <!-- 申请要求 - 使用图标展示 -->
            <div class="requirements">
              <div class="req-row">
                <div class="req-item" v-if="major.ielts_requirement">
                  <div class="req-icon">
                    <el-icon><Document /></el-icon>
                  </div>
                  <div class="req-content">
                    <span class="req-label">雅思</span>
                    <span class="req-value">{{ major.ielts_requirement }}</span>
                  </div>
                </div>
                <div class="req-item" v-if="major.gpa_requirement">
                  <div class="req-icon">
                    <el-icon><Trophy /></el-icon>
                  </div>
                  <div class="req-content">
                    <span class="req-label">GPA</span>
                    <span class="req-value">≥{{ major.gpa_requirement }}</span>
                  </div>
                </div>
              </div>
              <div class="req-row">
                <div class="req-item" v-if="major.toefl_requirement">
                  <div class="req-icon">
                    <el-icon><DocumentChecked /></el-icon>
                  </div>
                  <div class="req-content">
                    <span class="req-label">托福</span>
                    <span class="req-value">{{ major.toefl_requirement }}</span>
                  </div>
                </div>
                <div class="req-item" v-if="major.gre_requirement">
                  <div class="req-icon">
                    <el-icon><Edit /></el-icon>
                  </div>
                  <div class="req-content">
                    <span class="req-label">GRE</span>
                    <span class="req-value">{{ major.gre_requirement }}</span>
                  </div>
                </div>
              </div>
            </div>
            
            <!-- 卡片底部 - 学制和录取率 -->
            <div class="card-footer">
              <div class="footer-item" v-if="major.duration">
                <el-icon><Timer /></el-icon>
                <span>{{ major.duration }}</span>
              </div>
              <div class="footer-item admission-rate" v-if="major.admission_rate">
                <el-icon><TrendCharts /></el-icon>
                <span>录取率 {{ major.admission_rate }}%</span>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 分页 -->
        <div class="pagination-wrapper">
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :total="total"
            :page-sizes="[12, 24, 48]"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handleSizeChange"
            @current-change="handlePageChange"
          />
        </div>
      </div>
    </div>
    
    <Footer />
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import NavBar from '@/components/common/NavBar.vue'
import Footer from '@/components/common/Footer.vue'
import { getMajors, getMajorsCount, addCollection, removeCollection, getCollections } from '@/utils/api'
import { getLogoGradient } from '@/utils/logoHelper'
import { ElMessage } from 'element-plus'
import { Search, Star, StarFilled, Timer, Document, Trophy, DocumentChecked, Edit, TrendCharts } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const majors = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(12)
const sortBy = ref('default')
const collections = ref([])
const loadedLogos = new Set()

const filters = reactive({
  category: route.query.category || '',
  country: '',
  keyword: ''
})

const isCollected = (id) => {
  return collections.value.some(c => c.collection_type === 'major' && c.target_id === id)
}

const fetchMajors = async () => {
  try {
    const params = {
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value,
      sort_by: sortBy.value,
      ...filters
    }
    const countParams = {}
    if (filters.category) countParams.category = filters.category
    if (filters.country) countParams.country = filters.country
    if (filters.keyword) countParams.keyword = filters.keyword
    const [res, countRes] = await Promise.all([
      getMajors(params),
      getMajorsCount(countParams)
    ])
    majors.value = (Array.isArray(res) ? res : []).map(m => ({
      ...m,
      _logoLoaded: loadedLogos.has(m.university_logo)
    }))
    total.value = countRes.total
  } catch (error) {
    console.error('获取专业列表失败:', error)
    ElMessage.error('获取专业列表失败')
  }
}

const fetchCollections = async () => {
  if (!userStore.isAuthenticated) return
  try {
    const res = await getCollections()
    collections.value = (Array.isArray(res) ? res : []).filter(c => c.collection_type === 'major')
  } catch (error) {
    console.error('获取收藏失败:', error)
  }
}

const handleFilterChange = () => {
  currentPage.value = 1
  fetchMajors()
}

const handleSortChange = () => {
  fetchMajors()
}

const handleSizeChange = (val) => {
  pageSize.value = val
  currentPage.value = 1
  fetchMajors()
}

const handlePageChange = (val) => {
  currentPage.value = val
  fetchMajors()
}

const goToDetail = (id) => {
  router.push(`/majors/${id}`)
}

const toggleCollect = async (id) => {
  if (!userStore.isAuthenticated) {
    ElMessage.warning('请先登录')
    router.push('/login')
    return
  }
  
  try {
    const collected = isCollected(id)
    if (collected) {
      const collection = collections.value.find(c => c.target_id === id)
      if (collection) {
        await removeCollection(collection.id)
        collections.value = collections.value.filter(c => c.id !== collection.id)
        ElMessage.success('已取消收藏')
      }
    } else {
      const res = await addCollection({
        collection_type: 'major',
        target_id: id
      })
      collections.value.push(res)
      ElMessage.success('收藏成功')
    }
  } catch (error) {
    console.error('收藏操作失败:', error)
    ElMessage.error('操作失败')
  }
}

onMounted(() => {
  fetchMajors()
  fetchCollections()
})
</script>

<style lang="scss" scoped>
.major-list-page {
  min-height: 100vh;
  background: #f5f7fa;
  padding-top: 70px;
}

.page-header {
  background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
  padding: 60px 0;
  color: white;
  text-align: center;
  
  h1 {
    font-size: 36px;
    font-weight: 700;
    margin-bottom: 12px;
  }
  
  p {
    font-size: 16px;
    opacity: 0.9;
  }
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

// 筛选卡片
.filter-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  margin-top: -30px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  position: relative;
  z-index: 10;
}

.filter-row {
  display: flex;
  gap: 20px;
  align-items: flex-end;
  flex-wrap: wrap;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
  
  label {
    font-size: 13px;
    color: #64748b;
    font-weight: 500;
  }
  
  .el-select,
  .el-input {
    width: 180px;
  }
  
  &.search-group {
    flex: 1;
    min-width: 250px;
    
    .el-input {
      width: 100%;
    }
  }
}

// 内容区域
.content-section {
  padding: 40px 0;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  
  .results-count {
    font-size: 15px;
    color: #475569;
    
    .highlight {
      color: #1e40af;
      font-weight: 600;
      font-size: 18px;
    }
  }
  
  .sort-options {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 14px;
    color: #64748b;
  }
}

// 专业卡片网格
.majors-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}

.major-card {
  background: white;
  border-radius: 16px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
  cursor: pointer;
  border: 1px solid #e2e8f0;
  
  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 40px rgba(0, 0, 0, 0.12);
    border-color: #3b82f6;
  }
}

// 卡片头部
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}

.university-logo {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  
  .logo-img {
    width: 100%;
    height: 100%;
    object-fit: contain;
    padding: 3px;
  }
  
  .logo-text {
    font-size: 24px;
    font-weight: 700;
    color: white;
    line-height: 1;
  }
}

.collect-btn {
  flex-shrink: 0;
}

// 专业信息
.major-info {
  margin-bottom: 20px;
  
  .category-tag {
    margin-bottom: 10px;
  }
  
  .major-name {
    font-size: 18px;
    font-weight: 600;
    color: #1e293b;
    margin-bottom: 6px;
    line-height: 1.4;
  }
  
  .university-name {
    font-size: 14px;
    color: #64748b;
  }
}

// 申请要求
.requirements {
  background: #f8fafc;
  border-radius: 10px;
  padding: 16px;
  margin-bottom: 16px;
}

.req-row {
  display: flex;
  gap: 16px;
  margin-bottom: 12px;
  
  &:last-child {
    margin-bottom: 0;
  }
}

.req-item {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 10px;
}

.req-icon {
  width: 32px;
  height: 32px;
  background: white;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #3b82f6;
  font-size: 16px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.04);
}

.req-content {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.req-label {
  font-size: 12px;
  color: #94a3b8;
}

.req-value {
  font-size: 14px;
  font-weight: 600;
  color: #334155;
}

// 卡片底部
.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 16px;
  border-top: 1px solid #e2e8f0;
}

.footer-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #64748b;
  
  .el-icon {
    font-size: 14px;
  }
  
  &.admission-rate {
    color: #10b981;
    font-weight: 500;
  }
}

// 分页
.pagination-wrapper {
  display: flex;
  justify-content: center;
  padding: 20px 0;
}

// 响应式
@media (max-width: 768px) {
  .filter-row {
    flex-direction: column;
    
    .filter-group {
      width: 100%;
      
      .el-select,
      .el-input {
        width: 100%;
      }
    }
  }
  
  .majors-grid {
    grid-template-columns: 1fr;
  }
  
  .results-header {
    flex-direction: column;
    gap: 16px;
    align-items: flex-start;
  }
}
</style>

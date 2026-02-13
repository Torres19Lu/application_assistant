<template>
  <div class="university-list-page">
    <NavBar />
    
    <div class="page-header">
      <div class="container">
        <h1>院校库</h1>
        <p>探索全球顶尖院校，找到适合您的梦校</p>
      </div>
    </div>
    
    <div class="container">
      <div class="filter-section">
        <div class="filter-row">
          <div class="filter-group">
            <label>国家/地区</label>
            <el-select v-model="filters.country" placeholder="全部国家" clearable @change="handleFilterChange">
              <el-option label="美国" value="美国" />
              <el-option label="英国" value="英国" />
              <el-option label="新加坡" value="新加坡" />
              <el-option label="中国香港" value="中国香港" />
              <el-option label="澳大利亚" value="澳大利亚" />
              <el-option label="加拿大" value="加拿大" />
              <el-option label="瑞士" value="瑞士" />
              <el-option label="日本" value="日本" />
              <el-option label="中国" value="中国" />
            </el-select>
          </div>
          
          <div class="filter-group">
            <label>申请难度</label>
            <el-select v-model="filters.difficulty" placeholder="全部难度" clearable @change="handleFilterChange">
              <el-option label="容易" value="low" />
              <el-option label="中等" value="medium" />
              <el-option label="困难" value="high" />
            </el-select>
          </div>
          
          <div class="filter-group">
            <label>QS排名</label>
            <el-select v-model="filters.ranking" placeholder="不限" clearable @change="handleFilterChange">
              <el-option label="前10" value="10" />
              <el-option label="前50" value="50" />
              <el-option label="前100" value="100" />
              <el-option label="前200" value="200" />
            </el-select>
          </div>
          
          <div class="filter-group search-group">
            <label>关键词</label>
            <el-input
              v-model="filters.keyword"
              placeholder="搜索院校名称"
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
        <div class="results-header">
          <p>共找到 <strong>{{ total }}</strong> 所院校</p>
          <el-radio-group v-model="sortBy" size="small" @change="handleSortChange">
            <el-radio-button label="ranking">按排名</el-radio-button>
            <el-radio-button label="name">按名称</el-radio-button>
          </el-radio-group>
        </div>
        
        <el-row :gutter="24">
          <el-col :xs="24" :sm="12" :md="8" v-for="uni in universities" :key="uni.id">
            <div class="university-card" @click="goToDetail(uni.id)">
              <div class="card-header">
                <div class="uni-logo-wrapper" :style="{ background: (!uni._logoLoaded && uni.logo_url) ? getLogoGradient(uni.country) : 'transparent' }">
                  <img
                    v-if="uni.logo_url"
                    :src="uni.logo_url"
                    :alt="uni.name"
                    class="uni-logo-img"
                    @load="() => { uni._logoLoaded = true; loadedLogos.add(uni.logo_url) }"
                    @error="uni.logo_url = ''"
                  />
                  <span v-if="!uni.logo_url" class="uni-logo-text">{{ uni.name.charAt(0) }}</span>
                </div>
                <el-button
                  v-if="userStore.isAuthenticated"
                  class="collect-btn"
                  :type="isCollected(uni.id) ? 'primary' : 'default'"
                  :icon="isCollected(uni.id) ? StarFilled : Star"
                  circle
                  size="small"
                  @click.stop="toggleCollect(uni.id)"
                />
              </div>
              <h3>{{ uni.name }}</h3>
              <p class="name-en">{{ uni.name_en }}</p>
              <div class="info-row">
                <span class="country">
                  <el-icon><Location /></el-icon>
                  {{ uni.country }}
                </span>
                <span class="ranking" v-if="uni.qs_ranking">
                  QS {{ uni.qs_ranking }}
                </span>
              </div>
              <div class="tags">
                <el-tag :type="getDifficultyType(uni.difficulty)" size="small">
                  {{ getDifficultyText(uni.difficulty) }}
                </el-tag>
              </div>
            </div>
          </el-col>
        </el-row>
        
        <div class="pagination-wrapper">
          <el-pagination
            v-model:current-page="currentPage"
            v-model:page-size="pageSize"
            :total="total"
            :page-sizes="[12, 24, 48]"
            layout="total, sizes, prev, pager, next"
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
import { ref, reactive, onMounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useUserStore } from '@/stores/user'
import NavBar from '@/components/common/NavBar.vue'
import Footer from '@/components/common/Footer.vue'
import { getUniversities, getUniversitiesCount, addCollection, removeCollection, getCollections, checkCollection } from '@/utils/api'
import { getLogoGradient } from '@/utils/logoHelper'
import { ElMessage } from 'element-plus'

const router = useRouter()
const route = useRoute()
const userStore = useUserStore()

const universities = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(12)
const sortBy = ref('ranking')
const collections = ref([])
const loadedLogos = new Set()

const filters = reactive({
  country: route.query.country || '',
  difficulty: '',
  ranking: '',
  keyword: route.query.keyword || ''
})

const getDifficultyText = (difficulty) => {
  const map = { low: '容易', medium: '中等', high: '困难' }
  return map[difficulty] || difficulty
}

const getDifficultyType = (difficulty) => {
  const map = { low: 'success', medium: 'warning', high: 'danger' }
  return map[difficulty] || 'info'
}

const isCollected = (id) => {
  return collections.value.some(c => c.collection_type === 'university' && c.target_id === id)
}

const fetchUniversities = async () => {
  try {
    const params = {
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value,
      sort_by: sortBy.value,
      ...filters
    }
    if (filters.ranking) {
      params.max_ranking = parseInt(filters.ranking)
    }
    const countParams = {}
    if (filters.country) countParams.country = filters.country
    if (filters.difficulty) countParams.difficulty = filters.difficulty
    if (filters.ranking) countParams.max_ranking = parseInt(filters.ranking)
    if (filters.keyword) countParams.keyword = filters.keyword
    const [res, countRes] = await Promise.all([
      getUniversities(params),
      getUniversitiesCount(countParams)
    ])
    universities.value = (res || []).map(u => ({
      ...u,
      _logoLoaded: loadedLogos.has(u.logo_url)
    }))
    total.value = countRes.total
  } catch (error) {
    console.error('获取院校列表失败:', error)
  }
}

const fetchCollections = async () => {
  if (!userStore.isAuthenticated) return
  try {
    const res = await getCollections()
    collections.value = res.filter(c => c.collection_type === 'university')
  } catch (error) {
    console.error('获取收藏失败:', error)
  }
}

const handleFilterChange = () => {
  currentPage.value = 1
  fetchUniversities()
}

const handleSortChange = () => {
  fetchUniversities()
}

const handleSizeChange = (size) => {
  pageSize.value = size
  fetchUniversities()
}

const handlePageChange = (page) => {
  currentPage.value = page
  fetchUniversities()
}

const goToDetail = (id) => {
  router.push(`/universities/${id}`)
}

const toggleCollect = async (id) => {
  if (!userStore.isAuthenticated) {
    ElMessage.warning('请先登录')
    router.push('/login')
    return
  }
  
  try {
    if (isCollected(id)) {
      const collection = collections.value.find(c => c.collection_type === 'university' && c.target_id === id)
      if (collection) {
        await removeCollection(collection.id)
        ElMessage.success('已取消收藏')
      }
    } else {
      await addCollection({ collection_type: 'university', target_id: id })
      ElMessage.success('收藏成功')
    }
    fetchCollections()
  } catch (error) {
    console.error('操作失败:', error)
  }
}

watch(() => route.query, (query) => {
  filters.country = query.country || ''
  filters.keyword = query.keyword || ''
  fetchUniversities()
})

onMounted(() => {
  fetchUniversities()
  fetchCollections()
})
</script>

<style lang="scss" scoped>
.university-list-page {
  padding-top: 70px;
  min-height: 100vh;
  background: #f5f7fa;
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

.filter-section {
  background: white;
  padding: 24px;
  margin: 24px 0;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.filter-row {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
  align-items: flex-end;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
  
  label {
    font-size: 13px;
    color: $text-secondary;
    font-weight: 500;
  }
  
  &.search-group {
    flex: 1;
    min-width: 200px;
  }
}

.content-section {
  padding-bottom: 60px;
}

.results-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  
  p {
    color: $text-secondary;
    
    strong {
      color: $text-primary;
    }
  }
}

.university-card {
  background: white;
  border-radius: 12px;
  padding: 28px;
  margin-bottom: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  transition: all 0.3s;
  cursor: pointer;
  min-height: 220px;
  display: flex;
  flex-direction: column;
  
  &:hover {
    transform: translateY(-4px);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
  }
  
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 20px;
    
    .uni-logo-wrapper {
      width: 72px;
      height: 72px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      overflow: hidden;
      flex-shrink: 0;
    }
    
    .uni-logo-img {
      width: 100%;
      height: 100%;
      object-fit: contain;
      padding: 4px;
    }
    
    .uni-logo-text {
      font-size: 32px;
      font-weight: 700;
      color: white;
      line-height: 1;
    }
    
    .collect-btn {
      opacity: 0;
      transition: opacity 0.3s;
    }
  }
  
  &:hover .collect-btn {
    opacity: 1;
  }
  
  h3 {
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 6px;
    color: $text-primary;
  }
  
  .name-en {
    font-size: 13px;
    color: $text-muted;
    margin-bottom: 16px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
  }
  
  .info-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 14px;
    margin-top: auto;
    
    .country {
      display: flex;
      align-items: center;
      gap: 4px;
      font-size: 14px;
      color: $text-secondary;
    }
    
    .ranking {
      font-size: 14px;
      color: $primary-color;
      font-weight: 600;
    }
  }
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 40px;
}
</style>

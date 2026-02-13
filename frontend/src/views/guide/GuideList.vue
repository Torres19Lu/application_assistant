<template>
  <div class="guide-list-page">
    <NavBar />
    
    <div class="page-header">
      <div class="container">
        <h1>申请攻略</h1>
        <p>全面的留学申请指南，助你成功拿到offer</p>
      </div>
    </div>

    <div class="page-content">
    
    <div class="filter-section">
      <el-row :gutter="20">
        <el-col :span="8">
          <el-input
            v-model="searchQuery"
            placeholder="搜索攻略..."
            clearable
            @keyup.enter="handleSearch"
          >
            <template #append>
              <el-button @click="handleSearch">
                <el-icon><Search /></el-icon>
              </el-button>
            </template>
          </el-input>
        </el-col>
        <el-col :span="8">
          <el-select v-model="selectedCategory" placeholder="选择分类" clearable @change="handleSearch">
            <el-option
              v-for="cat in categories"
              :key="cat.value"
              :label="cat.label"
              :value="cat.value"
            />
          </el-select>
        </el-col>
      </el-row>
    </div>
    
    <div class="guide-list">
      <el-row :gutter="20">
        <el-col :span="8" v-for="guide in guides" :key="guide.id">
          <el-card class="guide-card" shadow="hover" @click="goToDetail(guide.id)">
            <div class="guide-cover" :style="{ background: getCoverGradient(guide.category) }">
              <div class="guide-cover-icon">{{ getCoverIcon(guide.category) }}</div>
              <div class="guide-category">{{ guide.category }}</div>
            </div>
            <div class="guide-content">
              <h3 class="guide-title">{{ guide.title }}</h3>
              <p class="guide-summary">{{ guide.summary }}</p>
              <div class="guide-meta">
                <span class="author">
                  <el-icon><User /></el-icon>
                  {{ guide.author_name || '匿名' }}
                </span>
                <span class="date">
                  <el-icon><Calendar /></el-icon>
                  {{ formatDate(guide.created_at) }}
                </span>
                <span class="views">
                  <el-icon><View /></el-icon>
                  {{ guide.views || 0 }}
                </span>
              </div>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
    
    <div class="pagination">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[9, 18, 27]"
        layout="total, sizes, prev, pager, next"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
    </div>
    
    <Footer />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Search, User, Calendar, View } from '@element-plus/icons-vue'
import { getGuides, getGuidesCount } from '@/utils/api'
import NavBar from '@/components/common/NavBar.vue'
import Footer from '@/components/common/Footer.vue'

const router = useRouter()
const guides = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(9)
const searchQuery = ref('')
const selectedCategory = ref('')

const categories = [
  { label: '申请规划', value: '申请规划' },
  { label: '文书写作', value: '文书写作' },
  { label: '考试准备', value: '考试准备' },
  { label: '面试准备', value: '面试准备' },
  { label: '签证办理', value: '签证办理' },
  { label: '留学生活', value: '留学生活' }
]

const fetchGuides = async () => {
  try {
    const params = {
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value,
      keyword: searchQuery.value,
      category: selectedCategory.value
    }
    const countParams = {}
    if (searchQuery.value) countParams.keyword = searchQuery.value
    if (selectedCategory.value) countParams.category = selectedCategory.value
    const [response, countRes] = await Promise.all([
      getGuides(params),
      getGuidesCount(countParams)
    ])
    // Axios interceptor 已经 unwrap response.data，后端直接返回数组
    guides.value = Array.isArray(response) ? response : []
    total.value = countRes.total
  } catch (error) {
    ElMessage.error('获取攻略列表失败')
  }
}

const handleSearch = () => {
  currentPage.value = 1
  fetchGuides()
}

const handleSizeChange = (val) => {
  pageSize.value = val
  fetchGuides()
}

const handleCurrentChange = (val) => {
  currentPage.value = val
  fetchGuides()
}

const goToDetail = (id) => {
  router.push(`/guides/${id}`)
}

const formatDate = (date) => {
  return new Date(date).toLocaleDateString('zh-CN')
}

const getCoverGradient = (category) => {
  const gradients = {
    '申请规划': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    '文书写作': 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
    '考试准备': 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
    '面试准备': 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
    '签证办理': 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
    '留学生活': 'linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%)'
  }
  return gradients[category] || 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
}

const getCoverIcon = (category) => {
  const icons = {
    '申请规划': '📋',
    '文书写作': '✍️',
    '考试准备': '📚',
    '面试准备': '🎤',
    '签证办理': '🛂',
    '留学生活': '🌍'
  }
  return icons[category] || '📖'
}

onMounted(() => {
  fetchGuides()
})
</script>

<style scoped lang="scss">
.guide-list-page {
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

.page-content {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.filter-section {
  margin-bottom: 30px;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
}

.guide-list {
  margin-bottom: 30px;
}

.guide-card {
  margin-bottom: 20px;
  cursor: pointer;
  transition: transform 0.3s;
  
  &:hover {
    transform: translateY(-5px);
  }
  
  .guide-cover {
    position: relative;
    height: 160px;
    overflow: hidden;
    border-radius: 4px;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    
    .guide-cover-icon {
      font-size: 56px;
      opacity: 0.5;
    }
    
    .guide-category {
      position: absolute;
      top: 8px;
      left: 8px;
      background: rgba(255, 255, 255, 0.25);
      backdrop-filter: blur(4px);
      color: white;
      padding: 4px 12px;
      border-radius: 20px;
      font-size: 12px;
      font-weight: 500;
    }
  }
  
  .guide-content {
    .guide-title {
      font-size: 16px;
      color: #303133;
      margin-bottom: 8px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
    
    .guide-summary {
      font-size: 14px;
      color: #606266;
      margin-bottom: 12px;
      overflow: hidden;
      text-overflow: ellipsis;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
    }
    
    .guide-meta {
      display: flex;
      gap: 16px;
      font-size: 12px;
      color: #909399;
      
      span {
        display: flex;
        align-items: center;
        gap: 4px;
      }
    }
  }
}

.pagination {
  display: flex;
  justify-content: center;
}
</style>

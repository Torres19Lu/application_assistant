<template>
  <div class="university-detail-page" v-if="university">
    <NavBar />
    
    <!-- 返回按钮 -->
    <div class="back-nav">
      <div class="container">
        <el-button link @click="goBack">
          <el-icon><ArrowLeft /></el-icon>
          返回院校列表
        </el-button>
      </div>
    </div>
    
    <div class="university-header">
      <div class="container">
        <div class="header-content">
          <div class="university-logo" :style="{ background: !logoLoaded ? getLogoGradient(university.country) : 'white' }">
            <img
              v-if="university.logo_url"
              :src="university.logo_url"
              :alt="university.name"
              class="logo-img"
              @load="logoLoaded = true"
              @error="university.logo_url = ''"
            />
            <span v-if="!university.logo_url" class="logo-text">{{ university.name.charAt(0) }}</span>
          </div>
          <div class="university-info">
            <h1>{{ university.name }}</h1>
            <p class="name-en">{{ university.name_en }}</p>
            <div class="meta-info">
              <span class="location">
                <el-icon><Location /></el-icon>
                {{ university.country }} · {{ university.location }}
              </span>
              <span class="ranking" v-if="university.qs_ranking">
                <el-icon><Trophy /></el-icon>
                QS排名: {{ university.qs_ranking }}
              </span>
            </div>
            <div class="actions">
              <el-button
                v-if="userStore.isAuthenticated"
                :type="isCollected ? 'primary' : 'default'"
                @click="toggleCollect"
              >
                <el-icon><Star /></el-icon>
                {{ isCollected ? '已收藏' : '收藏' }}
              </el-button>
              <el-button v-else @click="$router.push('/login')">
                <el-icon><Star /></el-icon>
                登录后收藏
              </el-button>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <div class="container">
      <div class="content-layout">
        <div class="main-content">
          <el-tabs v-model="activeTab">
            <el-tab-pane label="院校概况" name="overview">
              <div class="section">
                <h2>院校介绍</h2>
                <p class="description">{{ university.description || '暂无介绍' }}</p>
              </div>
              
              <div class="section" v-if="university.application_requirements">
                <h2>申请要求</h2>
                <p class="description">{{ university.application_requirements }}</p>
              </div>
            </el-tab-pane>
            
            <el-tab-pane label="专业列表" name="majors">
              <div class="majors-filter">
                <el-select v-model="majorCategory" placeholder="全部分类" clearable>
                  <el-option label="工科" value="工科" />
                  <el-option label="商科" value="商科" />
                  <el-option label="文科" value="文科" />
                  <el-option label="理科" value="理科" />
                </el-select>
              </div>
              
              <el-row :gutter="20">
                <el-col :span="12" v-for="major in filteredMajors" :key="major.id">
                  <div class="major-card" @click="goToMajor(major.id)">
                    <h4>{{ major.name }}</h4>
                    <p class="category">{{ major.category }}</p>
                    <div class="major-info">
                      <span v-if="major.duration">
                        <el-icon><Timer /></el-icon>
                        {{ major.duration }}
                      </span>
                      <span v-if="major.tuition">
                        <el-icon><Money /></el-icon>
                        {{ major.tuition }}
                      </span>
                    </div>
                  </div>
                </el-col>
              </el-row>
            </el-tab-pane>
          </el-tabs>
        </div>
        
        <div class="sidebar">
          <div class="info-card">
            <h3>基本信息</h3>
            <div class="info-item">
              <span class="label">学费范围</span>
              <span class="value">{{ university.tuition_range || '暂无数据' }}</span>
            </div>
            <div class="info-item">
              <span class="label">申请难度</span>
              <el-tag :type="getDifficultyType(university.difficulty)">
                {{ getDifficultyText(university.difficulty) }}
              </el-tag>
            </div>
            <div class="info-item" v-if="university.website">
              <span class="label">官方网站</span>
              <a :href="university.website" target="_blank" class="website-link">
                访问官网 <el-icon><Link /></el-icon>
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
    
    <Footer />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import NavBar from '@/components/common/NavBar.vue'
import Footer from '@/components/common/Footer.vue'
import { getUniversity, getMajors, addCollection, removeCollection, getCollections, checkCollection } from '@/utils/api'
import { getLogoGradient } from '@/utils/logoHelper'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

const university = ref(null)
const majors = ref([])
const activeTab = ref('overview')
const majorCategory = ref('')
const isCollected = ref(false)
const collectionId = ref(null)
const logoLoaded = ref(false)

const filteredMajors = computed(() => {
  if (!majorCategory.value) return majors.value
  return majors.value.filter(m => m.category === majorCategory.value)
})

const getDifficultyText = (difficulty) => {
  const map = { low: '容易', medium: '中等', high: '困难' }
  return map[difficulty] || difficulty
}

const getDifficultyType = (difficulty) => {
  const map = { low: 'success', medium: 'warning', high: 'danger' }
  return map[difficulty] || 'info'
}

const goBack = () => {
  router.push('/universities')
}

const fetchUniversity = async () => {
  try {
    const id = route.params.id
    const res = await getUniversity(id)
    university.value = res
  } catch (error) {
    console.error('获取院校详情失败:', error)
    ElMessage.error('获取院校信息失败')
  }
}

const fetchMajors = async () => {
  try {
    const id = route.params.id
    const res = await getMajors({ university_id: id })
    majors.value = Array.isArray(res) ? res : []
  } catch (error) {
    console.error('获取专业列表失败:', error)
  }
}

const checkIfCollected = async () => {
  if (!userStore.isAuthenticated) return
  try {
    const res = await checkCollection('university', parseInt(route.params.id))
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
        collection_type: 'university',
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

const goToMajor = (id) => {
  router.push(`/majors/${id}`)
}

onMounted(() => {
  fetchUniversity()
  fetchMajors()
  checkIfCollected()
})
</script>

<style lang="scss" scoped>
.university-detail-page {
  padding-top: 70px;
  min-height: 100vh;
  background: #f5f7fa;
}

.back-nav {
  background: white;
  border-bottom: 1px solid #e5e7eb;
  padding: 12px 0;
  
  .el-button {
    font-size: 14px;
    color: #6b7280;
    
    &:hover {
      color: #1e40af;
    }
  }
}

.university-header {
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
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  
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

.university-info {
  flex: 1;
  
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
    }
  }
}

.content-layout {
  display: grid;
  grid-template-columns: 1fr 320px;
  gap: 24px;
  padding: 40px 0;
}

.main-content {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  
  .section {
    margin-bottom: 32px;
    
    h2 {
      font-size: 20px;
      font-weight: 600;
      margin-bottom: 16px;
      color: $text-primary;
    }
    
    .description {
      color: $text-secondary;
      line-height: 1.8;
    }
  }
}

.majors-filter {
  margin-bottom: 20px;
}

.major-card {
  background: #f9fafb;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 16px;
  cursor: pointer;
  transition: all 0.3s;
  
  &:hover {
    background: #f3f4f6;
    transform: translateX(4px);
  }
  
  h4 {
    font-size: 15px;
    font-weight: 600;
    margin-bottom: 4px;
    color: $text-primary;
  }
  
  .category {
    font-size: 13px;
    color: $text-muted;
    margin-bottom: 8px;
  }
  
  .major-info {
    display: flex;
    gap: 16px;
    
    span {
      display: flex;
      align-items: center;
      gap: 4px;
      font-size: 13px;
      color: $text-secondary;
    }
  }
}

.sidebar {
  .info-card {
    background: white;
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
    
    h3 {
      font-size: 18px;
      font-weight: 600;
      margin-bottom: 20px;
      color: $text-primary;
    }
    
    .info-item {
      display: flex;
      justify-content: space-between;
      align-items: center;
      padding: 12px 0;
      border-bottom: 1px solid #e5e7eb;
      
      &:last-child {
        border-bottom: none;
      }
      
      .label {
        color: $text-secondary;
        font-size: 14px;
      }
      
      .value {
        color: $text-primary;
        font-weight: 500;
      }
      
      .website-link {
        color: $primary-color;
        text-decoration: none;
        display: flex;
        align-items: center;
        gap: 4px;
        font-size: 14px;
        
        &:hover {
          text-decoration: underline;
        }
      }
    }
  }
}

@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    text-align: center;
  }
  
  .content-layout {
    grid-template-columns: 1fr;
  }
}
</style>

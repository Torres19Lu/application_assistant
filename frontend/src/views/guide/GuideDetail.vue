<template>
  <div class="guide-detail-page">
    <NavBar />
    
    <div class="page-content">
    <el-card class="guide-card" v-loading="loading">
      <div class="guide-header">
        <el-breadcrumb separator="/">
          <el-breadcrumb-item :to="{ path: '/guides' }">申请攻略</el-breadcrumb-item>
          <el-breadcrumb-item>{{ guide.title }}</el-breadcrumb-item>
        </el-breadcrumb>
        
        <h1 class="guide-title">{{ guide.title }}</h1>
        
        <div class="guide-meta">
          <span class="category">
            <el-tag>{{ guide.category }}</el-tag>
          </span>
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
            {{ guide.views || 0 }} 阅读
          </span>
        </div>
      </div>
      
      <div class="guide-cover-banner" :style="{ background: getCoverGradient(guide.category) }">
        <span class="cover-icon">{{ getCoverIcon(guide.category) }}</span>
        <span class="cover-category">{{ guide.category }}</span>
      </div>
      
      <div class="guide-content" v-html="guide.content"></div>
      
      <div class="guide-footer">
        <el-divider />
        <div class="actions">
          <el-button type="primary" size="large" @click="handleLike">
            <el-icon><Star /></el-icon>
            点赞 ({{ guide.likes || 0 }})
          </el-button>
          <el-button size="large" @click="shareGuide">
            <el-icon><Share /></el-icon>
            分享攻略
          </el-button>
          <el-button size="large" @click="goBack">
            <el-icon><Back /></el-icon>
            返回列表
          </el-button>
        </div>
      </div>
    </el-card>
    </div>
    
    <Footer />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Calendar, View, Share, Back, Star } from '@element-plus/icons-vue'
import { getGuide, likeGuide } from '@/utils/api'
import NavBar from '@/components/common/NavBar.vue'
import Footer from '@/components/common/Footer.vue'

const route = useRoute()
const router = useRouter()
const guide = ref({})
const loading = ref(false)

const fetchGuideDetail = async () => {
  loading.value = true
  try {
    const response = await getGuide(route.params.id)
    guide.value = response
  } catch (error) {
    ElMessage.error('获取攻略详情失败')
  } finally {
    loading.value = false
  }
}

const formatDate = (date) => {
  if (!date) return ''
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

const handleLike = async () => {
  try {
    const res = await likeGuide(route.params.id)
    guide.value.likes = res.likes
    ElMessage.success('点赞成功')
  } catch (error) {
    console.error('点赞失败:', error)
  }
}

const shareGuide = () => {
  if (navigator.share) {
    navigator.share({
      title: guide.value.title,
      text: guide.value.summary,
      url: window.location.href
    })
  } else {
    navigator.clipboard.writeText(window.location.href)
    ElMessage.success('链接已复制到剪贴板')
  }
}

const goBack = () => {
  router.push('/guides')
}

onMounted(() => {
  fetchGuideDetail()
})
</script>

<style scoped lang="scss">
.guide-detail-page {
  min-height: 100vh;
  background: #f5f7fa;
  padding-top: 70px;
}

.page-content {
  max-width: 900px;
  margin: 0 auto;
  padding: 20px;
}

.guide-card {
  .guide-header {
    margin-bottom: 24px;
    
    .el-breadcrumb {
      margin-bottom: 16px;
    }
    
    .guide-title {
      font-size: 28px;
      color: #303133;
      margin-bottom: 16px;
      line-height: 1.4;
    }
    
    .guide-meta {
      display: flex;
      align-items: center;
      gap: 20px;
      color: #909399;
      font-size: 14px;
      
      span {
        display: flex;
        align-items: center;
        gap: 6px;
      }
    }
  }
  
  .guide-cover-banner {
    margin-bottom: 24px;
    border-radius: 12px;
    height: 120px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 12px;
    
    .cover-icon {
      font-size: 48px;
      opacity: 0.6;
    }
    
    .cover-category {
      font-size: 20px;
      font-weight: 600;
      color: white;
      opacity: 0.9;
    }
  }
  
  .guide-content {
    font-size: 16px;
    line-height: 1.8;
    color: #303133;
    
    h2, h3 {
      color: #303133;
      margin: 24px 0 16px;
    }
    
    p {
      margin-bottom: 16px;
    }
    
    ul, ol {
      margin-bottom: 16px;
      padding-left: 24px;
    }
    
    li {
      margin-bottom: 8px;
    }
  }
  
  .guide-footer {
    margin-top: 40px;
    
    .actions {
      display: flex;
      justify-content: center;
      gap: 16px;
    }
  }
}
</style>

<template>
  <div class="favorites-page">
    <NavBar />
    
    <div class="page-header">
      <div class="container">
        <h1>我的收藏</h1>
        <p>管理您收藏的院校和专业</p>
      </div>
    </div>

    <div class="container">
      
      <el-tabs v-model="activeTab" class="favorites-tabs">
        <el-tab-pane label="院校收藏" name="universities">
          <div class="favorites-grid" v-if="universityCollections.length > 0">
            <div 
              class="favorite-card" 
              v-for="item in universityCollections" 
              :key="item.id"
              @click="goToUniversity(item.target_id)"
            >
              <img :src="item.target?.logo_url || '/default-uni.png'" class="item-logo" />
              <div class="item-info">
                <h4>{{ item.target?.name }}</h4>
                <p>{{ item.target?.country }}</p>
              </div>
              <el-button 
                type="danger" 
                size="small" 
                circle
                @click.stop="removeFavorite(item.id)"
              >
                <el-icon><Delete /></el-icon>
              </el-button>
            </div>
          </div>
          <el-empty v-else description="暂无收藏的院校" />
        </el-tab-pane>
        
        <el-tab-pane label="专业收藏" name="majors">
          <div class="favorites-grid" v-if="majorCollections.length > 0">
            <div 
              class="favorite-card" 
              v-for="item in majorCollections" 
              :key="item.id"
              @click="goToMajor(item.target_id)"
            >
              <div class="item-info">
                <h4>{{ item.target?.name }}</h4>
                <p>{{ item.target?.university_name }}</p>
              </div>
              <el-button 
                type="danger" 
                size="small" 
                circle
                @click.stop="removeFavorite(item.id)"
              >
                <el-icon><Delete /></el-icon>
              </el-button>
            </div>
          </div>
          <el-empty v-else description="暂无收藏的专业" />
        </el-tab-pane>
      </el-tabs>
    </div>
    
    <Footer />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import NavBar from '@/components/common/NavBar.vue'
import Footer from '@/components/common/Footer.vue'
import { getCollections, removeCollection } from '@/utils/api'
import { ElMessage } from 'element-plus'

const router = useRouter()
const activeTab = ref('universities')
const collections = ref([])

const universityCollections = computed(() => {
  return collections.value.filter(c => c.collection_type === 'university')
})

const majorCollections = computed(() => {
  return collections.value.filter(c => c.collection_type === 'major')
})

const fetchCollections = async () => {
  try {
    const res = await getCollections()
    collections.value = res
  } catch (error) {
    console.error('获取收藏失败:', error)
  }
}

const removeFavorite = async (id) => {
  try {
    await removeCollection(id)
    ElMessage.success('已取消收藏')
    fetchCollections()
  } catch (error) {
    console.error('取消收藏失败:', error)
  }
}

const goToUniversity = (id) => {
  router.push(`/universities/${id}`)
}

const goToMajor = (id) => {
  router.push(`/majors/${id}`)
}

onMounted(() => {
  fetchCollections()
})
</script>

<style lang="scss" scoped>
.favorites-page {
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

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.favorites-tabs {
  background: white;
  padding: 24px;
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  margin-bottom: 40px;
}

.favorites-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  padding: 20px 0;
}

.favorite-card {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  background: #f9fafb;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
  
  &:hover {
    background: #f3f4f6;
  }
  
  .item-logo {
    width: 48px;
    height: 48px;
    object-fit: contain;
    border-radius: 8px;
    background: white;
  }
  
  .item-info {
    flex: 1;
    
    h4 {
      font-size: 15px;
      font-weight: 600;
      margin-bottom: 4px;
      color: $text-primary;
    }
    
    p {
      font-size: 13px;
      color: $text-secondary;
    }
  }
}
</style>

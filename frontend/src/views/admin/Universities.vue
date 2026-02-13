<template>
  <div class="admin-page">
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
          <h2>院校管理</h2>
          <el-button type="primary" @click="showAddDialog">
            <el-icon><Plus /></el-icon>
            添加院校
          </el-button>
        </el-header>
        
        <el-main>
          <el-table :data="universities" v-loading="loading" border>
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column label="Logo" width="80">
              <template #default="{ row }">
                <div class="logo-cell">
                  <img v-if="row.logo_url && !row._logoError" :src="row.logo_url" class="table-logo" @error="row._logoError = true" />
                  <div v-else class="table-logo-placeholder">
                    {{ (row.name || '?').charAt(0) }}
                  </div>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="name" label="院校名称" min-width="150" />
            <el-table-column prop="country" label="国家" width="100" />
            <el-table-column prop="qs_ranking" label="QS排名" width="100" />
            <el-table-column prop="difficulty" label="难度" width="100">
              <template #default="{ row }">
                <el-tag :type="getDifficultyType(row.difficulty)">
                  {{ getDifficultyText(row.difficulty) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="150" fixed="right">
              <template #default="{ row }">
                <el-button type="primary" size="small" @click="showEditDialog(row)">
                  <el-icon><Edit /></el-icon>
                </el-button>
                <el-button type="danger" size="small" @click="handleDelete(row)">
                  <el-icon><Delete /></el-icon>
                </el-button>
              </template>
            </el-table-column>
          </el-table>
          
          <div class="pagination-wrapper">
            <el-pagination
              v-model:current-page="currentPage"
              v-model:page-size="pageSize"
              :total="total"
              layout="total, prev, pager, next"
              @current-change="fetchUniversities"
            />
          </div>
        </el-main>
      </el-container>
    </el-container>
    
    <!-- Add/Edit Dialog -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑院校' : '添加院校'"
      width="700px"
    >
      <el-form :model="form" :rules="rules" ref="formRef" label-width="100px">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="院校名称" prop="name">
              <el-input v-model="form.name" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="英文名称" prop="name_en">
              <el-input v-model="form.name_en" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="国家" prop="country">
              <el-select v-model="form.country" style="width: 100%">
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
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="地区" prop="region">
              <el-input v-model="form.region" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="QS排名" prop="qs_ranking">
              <el-input-number v-model="form.qs_ranking" :min="1" style="width: 100%" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="USNews排名" prop="us_news_ranking">
              <el-input-number v-model="form.us_news_ranking" :min="1" style="width: 100%" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="申请难度" prop="difficulty">
              <el-select v-model="form.difficulty" style="width: 100%">
                <el-option label="容易" value="low" />
                <el-option label="中等" value="medium" />
                <el-option label="困难" value="high" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="学费范围" prop="tuition_range">
              <el-input v-model="form.tuition_range" placeholder="如：$30,000-50,000/年" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="Logo URL" prop="logo_url">
          <el-input v-model="form.logo_url" placeholder="院校Logo图片地址" />
        </el-form-item>

        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="所在地" prop="location">
              <el-input v-model="form.location" placeholder="如：Cambridge, MA" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="官网" prop="website">
              <el-input v-model="form.website" placeholder="https://..." />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="院校介绍" prop="description">
          <el-input v-model="form.description" type="textarea" :rows="4" />
        </el-form-item>
        
        <el-form-item label="申请要求" prop="application_requirements">
          <el-input v-model="form.application_requirements" type="textarea" :rows="3" />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">
          确定
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Edit, Delete, School, DataLine, Reading, Document, User, HomeFilled, FolderOpened } from '@element-plus/icons-vue'
import { getUniversities, getUniversitiesCount, createUniversity, updateUniversity, deleteUniversity } from '@/utils/api'

const universities = ref([])
const loading = ref(false)
const currentPage = ref(1)
const pageSize = ref(20)
const total = ref(0)
const dialogVisible = ref(false)
const isEdit = ref(false)
const submitting = ref(false)
const formRef = ref(null)

const form = reactive({
  name: '',
  name_en: '',
  country: '',
  region: '',
  qs_ranking: null,
  us_news_ranking: null,
  difficulty: 'medium',
  tuition_range: '',
  logo_url: '',
  location: '',
  website: '',
  description: '',
  application_requirements: ''
})

const rules = {
  name: [{ required: true, message: '请输入院校名称', trigger: 'blur' }],
  country: [{ required: true, message: '请选择国家', trigger: 'change' }]
}

const getDifficultyText = (difficulty) => {
  const map = { low: '容易', medium: '中等', high: '困难' }
  return map[difficulty] || difficulty
}

const getDifficultyType = (difficulty) => {
  const map = { low: 'success', medium: 'warning', high: 'danger' }
  return map[difficulty] || 'info'
}

const fetchUniversities = async () => {
  loading.value = true
  try {
    const res = await getUniversities({
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value
    })
    universities.value = Array.isArray(res) ? res : []
    // 获取总数
    const countRes = await getUniversitiesCount()
    total.value = countRes.total || universities.value.length
  } catch (error) {
    console.error('获取院校列表失败:', error)
    ElMessage.error('获取院校列表失败')
  } finally {
    loading.value = false
  }
}

const showAddDialog = () => {
  isEdit.value = false
  Object.keys(form).forEach(key => {
    form[key] = key === 'difficulty' ? 'medium' : ''
  })
  dialogVisible.value = true
}

const showEditDialog = (row) => {
  isEdit.value = true
  Object.assign(form, row)
  dialogVisible.value = true
}

const handleSubmit = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return
  
  submitting.value = true
  try {
    if (isEdit.value) {
      await updateUniversity(form.id, form)
      ElMessage.success('更新成功')
    } else {
      await createUniversity(form)
      ElMessage.success('添加成功')
    }
    dialogVisible.value = false
    fetchUniversities()
  } catch (error) {
    console.error('提交失败:', error)
  } finally {
    submitting.value = false
  }
}

const handleDelete = (row) => {
  ElMessageBox.confirm('确定要删除该院校吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(async () => {
    try {
      await deleteUniversity(row.id)
      ElMessage.success('删除成功')
      fetchUniversities()
    } catch (error) {
      console.error('删除失败:', error)
    }
  })
}

onMounted(() => {
  fetchUniversities()
})
</script>

<style lang="scss" scoped>
.admin-page {
  min-height: 100vh;
}

.sidebar {
  background: #1f2937;
  min-height: 100vh;
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  
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
  justify-content: space-between;
  
  h2 {
    margin: 0;
    color: $text-primary;
  }
}

.el-main {
  background: #f5f7fa;
  margin-left: 220px;
}

.table-logo {
  width: 40px;
  height: 40px;
  object-fit: contain;
}

.table-logo-placeholder {
  width: 40px;
  height: 40px;
  border-radius: 8px;
  background: linear-gradient(135deg, #1e40af, #3b82f6);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  font-weight: 700;
}

.pagination-wrapper {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>

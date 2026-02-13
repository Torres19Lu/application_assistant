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
          <h2>攻略管理</h2>
          <el-button type="primary" @click="showAddDialog">
            <el-icon><Plus /></el-icon>
            添加攻略
          </el-button>
        </el-header>
        
        <el-main>
    <el-card>
      <el-table :data="guides" v-loading="loading" border>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="title" label="标题" min-width="200" />
        <el-table-column prop="category" label="分类" width="120">
          <template #default="{ row }">
            <el-tag>{{ row.category }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="author_name" label="作者" width="120" />
        <el-table-column prop="views" label="阅读量" width="100" />
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" @click="editGuide(row)">
              编辑
            </el-button>
            <el-button type="danger" size="small" @click="deleteGuide(row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <div class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          layout="total, prev, pager, next"
          @current-change="fetchGuides"
        />
      </div>
    </el-card>
    
    <!-- 添加/编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑攻略' : '添加攻略'"
      width="800px"
    >
      <el-form :model="form" label-width="100px" :rules="rules" ref="formRef">
        <el-form-item label="标题" prop="title">
          <el-input v-model="form.title" />
        </el-form-item>
        <el-form-item label="分类" prop="category">
          <el-select v-model="form.category" style="width: 100%">
            <el-option label="申请规划" value="申请规划" />
            <el-option label="文书写作" value="文书写作" />
            <el-option label="考试准备" value="考试准备" />
            <el-option label="面试准备" value="面试准备" />
            <el-option label="签证办理" value="签证办理" />
            <el-option label="留学生活" value="留学生活" />
          </el-select>
        </el-form-item>
        <el-form-item label="摘要" prop="summary">
          <el-input v-model="form.summary" type="textarea" :rows="3" />
        </el-form-item>
        <el-form-item label="内容" prop="content">
          <el-input v-model="form.content" type="textarea" :rows="10" />
        </el-form-item>
        <el-form-item label="封面图片" prop="cover_image">
          <el-input v-model="form.cover_image" placeholder="图片URL" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitForm">确定</el-button>
      </template>
    </el-dialog>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, School, DataLine, Reading, Document, User, HomeFilled, FolderOpened } from '@element-plus/icons-vue'
import { getGuides, getGuidesCount, createGuide, updateGuide, deleteGuide as deleteGuideApi } from '@/utils/api'

const loading = ref(false)
const guides = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref(null)

const form = ref({
  title: '',
  category: '申请规划',
  summary: '',
  content: '',
  cover_image: ''
})

const rules = {
  title: [{ required: true, message: '请输入标题', trigger: 'blur' }],
  category: [{ required: true, message: '请选择分类', trigger: 'change' }],
  content: [{ required: true, message: '请输入内容', trigger: 'blur' }]
}

const fetchGuides = async () => {
  loading.value = true
  try {
    const response = await getGuides({
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value
    })
    guides.value = Array.isArray(response) ? response : []
    // 获取总数
    const countRes = await getGuidesCount()
    total.value = countRes.total || guides.value.length
  } catch (error) {
    ElMessage.error('获取攻略列表失败')
  } finally {
    loading.value = false
  }
}

const showAddDialog = () => {
  isEdit.value = false
  form.value = {
    title: '',
    category: '申请规划',
    summary: '',
    content: '',
    cover_image: ''
  }
  dialogVisible.value = true
}

const editGuide = (row) => {
  isEdit.value = true
  form.value = { ...row }
  dialogVisible.value = true
}

const deleteGuide = (row) => {
  ElMessageBox.confirm('确定要删除这篇攻略吗？', '提示', {
    type: 'warning'
  }).then(async () => {
    try {
      await deleteGuideApi(row.id)
      ElMessage.success('删除成功')
      fetchGuides()
    } catch (error) {
      ElMessage.error('删除失败')
    }
  })
}

const submitForm = async () => {
  formRef.value.validate(async (valid) => {
    if (valid) {
      try {
        if (isEdit.value) {
          await updateGuide(form.value.id, form.value)
        } else {
          await createGuide(form.value)
        }
        ElMessage.success(isEdit.value ? '更新成功' : '添加成功')
        dialogVisible.value = false
        fetchGuides()
      } catch (error) {
        ElMessage.error(isEdit.value ? '更新失败' : '添加失败')
      }
    }
  })
}

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleString('zh-CN')
}

onMounted(() => {
  fetchGuides()
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
  }
}

.el-main {
  background: #f5f7fa;
  margin-left: 220px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>

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
          <h2>专业管理</h2>
          <el-button type="primary" @click="showAddDialog">
            <el-icon><Plus /></el-icon>
            添加专业
          </el-button>
        </el-header>
        
        <el-main>
          <el-card>
            <el-table :data="majors" v-loading="loading" border>
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="name" label="专业名称" min-width="180" />
              <el-table-column label="所属院校" min-width="150">
                <template #default="{ row }">
                  {{ row.university_name || '-' }}
                </template>
              </el-table-column>
              <el-table-column prop="category" label="分类" width="120">
                <template #default="{ row }">
                  <el-tag>{{ row.category }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="duration" label="学制" width="100" />
              <el-table-column prop="tuition" label="学费" width="140" />
              <el-table-column label="语言要求" width="140">
                <template #default="{ row }">
                  <span v-if="row.ielts_requirement">IELTS {{ row.ielts_requirement }}</span>
                  <span v-else-if="row.toefl_requirement">TOEFL {{ row.toefl_requirement }}</span>
                  <span v-else>-</span>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="180" fixed="right">
                <template #default="{ row }">
                  <el-button type="primary" size="small" @click="editMajor(row)">
                    编辑
                  </el-button>
                  <el-button type="danger" size="small" @click="handleDelete(row)">
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
                @current-change="fetchMajors"
              />
            </div>
          </el-card>
    
          <!-- 添加/编辑对话框 -->
          <el-dialog
            v-model="dialogVisible"
            :title="isEdit ? '编辑专业' : '添加专业'"
            width="800px"
          >
            <el-form :model="form" label-width="100px" :rules="rules" ref="formRef">
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="专业名称" prop="name">
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
                  <el-form-item label="所属院校" prop="university_id">
                    <el-select v-model="form.university_id" filterable style="width: 100%">
                      <el-option
                        v-for="uni in universities"
                        :key="uni.id"
                        :label="uni.name"
                        :value="uni.id"
                      />
                    </el-select>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="专业分类" prop="category">
                    <el-select v-model="form.category" style="width: 100%">
                      <el-option label="工程技术" value="工程技术" />
                      <el-option label="商科管理" value="商科管理" />
                      <el-option label="计算机科学" value="计算机科学" />
                      <el-option label="人文社科" value="人文社科" />
                      <el-option label="自然科学" value="自然科学" />
                      <el-option label="医学健康" value="医学健康" />
                      <el-option label="艺术设计" value="艺术设计" />
                      <el-option label="教育学" value="教育学" />
                      <el-option label="法学" value="法学" />
                    </el-select>
                  </el-form-item>
                </el-col>
              </el-row>
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="子分类" prop="subcategory">
                    <el-input v-model="form.subcategory" placeholder="如：人工智能、金融学" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="学制" prop="duration">
                    <el-input v-model="form.duration" placeholder="如：2年" />
                  </el-form-item>
                </el-col>
              </el-row>
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="学费" prop="tuition">
                    <el-input v-model="form.tuition" placeholder="如：$50,000/年" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="GPA要求" prop="gpa_requirement">
                    <el-input-number v-model="form.gpa_requirement" :min="0" :max="4.0" :step="0.1" :precision="1" style="width: 100%" />
                  </el-form-item>
                </el-col>
              </el-row>
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="IELTS要求" prop="ielts_requirement">
                    <el-input v-model="form.ielts_requirement" placeholder="如：7.0" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="TOEFL要求" prop="toefl_requirement">
                    <el-input v-model="form.toefl_requirement" placeholder="如：100" />
                  </el-form-item>
                </el-col>
              </el-row>
              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="GRE要求" prop="gre_requirement">
                    <el-input v-model="form.gre_requirement" placeholder="如：320+" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="GMAT要求" prop="gmat_requirement">
                    <el-input v-model="form.gmat_requirement" placeholder="如：700+" />
                  </el-form-item>
                </el-col>
              </el-row>
              <el-form-item label="专业介绍" prop="description">
                <el-input v-model="form.description" type="textarea" :rows="4" />
              </el-form-item>
              <el-form-item label="课程设置" prop="curriculum">
                <el-input v-model="form.curriculum" type="textarea" :rows="3" />
              </el-form-item>
              <el-form-item label="就业前景" prop="career_prospects">
                <el-input v-model="form.career_prospects" type="textarea" :rows="3" />
              </el-form-item>
            </el-form>
            <template #footer>
              <el-button @click="dialogVisible = false">取消</el-button>
              <el-button type="primary" @click="submitForm" :loading="submitting">确定</el-button>
            </template>
          </el-dialog>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, School, DataLine, Reading, Document, User, HomeFilled, FolderOpened } from '@element-plus/icons-vue'
import { getMajors, getMajorsCount, createMajor, updateMajor, deleteMajor as deleteMajorApi, getUniversities } from '@/utils/api'

const loading = ref(false)
const submitting = ref(false)
const majors = ref([])
const universities = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const dialogVisible = ref(false)
const isEdit = ref(false)
const formRef = ref(null)

const defaultForm = {
  name: '',
  name_en: '',
  university_id: '',
  category: '',
  subcategory: '',
  duration: '',
  tuition: '',
  ielts_requirement: '',
  toefl_requirement: '',
  gpa_requirement: 0.0,
  gre_requirement: '',
  gmat_requirement: '',
  description: '',
  curriculum: '',
  career_prospects: ''
}

const form = ref({ ...defaultForm })

const rules = {
  name: [{ required: true, message: '请输入专业名称', trigger: 'blur' }],
  university_id: [{ required: true, message: '请选择所属院校', trigger: 'change' }],
  category: [{ required: true, message: '请选择专业分类', trigger: 'change' }]
}

const fetchMajors = async () => {
  loading.value = true
  try {
    const response = await getMajors({
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value
    })
    majors.value = Array.isArray(response) ? response : []
    // 获取总数
    const countRes = await getMajorsCount()
    total.value = countRes.total || majors.value.length
  } catch (error) {
    ElMessage.error('获取专业列表失败')
  } finally {
    loading.value = false
  }
}

const fetchUniversities = async () => {
  try {
    const response = await getUniversities({ limit: 1000 })
    universities.value = Array.isArray(response) ? response : []
  } catch (error) {
    ElMessage.error('获取院校列表失败')
  }
}

const showAddDialog = () => {
  isEdit.value = false
  form.value = { ...defaultForm }
  dialogVisible.value = true
}

const editMajor = (row) => {
  isEdit.value = true
  form.value = { ...row }
  dialogVisible.value = true
}

const handleDelete = (row) => {
  ElMessageBox.confirm('确定要删除这个专业吗？', '提示', {
    type: 'warning'
  }).then(async () => {
    try {
      await deleteMajorApi(row.id)
      ElMessage.success('删除成功')
      fetchMajors()
    } catch (error) {
      ElMessage.error('删除失败')
    }
  })
}

const submitForm = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return
  
  submitting.value = true
  try {
    if (isEdit.value) {
      await updateMajor(form.value.id, form.value)
      ElMessage.success('更新成功')
    } else {
      await createMajor(form.value)
      ElMessage.success('添加成功')
    }
    dialogVisible.value = false
    fetchMajors()
  } catch (error) {
    ElMessage.error(isEdit.value ? '更新失败' : '添加失败')
  } finally {
    submitting.value = false
  }
}

onMounted(() => {
  fetchMajors()
  fetchUniversities()
})
</script>

<style scoped lang="scss">
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

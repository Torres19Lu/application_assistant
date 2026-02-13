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
          <h2>案例管理</h2>
          <el-button type="primary" @click="showAddDialog">
            <el-icon><Plus /></el-icon> 添加案例
          </el-button>
        </el-header>

        <el-main>
          <el-card>
            <el-table :data="cases" v-loading="loading" border>
              <el-table-column prop="id" label="ID" width="60" />
              <el-table-column label="申请人" width="100">
                <template #default="{ row }">{{ row.applicant_name }}</template>
              </el-table-column>
              <el-table-column label="本科院校" min-width="140">
                <template #default="{ row }">{{ row.undergraduate_university_display || '-' }}</template>
              </el-table-column>
              <el-table-column label="录取院校" min-width="140">
                <template #default="{ row }">{{ row.admitted_university_name }}</template>
              </el-table-column>
              <el-table-column label="录取专业" min-width="160">
                <template #default="{ row }">{{ row.admitted_major_name }}</template>
              </el-table-column>
              <el-table-column label="GPA" width="90">
                <template #default="{ row }">{{ row.gpa ? `${row.gpa}/${row.gpa_scale}` : '-' }}</template>
              </el-table-column>
              <el-table-column label="结果" width="80">
                <template #default="{ row }">
                  <el-tag :type="resultTag(row.result)" size="small">{{ row.result }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column label="年份" width="80" prop="admission_year" />
              <el-table-column label="审核" width="80">
                <template #default="{ row }">
                  <el-switch
                    :model-value="!!row.is_verified"
                    @change="toggleVerify(row)"
                    size="small"
                  />
                </template>
              </el-table-column>
              <el-table-column label="操作" width="160" fixed="right">
                <template #default="{ row }">
                  <el-button type="primary" size="small" @click="editCase(row)">编辑</el-button>
                  <el-button type="danger" size="small" @click="handleDelete(row)">删除</el-button>
                </template>
              </el-table-column>
            </el-table>

            <div class="pagination">
              <el-pagination
                v-model:current-page="page"
                :page-size="pageSize"
                :total="total"
                layout="prev, pager, next, total"
                @current-change="loadCases"
              />
            </div>
          </el-card>
        </el-main>
      </el-container>
    </el-container>

    <!-- 添加/编辑对话框 -->
    <el-dialog v-model="dialogVisible" :title="isEdit ? '编辑案例' : '添加案例'" width="850px" top="3vh" destroy-on-close>
      <el-form :model="form" label-width="100px" class="case-form">
        <!-- 申请人信息 -->
        <el-divider content-position="left">申请人信息</el-divider>
        <el-row :gutter="16">
          <el-col :span="8">
            <el-form-item label="申请人">
              <el-input v-model="form.applicant_name" placeholder="匿名" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="本科院校">
              <el-select
                v-model="form.undergraduate_university_id"
                filterable remote :remote-method="searchUniv"
                placeholder="搜索院校" clearable style="width:100%"
                @change="onUndergradChange"
              >
                <el-option v-for="u in univOptions" :key="u.id" :label="u.name" :value="u.id" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="本科专业">
              <el-input v-model="form.undergraduate_major" placeholder="计算机科学" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="8">
            <el-form-item label="毕业年份">
              <el-input-number v-model="form.graduation_year" :min="2010" :max="2030" style="width:100%" />
            </el-form-item>
          </el-col>
        </el-row>

        <!-- 成绩 -->
        <el-divider content-position="left">学术成绩</el-divider>
        <el-row :gutter="16">
          <el-col :span="6">
            <el-form-item label="GPA">
              <el-input-number v-model="form.gpa" :min="0" :max="100" :step="0.01" :precision="2" style="width:100%" />
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="GPA满分">
              <el-select v-model="form.gpa_scale" style="width:100%">
                <el-option label="4.0" :value="4.0" />
                <el-option label="5.0" :value="5.0" />
                <el-option label="100" :value="100" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="排名">
              <el-input v-model="form.ranking" placeholder="如 5/120" />
            </el-form-item>
          </el-col>
        </el-row>

        <!-- IELTS -->
        <el-divider content-position="left">IELTS 雅思</el-divider>
        <el-row :gutter="16">
          <el-col :span="8"><el-form-item label="总分"><el-input-number v-model="form.ielts_overall" :min="0" :max="9" :step="0.5" :precision="1" style="width:100%" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="听力"><el-input-number v-model="form.ielts_listening" :min="0" :max="9" :step="0.5" :precision="1" style="width:100%" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="阅读"><el-input-number v-model="form.ielts_reading" :min="0" :max="9" :step="0.5" :precision="1" style="width:100%" /></el-form-item></el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="8"><el-form-item label="写作"><el-input-number v-model="form.ielts_writing" :min="0" :max="9" :step="0.5" :precision="1" style="width:100%" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="口语"><el-input-number v-model="form.ielts_speaking" :min="0" :max="9" :step="0.5" :precision="1" style="width:100%" /></el-form-item></el-col>
        </el-row>

        <!-- TOEFL -->
        <el-divider content-position="left">TOEFL 托福</el-divider>
        <el-row :gutter="16">
          <el-col :span="8"><el-form-item label="总分"><el-input-number v-model="form.toefl_total" :min="0" :max="120" style="width:100%" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="阅读"><el-input-number v-model="form.toefl_reading" :min="0" :max="30" style="width:100%" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="听力"><el-input-number v-model="form.toefl_listening" :min="0" :max="30" style="width:100%" /></el-form-item></el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="8"><el-form-item label="口语"><el-input-number v-model="form.toefl_speaking" :min="0" :max="30" style="width:100%" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="写作"><el-input-number v-model="form.toefl_writing" :min="0" :max="30" style="width:100%" /></el-form-item></el-col>
        </el-row>

        <!-- GRE / GMAT -->
        <el-divider content-position="left">GRE / GMAT</el-divider>
        <el-row :gutter="16">
          <el-col :span="8"><el-form-item label="GRE总分"><el-input-number v-model="form.gre_total" :min="260" :max="340" controls-position="right" style="width:100%" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="Verbal"><el-input-number v-model="form.gre_verbal" :min="130" :max="170" controls-position="right" style="width:100%" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="Quant"><el-input-number v-model="form.gre_quant" :min="130" :max="170" controls-position="right" style="width:100%" /></el-form-item></el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="8"><el-form-item label="Writing"><el-input-number v-model="form.gre_writing" :min="0" :max="6" :step="0.5" :precision="1" controls-position="right" style="width:100%" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="GMAT"><el-input-number v-model="form.gmat_total" :min="200" :max="800" :step="10" controls-position="right" style="width:100%" /></el-form-item></el-col>
        </el-row>

        <!-- 软背景 -->
        <el-divider content-position="left">软背景</el-divider>
        <el-row :gutter="16">
          <el-col :span="8"><el-form-item label="实习段数"><el-input-number v-model="form.internship_count" :min="0" :max="10" controls-position="right" style="width:100%" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="科研段数"><el-input-number v-model="form.research_count" :min="0" :max="10" controls-position="right" style="width:100%" /></el-form-item></el-col>
          <el-col :span="8"><el-form-item label="论文篇数"><el-input-number v-model="form.publication_count" :min="0" :max="20" controls-position="right" style="width:100%" /></el-form-item></el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="8"><el-form-item label="工作年限"><el-input-number v-model="form.work_years" :min="0" :max="20" :step="0.5" :precision="1" controls-position="right" style="width:100%" /></el-form-item></el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="12"><el-form-item label="实习详情"><el-input v-model="form.internship_experience" type="textarea" :rows="2" /></el-form-item></el-col>
          <el-col :span="12"><el-form-item label="科研详情"><el-input v-model="form.research_experience" type="textarea" :rows="2" /></el-form-item></el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="12"><el-form-item label="论文详情"><el-input v-model="form.publications" type="textarea" :rows="2" /></el-form-item></el-col>
          <el-col :span="12"><el-form-item label="工作详情"><el-input v-model="form.work_experience" type="textarea" :rows="2" /></el-form-item></el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="12"><el-form-item label="课外活动"><el-input v-model="form.extracurricular" type="textarea" :rows="2" /></el-form-item></el-col>
          <el-col :span="12"><el-form-item label="获奖经历"><el-input v-model="form.awards" type="textarea" :rows="2" /></el-form-item></el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="8">
            <el-form-item label="推荐信">
              <el-select v-model="form.recommendation_strength" style="width:100%">
                <el-option label="一般" value="weak" />
                <el-option label="较好" value="medium" />
                <el-option label="非常强" value="strong" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <!-- 录取结果 -->
        <el-divider content-position="left">录取结果</el-divider>
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="录取院校" required>
              <el-select
                v-model="form.admitted_university_id"
                filterable remote :remote-method="searchUniv"
                placeholder="搜索院校" style="width:100%"
                @change="onAdmittedUnivChange"
              >
                <el-option v-for="u in univOptions" :key="u.id" :label="u.name" :value="u.id" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="录取专业" required>
              <el-select
                v-model="form.admitted_major_id"
                filterable remote :remote-method="searchMaj"
                placeholder="搜索专业" style="width:100%"
              >
                <el-option v-for="m in majorOptions" :key="m.id" :label="m.name" :value="m.id" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="6">
            <el-form-item label="结果">
              <el-select v-model="form.result" style="width:100%">
                <el-option label="录取" value="录取" />
                <el-option label="拒绝" value="拒绝" />
                <el-option label="候补" value="候补" />
                <el-option label="放弃" value="放弃" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="年份">
              <el-input-number v-model="form.admission_year" :min="2020" :max="2030" controls-position="right" style="width:100%" />
            </el-form-item>
          </el-col>
          <el-col :span="6">
            <el-form-item label="学期">
              <el-select v-model="form.admission_semester" style="width:100%">
                <el-option label="秋季" value="秋季" />
                <el-option label="春季" value="春季" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="12">
            <el-form-item label="奖学金">
              <el-input v-model="form.scholarship" placeholder="如：全额奖学金" />
            </el-form-item>
          </el-col>
        </el-row>
        <el-row :gutter="16">
          <el-col :span="24">
            <el-form-item label="备注">
              <el-input v-model="form.remarks" type="textarea" :rows="2" />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>

      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitForm" :loading="submitting">{{ isEdit ? '更新' : '添加' }}</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getCases, getCasesCount, createCase, updateCase, deleteCase, searchUniversities, searchMajors } from '@/utils/api'

const loading = ref(false)
const submitting = ref(false)
const cases = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = 15
const dialogVisible = ref(false)
const isEdit = ref(false)
const editId = ref(null)

const univOptions = ref([])
const majorOptions = ref([])

const defaultForm = () => ({
  applicant_name: '匿名',
  undergraduate_university_id: null,
  undergraduate_university_name: '',
  undergraduate_major: '',
  graduation_year: null,
  gpa: null,
  gpa_scale: 4.0,
  ranking: '',
  ielts_overall: null, ielts_listening: null, ielts_reading: null, ielts_writing: null, ielts_speaking: null,
  toefl_total: null, toefl_reading: null, toefl_listening: null, toefl_speaking: null, toefl_writing: null,
  gre_total: null, gre_verbal: null, gre_quant: null, gre_writing: null,
  gmat_total: null,
  internship_count: 0, internship_experience: '',
  research_count: 0, research_experience: '',
  publication_count: 0, publications: '',
  work_years: 0, work_experience: '',
  extracurricular: '', awards: '',
  recommendation_strength: 'medium',
  admitted_university_id: null,
  admitted_major_id: null,
  admission_year: 2026,
  admission_semester: '秋季',
  result: '录取',
  scholarship: '',
  remarks: ''
})

const form = ref(defaultForm())

const resultTag = (r) => {
  if (r === '录取') return 'success'
  if (r === '拒绝') return 'danger'
  if (r === '候补') return 'warning'
  return 'info'
}

const searchUniv = async (q) => {
  if (!q || q.length < 1) return
  try { univOptions.value = await searchUniversities(q) } catch {}
}

const searchMaj = async (q) => {
  if (!q || q.length < 1) return
  try { majorOptions.value = await searchMajors(q, form.value.admitted_university_id) } catch {}
}

const onUndergradChange = (id) => {
  const u = univOptions.value.find(u => u.id === id)
  if (u) form.value.undergraduate_university_name = u.name
}

const onAdmittedUnivChange = () => {
  form.value.admitted_major_id = null
  majorOptions.value = []
}

const loadCases = async () => {
  loading.value = true
  try {
    const params = { skip: (page.value - 1) * pageSize, limit: pageSize }
    const [casesData, countData] = await Promise.all([getCases(params), getCasesCount()])
    cases.value = casesData
    total.value = countData.total
  } finally { loading.value = false }
}

const showAddDialog = () => {
  isEdit.value = false
  editId.value = null
  form.value = defaultForm()
  univOptions.value = []
  majorOptions.value = []
  dialogVisible.value = true
}

const editCase = (row) => {
  isEdit.value = true
  editId.value = row.id
  form.value = { ...defaultForm(), ...row }
  // 预设选项
  if (row.undergraduate_university_display) {
    univOptions.value = [{ id: row.undergraduate_university_id, name: row.undergraduate_university_display }]
  }
  if (row.admitted_university_name) {
    univOptions.value = [...univOptions.value, { id: row.admitted_university_id, name: row.admitted_university_name }]
  }
  if (row.admitted_major_name) {
    majorOptions.value = [{ id: row.admitted_major_id, name: row.admitted_major_name }]
  }
  dialogVisible.value = true
}

const submitForm = async () => {
  if (!form.value.admitted_university_id || !form.value.admitted_major_id) {
    ElMessage.warning('请选择录取院校和专业')
    return
  }
  submitting.value = true
  try {
    if (isEdit.value) {
      await updateCase(editId.value, form.value)
      ElMessage.success('更新成功')
    } else {
      await createCase(form.value)
      ElMessage.success('添加成功')
    }
    dialogVisible.value = false
    loadCases()
  } catch (e) {
    console.error(e)
  } finally { submitting.value = false }
}

const handleDelete = (row) => {
  ElMessageBox.confirm(`确定删除案例 #${row.id}？`, '确认', { type: 'warning' })
    .then(async () => {
      await deleteCase(row.id)
      ElMessage.success('删除成功')
      loadCases()
    }).catch(() => {})
}

const toggleVerify = async (row) => {
  try {
    await updateCase(row.id, { is_verified: row.is_verified ? 0 : 1 })
    ElMessage.success('审核状态已更新')
    loadCases()
  } catch {}
}

onMounted(loadCases)
</script>

<style lang="scss" scoped>
.admin-page {
  height: 100vh;
  .el-container { height: 100%; }
  .el-main { background: #f5f7fa; }
}

.sidebar {
  background: #1f2937;
  .logo {
    height: 60px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    color: white;
    font-size: 18px;
    font-weight: 600;
    border-bottom: 1px solid rgba(255,255,255,0.1);
  }
  .el-menu { border-right: none; }
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  border-bottom: 1px solid #e5e7eb;
  h2 { font-size: 18px; }
}

.pagination {
  margin-top: 16px;
  display: flex;
  justify-content: center;
}

.case-form {
  max-height: 70vh;
  overflow-y: auto;
  padding-right: 12px;
}
</style>

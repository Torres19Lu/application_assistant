<template>
  <div class="case-detail-page" v-if="caseData">
    <NavBar />

    <div class="back-nav">
      <div class="container">
        <el-button link @click="$router.push('/cases')">
          <el-icon><ArrowLeft /></el-icon> 返回案例列表
        </el-button>
      </div>
    </div>

    <!-- 头部概要 -->
    <div class="case-header" :class="resultClass">
      <div class="container">
        <div class="header-content">
          <el-tag :type="resultTagType" size="large" class="result-tag">{{ caseData.result }}</el-tag>
          <h1>{{ caseData.admitted_university_name }}</h1>
          <p class="major">{{ caseData.admitted_major_name }}</p>
          <div class="header-meta">
            <span><el-icon><Location /></el-icon> {{ caseData.admitted_country }}</span>
            <span><el-icon><Calendar /></el-icon> {{ caseData.admission_year }} {{ caseData.admission_semester }}</span>
            <span v-if="caseData.scholarship"><el-icon><Present /></el-icon> {{ caseData.scholarship }}</span>
          </div>
        </div>
      </div>
    </div>

    <div class="container detail-body">
      <el-row :gutter="24">
        <!-- 左侧 -->
        <el-col :span="16">
          <!-- 申请人背景 -->
          <div class="section-card">
            <h2><el-icon><User /></el-icon> 申请人背景</h2>
            <el-descriptions :column="2" border>
              <el-descriptions-item label="申请人">{{ caseData.applicant_name }}</el-descriptions-item>
              <el-descriptions-item label="本科院校">{{ caseData.undergraduate_university_display || '未填写' }}</el-descriptions-item>
              <el-descriptions-item label="本科专业">{{ caseData.undergraduate_major || '未填写' }}</el-descriptions-item>
              <el-descriptions-item label="毕业年份">{{ caseData.graduation_year || '未填写' }}</el-descriptions-item>
            </el-descriptions>
          </div>

          <!-- 学术成绩 -->
          <div class="section-card">
            <h2><el-icon><Reading /></el-icon> 学术成绩</h2>
            <el-descriptions :column="3" border>
              <el-descriptions-item label="GPA">
                <span v-if="caseData.gpa">{{ caseData.gpa }} / {{ caseData.gpa_scale }}</span>
                <span v-else class="na">N/A</span>
              </el-descriptions-item>
              <el-descriptions-item label="排名">{{ caseData.ranking || 'N/A' }}</el-descriptions-item>
            </el-descriptions>
          </div>

          <!-- 语言成绩 -->
          <div class="section-card">
            <h2><el-icon><ChatDotRound /></el-icon> 语言与标化成绩</h2>

            <!-- IELTS -->
            <div v-if="caseData.ielts_overall" class="score-block">
              <h3>IELTS 雅思</h3>
              <div class="score-grid">
                <div class="score-item main">
                  <span class="score-value">{{ caseData.ielts_overall }}</span>
                  <span class="score-label">总分</span>
                </div>
                <div class="score-item" v-if="caseData.ielts_listening">
                  <span class="score-value">{{ caseData.ielts_listening }}</span>
                  <span class="score-label">听力</span>
                </div>
                <div class="score-item" v-if="caseData.ielts_reading">
                  <span class="score-value">{{ caseData.ielts_reading }}</span>
                  <span class="score-label">阅读</span>
                </div>
                <div class="score-item" v-if="caseData.ielts_writing">
                  <span class="score-value">{{ caseData.ielts_writing }}</span>
                  <span class="score-label">写作</span>
                </div>
                <div class="score-item" v-if="caseData.ielts_speaking">
                  <span class="score-value">{{ caseData.ielts_speaking }}</span>
                  <span class="score-label">口语</span>
                </div>
              </div>
            </div>

            <!-- TOEFL -->
            <div v-if="caseData.toefl_total" class="score-block">
              <h3>TOEFL 托福</h3>
              <div class="score-grid">
                <div class="score-item main">
                  <span class="score-value">{{ caseData.toefl_total }}</span>
                  <span class="score-label">总分</span>
                </div>
                <div class="score-item" v-if="caseData.toefl_reading">
                  <span class="score-value">{{ caseData.toefl_reading }}</span>
                  <span class="score-label">阅读</span>
                </div>
                <div class="score-item" v-if="caseData.toefl_listening">
                  <span class="score-value">{{ caseData.toefl_listening }}</span>
                  <span class="score-label">听力</span>
                </div>
                <div class="score-item" v-if="caseData.toefl_speaking">
                  <span class="score-value">{{ caseData.toefl_speaking }}</span>
                  <span class="score-label">口语</span>
                </div>
                <div class="score-item" v-if="caseData.toefl_writing">
                  <span class="score-value">{{ caseData.toefl_writing }}</span>
                  <span class="score-label">写作</span>
                </div>
              </div>
            </div>

            <!-- GRE -->
            <div v-if="caseData.gre_total" class="score-block">
              <h3>GRE</h3>
              <div class="score-grid">
                <div class="score-item main">
                  <span class="score-value">{{ caseData.gre_total }}</span>
                  <span class="score-label">总分</span>
                </div>
                <div class="score-item" v-if="caseData.gre_verbal">
                  <span class="score-value">{{ caseData.gre_verbal }}</span>
                  <span class="score-label">Verbal</span>
                </div>
                <div class="score-item" v-if="caseData.gre_quant">
                  <span class="score-value">{{ caseData.gre_quant }}</span>
                  <span class="score-label">Quant</span>
                </div>
                <div class="score-item" v-if="caseData.gre_writing">
                  <span class="score-value">{{ caseData.gre_writing }}</span>
                  <span class="score-label">Writing</span>
                </div>
              </div>
            </div>

            <!-- GMAT -->
            <div v-if="caseData.gmat_total" class="score-block">
              <h3>GMAT</h3>
              <div class="score-grid">
                <div class="score-item main">
                  <span class="score-value">{{ caseData.gmat_total }}</span>
                  <span class="score-label">总分</span>
                </div>
              </div>
            </div>

            <div v-if="!caseData.ielts_overall && !caseData.toefl_total && !caseData.gre_total && !caseData.gmat_total"
              class="no-data">暂无语言或标化成绩信息</div>
          </div>

          <!-- 软背景 -->
          <div class="section-card">
            <h2><el-icon><Briefcase /></el-icon> 软背景</h2>

            <div class="soft-grid">
              <div class="soft-item" v-if="caseData.internship_count">
                <div class="soft-header">
                  <span class="soft-count">{{ caseData.internship_count }}段</span>
                  <span class="soft-title">实习经历</span>
                </div>
                <p v-if="caseData.internship_experience" class="soft-detail">{{ caseData.internship_experience }}</p>
              </div>

              <div class="soft-item" v-if="caseData.research_count">
                <div class="soft-header">
                  <span class="soft-count">{{ caseData.research_count }}段</span>
                  <span class="soft-title">科研经历</span>
                </div>
                <p v-if="caseData.research_experience" class="soft-detail">{{ caseData.research_experience }}</p>
              </div>

              <div class="soft-item" v-if="caseData.publication_count">
                <div class="soft-header">
                  <span class="soft-count">{{ caseData.publication_count }}篇</span>
                  <span class="soft-title">论文发表</span>
                </div>
                <p v-if="caseData.publications" class="soft-detail">{{ caseData.publications }}</p>
              </div>

              <div class="soft-item" v-if="caseData.work_years">
                <div class="soft-header">
                  <span class="soft-count">{{ caseData.work_years }}年</span>
                  <span class="soft-title">工作经验</span>
                </div>
                <p v-if="caseData.work_experience" class="soft-detail">{{ caseData.work_experience }}</p>
              </div>

              <div class="soft-item" v-if="caseData.extracurricular">
                <div class="soft-header">
                  <span class="soft-title">课外活动</span>
                </div>
                <p class="soft-detail">{{ caseData.extracurricular }}</p>
              </div>

              <div class="soft-item" v-if="caseData.awards">
                <div class="soft-header">
                  <span class="soft-title">获奖经历</span>
                </div>
                <p class="soft-detail">{{ caseData.awards }}</p>
              </div>
            </div>

            <div class="no-data" v-if="!caseData.internship_count && !caseData.research_count && !caseData.publication_count && !caseData.work_years && !caseData.extracurricular && !caseData.awards">
              暂无软背景信息
            </div>
          </div>

          <!-- 备注 -->
          <div class="section-card" v-if="caseData.remarks">
            <h2><el-icon><Memo /></el-icon> 备注</h2>
            <p class="remarks-text">{{ caseData.remarks }}</p>
          </div>
        </el-col>

        <!-- 右侧摘要 -->
        <el-col :span="8">
          <div class="sidebar-card summary-card">
            <h3>录取概要</h3>
            <div class="summary-item">
              <span class="label">录取院校</span>
              <span class="value">{{ caseData.admitted_university_name }}</span>
            </div>
            <div class="summary-item">
              <span class="label">录取专业</span>
              <span class="value">{{ caseData.admitted_major_name }}</span>
            </div>
            <div class="summary-item">
              <span class="label">录取结果</span>
              <el-tag :type="resultTagType" size="small">{{ caseData.result }}</el-tag>
            </div>
            <div class="summary-item">
              <span class="label">入学时间</span>
              <span class="value">{{ caseData.admission_year }} {{ caseData.admission_semester }}</span>
            </div>
            <div class="summary-item" v-if="caseData.scholarship">
              <span class="label">奖学金</span>
              <span class="value scholarship">{{ caseData.scholarship }}</span>
            </div>
            <div class="summary-item">
              <span class="label">推荐信强度</span>
              <span class="value">{{ strengthLabel(caseData.recommendation_strength) }}</span>
            </div>
          </div>

          <div class="sidebar-card" v-if="caseData.submitter_name">
            <h3>提交者</h3>
            <p>{{ caseData.submitter_name }}</p>
            <p class="date">{{ formatDate(caseData.created_at) }}</p>
          </div>
        </el-col>
      </el-row>
    </div>

    <Footer />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import NavBar from '@/components/common/NavBar.vue'
import Footer from '@/components/common/Footer.vue'
import { getCase } from '@/utils/api'

const route = useRoute()
const caseData = ref(null)

const resultTagType = computed(() => {
  if (!caseData.value) return 'info'
  const r = caseData.value.result
  if (r === '录取') return 'success'
  if (r === '拒绝') return 'danger'
  if (r === '候补') return 'warning'
  return 'info'
})

const resultClass = computed(() => {
  if (!caseData.value) return ''
  return 'result-' + caseData.value.result
})

const strengthLabel = (s) => {
  const map = { weak: '一般', medium: '较好', strong: '非常强' }
  return map[s] || s || '未填写'
}

const formatDate = (d) => {
  if (!d) return ''
  return new Date(d).toLocaleDateString('zh-CN')
}

onMounted(async () => {
  try {
    caseData.value = await getCase(route.params.id)
  } catch (e) {
    console.error('加载案例详情失败', e)
  }
})
</script>

<style lang="scss" scoped>
@use '@/styles/variables.scss' as *;

.case-detail-page {
  min-height: 100vh;
  background: #f5f7fa;
  padding-top: 70px;
}

.back-nav {
  background: white;
  padding: 12px 0;
  border-bottom: 1px solid $border-color;
}

/* 头部 */
.case-header {
  background: linear-gradient(135deg, #1e40af, #3b82f6);
  color: white;
  padding: 40px 0 32px;
  &.result-录取 { background: linear-gradient(135deg, #065f46, #10b981); }
  &.result-拒绝 { background: linear-gradient(135deg, #991b1b, #ef4444); }
  &.result-候补 { background: linear-gradient(135deg, #92400e, #f59e0b); }
}

.header-content {
  .result-tag { margin-bottom: 12px; }
  h1 { font-size: 28px; margin-bottom: 4px; }
  .major { font-size: 16px; opacity: 0.9; margin-bottom: 12px; }
  .header-meta {
    display: flex;
    gap: 24px;
    font-size: 14px;
    opacity: 0.85;
    span { display: flex; align-items: center; gap: 4px; }
  }
}

.container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }

.detail-body { padding: 32px 20px 60px; }

/* 信息卡 */
.section-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 20px;
  box-shadow: $box-shadow;
  h2 {
    font-size: 18px;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 8px;
    .el-icon { color: $primary-light; }
  }
}

/* 成绩展示 */
.score-block {
  margin-bottom: 20px;
  &:last-child { margin-bottom: 0; }
  h3 { font-size: 15px; color: $text-secondary; margin-bottom: 10px; }
}
.score-grid {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}
.score-item {
  text-align: center;
  padding: 12px 20px;
  border-radius: 8px;
  background: $secondary-color;
  min-width: 70px;
  .score-value { display: block; font-size: 22px; font-weight: 700; color: $primary-color; }
  .score-label { display: block; font-size: 12px; color: $text-secondary; margin-top: 4px; }
  &.main {
    background: $primary-light;
    .score-value { color: white; }
    .score-label { color: rgba(255,255,255,0.8); }
  }
}

/* 软背景 */
.soft-grid {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.soft-item {
  padding: 16px;
  background: $secondary-color;
  border-radius: 8px;
  .soft-header {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 6px;
    .soft-count { font-size: 18px; font-weight: 700; color: $primary-color; }
    .soft-title { font-size: 14px; color: $text-secondary; }
  }
  .soft-detail { font-size: 14px; color: $text-primary; line-height: 1.7; margin: 0; }
}

.no-data { color: $text-muted; text-align: center; padding: 24px; }

.remarks-text { line-height: 1.8; color: $text-primary; }

/* 右侧栏 */
.sidebar-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  margin-bottom: 16px;
  box-shadow: $box-shadow;
  h3 { font-size: 16px; margin-bottom: 16px; color: $text-primary; }
  .date { font-size: 13px; color: $text-muted; }
}
.summary-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
  border-bottom: 1px solid $border-color;
  &:last-child { border-bottom: none; }
  .label { font-size: 13px; color: $text-secondary; }
  .value { font-size: 14px; color: $text-primary; font-weight: 500; }
  .scholarship { color: $success-color; }
}

@media (max-width: 768px) {
  .detail-body .el-row { flex-direction: column; }
  .el-col { max-width: 100% !important; flex: 0 0 100% !important; }
}
</style>

<template>
  <div class="case-list-page">
    <NavBar />

    <div class="page-header">
      <div class="container">
        <h1>🎓 录取案例库</h1>
        <p>浏览真实录取案例，了解成功申请者背景，助力你的留学规划</p>
      </div>
    </div>

    <div class="container">
      <!-- 功能切换 -->
      <div class="mode-switch">
        <el-radio-group v-model="mode" size="large">
          <el-radio-button value="browse">
            <el-icon><Document /></el-icon> 浏览案例
          </el-radio-button>
          <el-radio-button value="recommend">
            <el-icon><MagicStick /></el-icon> AI 智能推荐
          </el-radio-button>
        </el-radio-group>
      </div>

      <!-- ========== 浏览模式 ========== -->
      <template v-if="mode === 'browse'">
        <div class="filter-section">
          <div class="filter-row">
            <div class="filter-group">
              <label>录取国家</label>
              <el-select v-model="filters.country" placeholder="全部国家" clearable @change="loadCases">
                <el-option label="美国" value="美国" />
                <el-option label="英国" value="英国" />
                <el-option label="新加坡" value="新加坡" />
                <el-option label="中国香港" value="中国香港" />
                <el-option label="澳大利亚" value="澳大利亚" />
                <el-option label="加拿大" value="加拿大" />
                <el-option label="瑞士" value="瑞士" />
                <el-option label="日本" value="日本" />
              </el-select>
            </div>

            <div class="filter-group">
              <label>录取结果</label>
              <el-select v-model="filters.result" placeholder="全部结果" clearable @change="loadCases">
                <el-option label="录取" value="录取" />
                <el-option label="拒绝" value="拒绝" />
                <el-option label="候补" value="候补" />
              </el-select>
            </div>

            <div class="filter-group">
              <label>录取年份</label>
              <el-select v-model="filters.year" placeholder="全部年份" clearable @change="loadCases">
                <el-option label="2026" :value="2026" />
                <el-option label="2025" :value="2025" />
                <el-option label="2024" :value="2024" />
                <el-option label="2023" :value="2023" />
              </el-select>
            </div>

            <div class="filter-group search-group">
              <label>关键词</label>
              <el-input v-model="filters.keyword" placeholder="搜索院校/专业/申请人" clearable
                @keyup.enter="loadCases" @clear="loadCases">
                <template #append>
                  <el-button @click="loadCases"><el-icon><Search /></el-icon></el-button>
                </template>
              </el-input>
            </div>
          </div>
        </div>

        <!-- 案例卡片列表 -->
        <div class="case-cards" v-loading="loading">
          <div v-if="cases.length === 0 && !loading" class="empty-state">
            <el-empty description="暂无录取案例">
              <el-button type="primary" @click="mode = 'recommend'">试试 AI 智能推荐</el-button>
            </el-empty>
          </div>

          <div class="case-card" v-for="c in cases" :key="c.id" @click="$router.push(`/cases/${c.id}`)">
            <div class="card-header">
              <div class="result-tag">
                <el-tag :type="resultTagType(c.result)" size="large">{{ c.result }}</el-tag>
              </div>
              <span class="year-badge">{{ c.admission_year }} {{ c.admission_semester }}</span>
            </div>

            <div class="card-body">
              <h3 class="admitted-info">
                <span class="university-name">{{ c.admitted_university_name }}</span>
                <span class="major-name">{{ c.admitted_major_name }}</span>
              </h3>

              <div class="applicant-info">
                <div class="info-row">
                  <span class="label">本科院校</span>
                  <span class="value">{{ c.undergraduate_university_display || '未填写' }}</span>
                </div>
                <div class="info-row">
                  <span class="label">本科专业</span>
                  <span class="value">{{ c.undergraduate_major || '未填写' }}</span>
                </div>
              </div>

              <div class="score-tags">
                <el-tag v-if="c.gpa" type="info" size="small">GPA {{ c.gpa }}/{{ c.gpa_scale }}</el-tag>
                <el-tag v-if="c.ielts_overall" type="warning" size="small">IELTS {{ c.ielts_overall }}</el-tag>
                <el-tag v-if="c.toefl_total" type="warning" size="small">TOEFL {{ c.toefl_total }}</el-tag>
                <el-tag v-if="c.gre_total" type="danger" size="small">GRE {{ c.gre_total }}</el-tag>
                <el-tag v-if="c.gmat_total" type="danger" size="small">GMAT {{ c.gmat_total }}</el-tag>
                <el-tag v-if="c.internship_count" size="small">实习 {{ c.internship_count }}段</el-tag>
                <el-tag v-if="c.research_count" size="small">科研 {{ c.research_count }}段</el-tag>
                <el-tag v-if="c.publication_count" size="small">论文 {{ c.publication_count }}篇</el-tag>
              </div>

              <div class="scholarship" v-if="c.scholarship">
                <el-icon><Present /></el-icon> {{ c.scholarship }}
              </div>
            </div>

            <div class="card-footer">
              <span class="country-tag">
                <el-icon><Location /></el-icon> {{ c.admitted_country }}
              </span>
              <span class="submitter" v-if="c.submitter_name">{{ c.submitter_name }}</span>
            </div>
          </div>
        </div>

        <!-- 分页 -->
        <div class="pagination-wrapper" v-if="total > pageSize">
          <el-pagination
            v-model:current-page="page"
            :page-size="pageSize"
            :total="total"
            layout="prev, pager, next, total"
            @current-change="loadCases"
          />
        </div>
      </template>

      <!-- ========== AI 推荐模式 ========== -->
      <template v-if="mode === 'recommend'">
        <div class="recommend-section">
          <div class="recommend-form-card">
            <h2><el-icon><MagicStick /></el-icon> 输入你的背景条件</h2>
            <p class="subtitle">系统将基于历史录取数据，为你智能推荐录取概率较高的院校和专业</p>

            <el-form :model="profile" label-width="100px" class="profile-form">
              <el-divider content-position="left">🎓 学术背景</el-divider>

              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="本科院校">
                    <el-select
                      v-model="profile.undergraduate_university_name"
                      filterable
                      remote
                      :remote-method="searchUniv"
                      placeholder="输入院校名称搜索"
                      clearable
                      allow-create
                      default-first-option
                      style="width:100%"
                    >
                      <el-option
                        v-for="u in univOptions"
                        :key="u.id"
                        :label="u.name"
                        :value="u.name"
                      >
                        <span>{{ u.name }}</span>
                        <span style="color: #999; font-size: 12px; margin-left: 8px;">{{ u.country }}</span>
                      </el-option>
                    </el-select>
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="本科专业">
                    <el-input v-model="profile.undergraduate_major" placeholder="如：计算机科学" />
                  </el-form-item>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="8">
                  <el-form-item label="GPA">
                    <el-input-number v-model="profile.gpa" :min="0" :max="100" :step="0.1" :precision="2" style="width:100%" />
                  </el-form-item>
                </el-col>
                <el-col :span="8">
                  <el-form-item label="GPA满分">
                    <el-select v-model="profile.gpa_scale" style="width:100%">
                      <el-option label="4.0制" :value="4.0" />
                      <el-option label="5.0制" :value="5.0" />
                      <el-option label="100分制" :value="100" />
                    </el-select>
                  </el-form-item>
                </el-col>
              </el-row>

              <el-divider content-position="left">📝 标准化考试</el-divider>

              <!-- IELTS -->
              <div class="test-section">
                <div class="test-label">IELTS 雅思</div>
                <div class="score-row">
                  <div class="score-item">
                    <el-form-item label="总分">
                      <el-input-number v-model="profile.ielts_overall" :min="0" :max="9" :step="0.5" :precision="1" controls-position="right" style="width:100%" />
                    </el-form-item>
                  </div>
                  <div class="score-item">
                    <el-form-item label="听力">
                      <el-input-number v-model="profile.ielts_listening" :min="0" :max="9" :step="0.5" :precision="1" controls-position="right" style="width:100%" />
                    </el-form-item>
                  </div>
                  <div class="score-item">
                    <el-form-item label="阅读">
                      <el-input-number v-model="profile.ielts_reading" :min="0" :max="9" :step="0.5" :precision="1" controls-position="right" style="width:100%" />
                    </el-form-item>
                  </div>
                  <div class="score-item">
                    <el-form-item label="写作">
                      <el-input-number v-model="profile.ielts_writing" :min="0" :max="9" :step="0.5" :precision="1" controls-position="right" style="width:100%" />
                    </el-form-item>
                  </div>
                  <div class="score-item">
                    <el-form-item label="口语">
                      <el-input-number v-model="profile.ielts_speaking" :min="0" :max="9" :step="0.5" :precision="1" controls-position="right" style="width:100%" />
                    </el-form-item>
                  </div>
                </div>
              </div>

              <!-- TOEFL -->
              <div class="test-section">
                <div class="test-label">TOEFL 托福</div>
                <div class="score-row">
                  <div class="score-item">
                    <el-form-item label="总分">
                      <el-input-number v-model="profile.toefl_total" :min="0" :max="120" :step="1" controls-position="right" style="width:100%" />
                    </el-form-item>
                  </div>
                  <div class="score-item">
                    <el-form-item label="听力">
                      <el-input-number v-model="profile.toefl_listening" :min="0" :max="30" :step="1" controls-position="right" style="width:100%" />
                    </el-form-item>
                  </div>
                  <div class="score-item">
                    <el-form-item label="阅读">
                      <el-input-number v-model="profile.toefl_reading" :min="0" :max="30" :step="1" controls-position="right" style="width:100%" />
                    </el-form-item>
                  </div>
                  <div class="score-item">
                    <el-form-item label="写作">
                      <el-input-number v-model="profile.toefl_writing" :min="0" :max="30" :step="1" controls-position="right" style="width:100%" />
                    </el-form-item>
                  </div>
                  <div class="score-item">
                    <el-form-item label="口语">
                      <el-input-number v-model="profile.toefl_speaking" :min="0" :max="30" :step="1" controls-position="right" style="width:100%" />
                    </el-form-item>
                  </div>
                </div>
              </div>

              <!-- GRE -->
              <div class="test-section">
                <div class="test-label">GRE</div>
                <el-row :gutter="12">
                  <el-col :span="5">
                    <el-form-item label="总分">
                      <el-input-number v-model="profile.gre_total" :min="260" :max="340" :step="1" controls-position="right" style="width:100%" />
                    </el-form-item>
                  </el-col>
                  <el-col :span="5">
                    <el-form-item label="Verbal">
                      <el-input-number v-model="profile.gre_verbal" :min="130" :max="170" :step="1" controls-position="right" style="width:100%" />
                    </el-form-item>
                  </el-col>
                  <el-col :span="5">
                    <el-form-item label="Quant">
                      <el-input-number v-model="profile.gre_quant" :min="130" :max="170" :step="1" controls-position="right" style="width:100%" />
                    </el-form-item>
                  </el-col>
                  <el-col :span="5">
                    <el-form-item label="Writing">
                      <el-input-number v-model="profile.gre_writing" :min="0" :max="6" :step="0.5" :precision="1" controls-position="right" style="width:100%" />
                    </el-form-item>
                  </el-col>
                </el-row>
              </div>

              <!-- GMAT -->
              <div class="test-section">
                <div class="test-label">GMAT</div>
                <el-row :gutter="12">
                  <el-col :span="5">
                    <el-form-item label="总分">
                      <el-input-number v-model="profile.gmat_total" :min="200" :max="800" :step="10" controls-position="right" style="width:100%" />
                    </el-form-item>
                  </el-col>
                </el-row>
              </div>

              <el-divider content-position="left">💼 软背景</el-divider>

              <el-row :gutter="20">
                <el-col :span="6">
                  <el-form-item label="实习段数">
                    <el-input-number v-model="profile.internship_count" :min="0" :max="10" style="width:100%" />
                  </el-form-item>
                </el-col>
                <el-col :span="6">
                  <el-form-item label="科研段数">
                    <el-input-number v-model="profile.research_count" :min="0" :max="10" style="width:100%" />
                  </el-form-item>
                </el-col>
                <el-col :span="6">
                  <el-form-item label="论文发表">
                    <el-input-number v-model="profile.publication_count" :min="0" :max="20" style="width:100%" />
                  </el-form-item>
                </el-col>
                <el-col :span="6">
                  <el-form-item label="工作年限">
                    <el-input-number v-model="profile.work_years" :min="0" :max="20" :step="0.5" :precision="1" style="width:100%" />
                  </el-form-item>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="实习经历">
                    <el-input v-model="profile.internship_experience" type="textarea" :rows="3"
                      placeholder="例：字节跳动 产品运营实习（2024.06-2024.09）&#10;腾讯 后端开发实习（2024.12-2025.03）" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="科研经历">
                    <el-input v-model="profile.research_experience" type="textarea" :rows="3"
                      placeholder="例：XX 教授课题组，研究方向：自然语言处理&#10;独立完成数据采集与模型训练" />
                  </el-form-item>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="论文发表">
                    <el-input v-model="profile.publications" type="textarea" :rows="3"
                      placeholder="例：《基于深度学习的情感分析研究》发表于 ACL 2025&#10;第一作者，影响因子 5.2" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="工作经历">
                    <el-input v-model="profile.work_experience" type="textarea" :rows="3"
                      placeholder="例：华为 软件工程师（2023.07-2025.06）&#10;负责云计算平台核心模块开发" />
                  </el-form-item>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="12">
                  <el-form-item label="课外活动">
                    <el-input v-model="profile.extracurricular" type="textarea" :rows="2"
                      placeholder="例：校学生会主席、志愿者协会负责人、国际交换项目等" />
                  </el-form-item>
                </el-col>
                <el-col :span="12">
                  <el-form-item label="获奖经历">
                    <el-input v-model="profile.awards" type="textarea" :rows="2"
                      placeholder="例：国家奖学金（2024）、数学建模大赛省一等奖等" />
                  </el-form-item>
                </el-col>
              </el-row>

              <el-row :gutter="20">
                <el-col :span="8">
                  <el-form-item label="推荐信">
                    <el-select v-model="profile.recommendation_strength" style="width:100%">
                      <el-option label="一般" value="weak" />
                      <el-option label="较好" value="medium" />
                      <el-option label="非常强" value="strong" />
                    </el-select>
                  </el-form-item>
                </el-col>
              </el-row>

              <el-alert
                title="未来将支持上传简历（CV），通过 AI 大模型自动解析背景信息"
                type="info"
                :closable="false"
                show-icon
                style="margin-bottom: 20px;"
              />

              <div class="form-actions">
                <el-button type="primary" size="large" @click="doRecommend" :loading="recommendLoading">
                  <el-icon><MagicStick /></el-icon> 开始智能推荐
                </el-button>
              </div>
            </el-form>
          </div>

          <!-- 推荐结果 -->
          <div v-if="recommendations.length > 0" class="recommend-results">
            <h2>📊 推荐结果</h2>
            <p class="subtitle">基于 AI 算法分析历史录取数据，以下是为你推荐的院校和专业</p>

            <div class="result-cards">
              <div class="result-card" v-for="(r, idx) in recommendations" :key="idx">
                <div class="rank-badge">#{{ idx + 1 }}</div>

                <div class="result-main">
                  <h3>{{ r.university_name }}</h3>
                  <p class="major-name">{{ r.major_name }}</p>
                  <span class="country-tag"><el-icon><Location /></el-icon> {{ r.country }}</span>
                </div>

                <div class="probability-circle" :class="probClass(r.admission_probability)">
                  <span class="prob-value">{{ r.admission_probability }}%</span>
                  <span class="prob-label">录取概率</span>
                </div>

                <div class="result-stats">
                  <div class="stat">
                    <span class="stat-num">{{ r.similar_cases_count }}</span>
                    <span class="stat-label">相似案例</span>
                  </div>
                  <div class="stat">
                    <span class="stat-num">{{ r.admitted_count }}</span>
                    <span class="stat-label">录取人数</span>
                  </div>
                  <div class="stat" v-if="r.avg_gpa">
                    <span class="stat-num">{{ r.avg_gpa }}</span>
                    <span class="stat-label">平均GPA</span>
                  </div>
                  <div class="stat" v-if="r.avg_ielts">
                    <span class="stat-num">{{ r.avg_ielts }}</span>
                    <span class="stat-label">平均IELTS</span>
                  </div>
                  <div class="stat" v-if="r.avg_toefl">
                    <span class="stat-num">{{ r.avg_toefl }}</span>
                    <span class="stat-label">平均TOEFL</span>
                  </div>
                  <div class="stat" v-if="r.scholarship_rate > 0">
                    <span class="stat-num">{{ r.scholarship_rate }}%</span>
                    <span class="stat-label">奖学金率</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </template>
    </div>

    <Footer />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import NavBar from '@/components/common/NavBar.vue'
import Footer from '@/components/common/Footer.vue'
import { getCases, getCasesCount, searchUniversities, getRecommendations } from '@/utils/api'

const mode = ref('browse')
const loading = ref(false)
const cases = ref([])
const total = ref(0)
const page = ref(1)
const pageSize = 12

const filters = ref({
  country: '',
  result: '',
  year: null,
  keyword: ''
})

// AI 推荐
const recommendLoading = ref(false)
const recommendations = ref([])
const profile = ref({
  undergraduate_university_name: '',
  undergraduate_major: '',
  gpa: null,
  gpa_scale: 4.0,
  ielts_overall: null,
  ielts_listening: null,
  ielts_reading: null,
  ielts_writing: null,
  ielts_speaking: null,
  toefl_total: null,
  toefl_reading: null,
  toefl_listening: null,
  toefl_speaking: null,
  toefl_writing: null,
  gre_total: null,
  gre_verbal: null,
  gre_quant: null,
  gre_writing: null,
  gmat_total: null,
  internship_count: 0,
  internship_experience: '',
  research_count: 0,
  research_experience: '',
  publication_count: 0,
  publications: '',
  work_years: 0,
  work_experience: '',
  extracurricular: '',
  awards: '',
  recommendation_strength: 'medium'
})

// 院校搜索选项
const univOptions = ref([])
const searchUniv = async (query) => {
  if (query.length < 1) { univOptions.value = []; return }
  try {
    const data = await searchUniversities(query)
    univOptions.value = data
  } catch { univOptions.value = [] }
}

// 加载案例
const loadCases = async () => {
  loading.value = true
  try {
    const params = {
      skip: (page.value - 1) * pageSize,
      limit: pageSize
    }
    if (filters.value.country) params.country = filters.value.country
    if (filters.value.result) params.result = filters.value.result
    if (filters.value.year) params.year = filters.value.year
    if (filters.value.keyword) params.keyword = filters.value.keyword

    const countParams = {}
    if (filters.value.country) countParams.country = filters.value.country
    if (filters.value.result) countParams.result = filters.value.result
    if (filters.value.year) countParams.year = filters.value.year
    if (filters.value.keyword) countParams.keyword = filters.value.keyword
    const [casesData, countData] = await Promise.all([
      getCases(params),
      getCasesCount(countParams)
    ])
    cases.value = casesData
    total.value = countData.total
  } catch (e) {
    console.error('加载案例失败', e)
  } finally {
    loading.value = false
  }
}

// AI 推荐
const doRecommend = async () => {
  recommendLoading.value = true
  try {
    const data = await getRecommendations(profile.value)
    recommendations.value = data
  } catch (e) {
    console.error('推荐失败', e)
  } finally {
    recommendLoading.value = false
  }
}

const resultTagType = (result) => {
  if (result === '录取') return 'success'
  if (result === '拒绝') return 'danger'
  if (result === '候补') return 'warning'
  return 'info'
}

const probClass = (prob) => {
  if (prob >= 70) return 'high'
  if (prob >= 40) return 'medium'
  return 'low'
}

onMounted(loadCases)
</script>

<style lang="scss" scoped>
@use '@/styles/variables.scss' as *;

.case-list-page {
  min-height: 100vh;
  background: #f5f7fa;
  padding-top: 70px;
}

.page-header {
  background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
  color: white;
  padding: 60px 0;
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

.container { max-width: 1200px; margin: 0 auto; padding: 0 20px; }

.mode-switch {
  text-align: center;
  margin: 24px 0;
}

/* ===== 筛选区 ===== */
.filter-section {
  background: white;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: $box-shadow;
}
.filter-row {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}
.filter-group {
  flex: 0 0 auto;
  label { display: block; font-size: 13px; color: $text-secondary; margin-bottom: 6px; }
  .el-select { width: 160px; }
  &.search-group { flex: 1; min-width: 200px; }
}

/* ===== 案例卡片 ===== */
.case-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(360px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

.case-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: $box-shadow;
  &:hover {
    transform: translateY(-4px);
    box-shadow: $box-shadow-lg;
  }
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}
.year-badge {
  font-size: 13px;
  color: $text-secondary;
  background: $secondary-color;
  padding: 2px 10px;
  border-radius: 12px;
}

.admitted-info {
  margin-bottom: 12px;
  .university-name {
    display: block;
    font-size: 18px;
    font-weight: 600;
    color: $primary-color;
  }
  .major-name {
    display: block;
    font-size: 14px;
    color: $text-secondary;
    margin-top: 4px;
  }
}

.applicant-info {
  margin-bottom: 12px;
  .info-row {
    display: flex;
    justify-content: space-between;
    font-size: 13px;
    padding: 4px 0;
    .label { color: $text-secondary; }
    .value { color: $text-primary; font-weight: 500; }
  }
}

.score-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-bottom: 8px;
}

.scholarship {
  font-size: 13px;
  color: $success-color;
  margin-top: 8px;
  .el-icon { vertical-align: middle; }
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px solid $border-color;
  font-size: 13px;
  color: $text-secondary;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin: 24px 0 40px;
}

/* ===== AI 推荐区 ===== */
.recommend-section {
  margin-bottom: 40px;
}

.recommend-form-card {
  background: white;
  border-radius: 16px;
  padding: 32px;
  box-shadow: $box-shadow;
  margin-bottom: 32px;
  h2 {
    font-size: 22px;
    margin-bottom: 4px;
    .el-icon { vertical-align: middle; color: $primary-light; }
  }
  .subtitle {
    color: $text-secondary;
    margin-bottom: 20px;
    font-size: 14px;
  }
}

.test-section {
  margin-bottom: 8px;
  padding: 16px 20px 0;
  background: #f9fafb;
  border-radius: 10px;
  border: 1px solid #f0f0f0;

  .test-label {
    font-size: 14px;
    font-weight: 600;
    color: $text-primary;
    margin-bottom: 12px;
    padding-left: 2px;
  }

  .score-row {
    display: flex;
    gap: 12px;

    .score-item {
      flex: 1;
      min-width: 0;
    }
  }
}

.form-actions {
  text-align: center;
  margin-top: 16px;
}

.recommend-results {
  h2 { font-size: 22px; margin-bottom: 4px; }
  .subtitle { color: $text-secondary; margin-bottom: 20px; }
}

.result-cards {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.result-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 20px;
  box-shadow: $box-shadow;
  transition: all 0.3s;
  &:hover { box-shadow: $box-shadow-lg; }
}

.rank-badge {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: $primary-light;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 16px;
  flex-shrink: 0;
}

.result-main {
  flex: 1;
  h3 { font-size: 18px; margin-bottom: 4px; color: $text-primary; }
  .major-name { font-size: 14px; color: $text-secondary; }
  .country-tag { font-size: 12px; color: $text-muted; }
}

.probability-circle {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  .prob-value { font-size: 20px; font-weight: 700; }
  .prob-label { font-size: 11px; opacity: 0.8; }
  &.high { background: rgba(16,185,129,0.12); color: $success-color; }
  &.medium { background: rgba(245,158,11,0.12); color: $warning-color; }
  &.low { background: rgba(239,68,68,0.12); color: $error-color; }
}

.result-stats {
  display: flex;
  gap: 16px;
  flex-shrink: 0;
  .stat {
    text-align: center;
    .stat-num { display: block; font-size: 16px; font-weight: 600; color: $text-primary; }
    .stat-label { display: block; font-size: 11px; color: $text-muted; }
  }
}

.empty-state { padding: 60px 0; text-align: center; }

@media (max-width: 768px) {
  .case-cards { grid-template-columns: 1fr; }
  .result-card { flex-direction: column; text-align: center; }
  .result-stats { flex-wrap: wrap; justify-content: center; }
}
</style>

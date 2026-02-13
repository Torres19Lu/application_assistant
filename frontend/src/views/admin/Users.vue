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
          <h2>用户管理</h2>
          <el-button type="primary" @click="openCreateDialog">
            <el-icon><Plus /></el-icon> 添加用户
          </el-button>
        </el-header>

        <el-main>
          <!-- 搜索和筛选 -->
          <el-card class="filter-card" shadow="never">
            <div class="filter-row">
              <el-input
                v-model="filters.keyword"
                placeholder="搜索邮箱、昵称、手机号"
                clearable
                style="width: 280px"
                @keyup.enter="handleSearch"
                @clear="handleSearch"
              >
                <template #prefix><el-icon><Search /></el-icon></template>
              </el-input>
              <el-select v-model="filters.role" placeholder="全部角色" clearable style="width: 140px" @change="handleSearch">
                <el-option label="管理员" value="admin" />
                <el-option label="普通用户" value="user" />
              </el-select>
              <el-select v-model="filters.status" placeholder="全部状态" clearable style="width: 140px" @change="handleSearch">
                <el-option label="正常" value="active" />
                <el-option label="已禁用" value="disabled" />
              </el-select>
              <el-button type="primary" @click="handleSearch">
                <el-icon><Search /></el-icon> 搜索
              </el-button>
              <el-button @click="resetFilters">重置</el-button>
            </div>
          </el-card>

          <!-- 用户数量统计 -->
          <div class="stat-bar">
            <span>共 <strong>{{ total }}</strong> 个用户</span>
          </div>

          <!-- 用户表格 -->
          <el-card shadow="never">
            <el-table :data="users" v-loading="loading" border stripe>
              <el-table-column prop="id" label="ID" width="70" align="center" />
              <el-table-column label="用户信息" min-width="220">
                <template #default="{ row }">
                  <div class="user-info-cell">
                    <el-avatar :size="36" :src="row.avatar ? getAvatarUrl(row.avatar) : undefined">
                      {{ (row.nickname || row.email).charAt(0).toUpperCase() }}
                    </el-avatar>
                    <div class="user-meta">
                      <span class="nickname">{{ row.nickname || '未设置' }}</span>
                      <span class="email">{{ row.email }}</span>
                    </div>
                  </div>
                </template>
              </el-table-column>
              <el-table-column prop="phone" label="手机号" width="140">
                <template #default="{ row }">
                  {{ row.phone || '-' }}
                </template>
              </el-table-column>
              <el-table-column prop="role" label="角色" width="110" align="center">
                <template #default="{ row }">
                  <el-tag :type="row.role === 'admin' ? 'danger' : ''" effect="dark" size="small">
                    {{ row.role === 'admin' ? '管理员' : '普通用户' }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="is_active" label="状态" width="90" align="center">
                <template #default="{ row }">
                  <el-tag :type="row.is_active ? 'success' : 'info'" size="small">
                    {{ row.is_active ? '正常' : '禁用' }}
                  </el-tag>
                </template>
              </el-table-column>
              <el-table-column label="目标信息" min-width="160">
                <template #default="{ row }">
                  <div v-if="row.target_country || row.target_major" class="target-info">
                    <span v-if="row.target_country">{{ row.target_country }}</span>
                    <span v-if="row.target_country && row.target_major"> · </span>
                    <span v-if="row.target_major">{{ row.target_major }}</span>
                  </div>
                  <span v-else style="color: #999">未设置</span>
                </template>
              </el-table-column>
              <el-table-column label="注册时间" width="170" align="center">
                <template #default="{ row }">
                  {{ formatDate(row.created_at) }}
                </template>
              </el-table-column>
              <el-table-column label="最近登录" width="170" align="center">
                <template #default="{ row }">
                  {{ row.last_login ? formatDate(row.last_login) : '从未登录' }}
                </template>
              </el-table-column>
              <el-table-column label="操作" width="260" fixed="right" align="center">
                <template #default="{ row }">
                  <el-button size="small" @click="openEditDialog(row)">
                    <el-icon><Edit /></el-icon> 编辑
                  </el-button>
                  <el-dropdown trigger="click" @command="(cmd) => handleCommand(cmd, row)" style="margin-left: 8px">
                    <el-button size="small">
                      更多 <el-icon class="el-icon--right"><ArrowDown /></el-icon>
                    </el-button>
                    <template #dropdown>
                      <el-dropdown-menu>
                        <el-dropdown-item command="toggleRole" :disabled="isSelf(row)">
                          <el-icon><Switch /></el-icon>
                          {{ row.role === 'admin' ? '取消管理员' : '设为管理员' }}
                        </el-dropdown-item>
                        <el-dropdown-item command="resetPassword">
                          <el-icon><Key /></el-icon> 重置密码
                        </el-dropdown-item>
                        <el-dropdown-item :command="row.is_active ? 'disable' : 'enable'" :disabled="isSelf(row)" divided>
                          <el-icon><CircleClose /></el-icon>
                          {{ row.is_active ? '禁用账号' : '启用账号' }}
                        </el-dropdown-item>
                        <el-dropdown-item command="delete" :disabled="isSelf(row)" style="color: #f56c6c">
                          <el-icon><Delete /></el-icon> 删除用户
                        </el-dropdown-item>
                      </el-dropdown-menu>
                    </template>
                  </el-dropdown>
                </template>
              </el-table-column>
            </el-table>

            <div class="pagination">
              <el-pagination
                v-model:current-page="currentPage"
                v-model:page-size="pageSize"
                :total="total"
                :page-sizes="[10, 20, 50]"
                layout="total, sizes, prev, pager, next"
                @size-change="fetchUsers"
                @current-change="fetchUsers"
              />
            </div>
          </el-card>
        </el-main>
      </el-container>
    </el-container>

    <!-- 创建用户对话框 -->
    <el-dialog v-model="createDialogVisible" title="添加用户" width="520px" destroy-on-close>
      <el-form :model="createForm" :rules="createRules" ref="createFormRef" label-width="80px">
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="createForm.email" placeholder="请输入邮箱地址" />
        </el-form-item>
        <el-form-item label="密码" prop="password">
          <el-input v-model="createForm.password" type="password" show-password placeholder="至少6位密码" />
        </el-form-item>
        <el-form-item label="昵称" prop="nickname">
          <el-input v-model="createForm.nickname" placeholder="可选，默认使用邮箱前缀" />
        </el-form-item>
        <el-form-item label="手机号">
          <el-input v-model="createForm.phone" placeholder="可选" />
        </el-form-item>
        <el-form-item label="角色">
          <el-radio-group v-model="createForm.role">
            <el-radio value="user">普通用户</el-radio>
            <el-radio value="admin">管理员</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="createDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitCreate" :loading="submitting">确认创建</el-button>
      </template>
    </el-dialog>

    <!-- 编辑用户对话框 -->
    <el-dialog v-model="editDialogVisible" title="编辑用户" width="520px" destroy-on-close>
      <el-form :model="editForm" :rules="editRules" ref="editFormRef" label-width="80px">
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="editForm.email" />
        </el-form-item>
        <el-form-item label="昵称">
          <el-input v-model="editForm.nickname" />
        </el-form-item>
        <el-form-item label="手机号">
          <el-input v-model="editForm.phone" />
        </el-form-item>
        <el-form-item label="角色">
          <el-radio-group v-model="editForm.role" :disabled="isSelf(editingUser)">
            <el-radio value="user">普通用户</el-radio>
            <el-radio value="admin">管理员</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="目标国家">
          <el-input v-model="editForm.target_country" placeholder="如：英国" />
        </el-form-item>
        <el-form-item label="目标专业">
          <el-input v-model="editForm.target_major" placeholder="如：计算机科学" />
        </el-form-item>
        <el-form-item label="状态">
          <el-switch
            v-model="editForm.is_active"
            :active-value="1"
            :inactive-value="0"
            active-text="正常"
            inactive-text="禁用"
            :disabled="isSelf(editingUser)"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="editDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submitEdit" :loading="submitting">保存修改</el-button>
      </template>
    </el-dialog>

    <!-- 重置密码对话框 -->
    <el-dialog v-model="resetPwdVisible" title="重置密码" width="420px" destroy-on-close>
      <p style="margin-bottom: 16px; color: #606266">
        即将为用户 <strong>{{ resetPwdUser?.nickname || resetPwdUser?.email }}</strong> 重置密码
      </p>
      <el-form :model="resetPwdForm" ref="resetPwdFormRef" label-width="80px">
        <el-form-item label="新密码" prop="new_password" :rules="[{ required: true, message: '请输入新密码', trigger: 'blur' }, { min: 6, message: '密码至少6位', trigger: 'blur' }]">
          <el-input v-model="resetPwdForm.new_password" type="password" show-password placeholder="输入新密码，至少6位" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="resetPwdVisible = false">取消</el-button>
        <el-button type="warning" @click="submitResetPassword" :loading="submitting">确认重置</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { School, DataLine, Reading, Document, User, HomeFilled, FolderOpened, Plus, Search, Edit, Delete, ArrowDown, Switch, Key, CircleClose } from '@element-plus/icons-vue'
import { getUsers, getUsersCount, createUser, updateUser, toggleUserStatus, resetUserPassword, deleteUser } from '@/utils/api'
import { useUserStore } from '@/stores/user'

const route = useRoute()
const userStore = useUserStore()

const loading = ref(false)
const submitting = ref(false)
const users = ref([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)

const filters = reactive({ keyword: '', role: '', status: '' })

const isSelf = (row) => {
  if (!row) return false
  return row.id === userStore.userInfo?.id
}

const getAvatarUrl = (avatar) => {
  if (!avatar) return ''
  if (avatar.startsWith('http')) return avatar
  return `http://localhost:8000${avatar}`
}

const fetchUsers = async () => {
  loading.value = true
  try {
    const params = {
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value,
    }
    if (filters.keyword) params.keyword = filters.keyword
    if (filters.role) params.role = filters.role
    if (filters.status) params.status = filters.status

    const [res, countRes] = await Promise.all([
      getUsers(params),
      getUsersCount(params)
    ])
    users.value = Array.isArray(res) ? res : []
    total.value = countRes?.total || 0
  } catch (error) {
    ElMessage.error('获取用户列表失败')
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  currentPage.value = 1
  fetchUsers()
}

const resetFilters = () => {
  filters.keyword = ''
  filters.role = ''
  filters.status = ''
  currentPage.value = 1
  fetchUsers()
}

// ========== 创建用户 ==========
const createDialogVisible = ref(false)
const createFormRef = ref(null)
const createForm = ref({
  email: '',
  password: '',
  nickname: '',
  phone: '',
  role: 'user'
})

const createRules = {
  email: [{ required: true, message: '请输入邮箱', trigger: 'blur' }, { type: 'email', message: '请输入有效邮箱', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }, { min: 6, message: '密码至少6位', trigger: 'blur' }]
}

const openCreateDialog = () => {
  createForm.value = { email: '', password: '', nickname: '', phone: '', role: 'user' }
  createDialogVisible.value = true
}

const submitCreate = async () => {
  const valid = await createFormRef.value?.validate().catch(() => false)
  if (!valid) return

  submitting.value = true
  try {
    await createUser(createForm.value)
    ElMessage.success('用户创建成功')
    createDialogVisible.value = false
    fetchUsers()
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '创建失败')
  } finally {
    submitting.value = false
  }
}

// ========== 编辑用户 ==========
const editDialogVisible = ref(false)
const editFormRef = ref(null)
const editingUser = ref(null)
const editForm = ref({})

const editRules = {
  email: [{ required: true, message: '请输入邮箱', trigger: 'blur' }, { type: 'email', message: '请输入有效邮箱', trigger: 'blur' }]
}

const openEditDialog = (row) => {
  editingUser.value = row
  editForm.value = {
    email: row.email,
    nickname: row.nickname,
    phone: row.phone || '',
    role: row.role,
    target_country: row.target_country || '',
    target_major: row.target_major || '',
    is_active: row.is_active ? 1 : 0
  }
  editDialogVisible.value = true
}

const submitEdit = async () => {
  const valid = await editFormRef.value?.validate().catch(() => false)
  if (!valid) return

  submitting.value = true
  try {
    await updateUser(editingUser.value.id, editForm.value)
    ElMessage.success('用户信息已更新')
    editDialogVisible.value = false
    fetchUsers()
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '更新失败')
  } finally {
    submitting.value = false
  }
}

// ========== 重置密码 ==========
const resetPwdVisible = ref(false)
const resetPwdFormRef = ref(null)
const resetPwdUser = ref(null)
const resetPwdForm = ref({ new_password: '' })

const openResetPwdDialog = (row) => {
  resetPwdUser.value = row
  resetPwdForm.value = { new_password: '' }
  resetPwdVisible.value = true
}

const submitResetPassword = async () => {
  const valid = await resetPwdFormRef.value?.validate().catch(() => false)
  if (!valid) return

  submitting.value = true
  try {
    await resetUserPassword(resetPwdUser.value.id, resetPwdForm.value)
    ElMessage.success('密码已重置')
    resetPwdVisible.value = false
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '重置失败')
  } finally {
    submitting.value = false
  }
}

// ========== 更多操作下拉菜单 ==========
const handleCommand = (cmd, row) => {
  switch (cmd) {
    case 'toggleRole':
      confirmToggleRole(row)
      break
    case 'resetPassword':
      openResetPwdDialog(row)
      break
    case 'enable':
    case 'disable':
      confirmToggleStatus(row)
      break
    case 'delete':
      confirmDelete(row)
      break
  }
}

const confirmToggleRole = (row) => {
  const newRole = row.role === 'admin' ? '普通用户' : '管理员'
  ElMessageBox.confirm(
    `确定要将 ${row.nickname || row.email} 设为「${newRole}」吗？`,
    '角色变更',
    { type: 'warning' }
  ).then(async () => {
    try {
      const roleValue = row.role === 'admin' ? 'user' : 'admin'
      await updateUser(row.id, { role: roleValue })
      ElMessage.success(`已设为${newRole}`)
      fetchUsers()
    } catch (error) {
      ElMessage.error(error.response?.data?.detail || '操作失败')
    }
  }).catch(() => {})
}

const confirmToggleStatus = (row) => {
  const action = row.is_active ? '禁用' : '启用'
  ElMessageBox.confirm(
    `确定要${action}用户 ${row.nickname || row.email} 吗？`,
    '提示',
    { type: 'warning' }
  ).then(async () => {
    try {
      await toggleUserStatus(row.id)
      ElMessage.success(`${action}成功`)
      fetchUsers()
    } catch (error) {
      ElMessage.error(error.response?.data?.detail || `${action}失败`)
    }
  }).catch(() => {})
}

const confirmDelete = (row) => {
  ElMessageBox.confirm(
    `确定要永久删除用户 ${row.nickname || row.email} 吗？\n该操作不可恢复！`,
    '删除确认',
    { type: 'error', confirmButtonText: '确认删除', confirmButtonClass: 'el-button--danger' }
  ).then(async () => {
    try {
      await deleteUser(row.id)
      ElMessage.success('用户已删除')
      fetchUsers()
    } catch (error) {
      ElMessage.error(error.response?.data?.detail || '删除失败')
    }
  }).catch(() => {})
}

const formatDate = (date) => {
  if (!date) return ''
  return new Date(date).toLocaleString('zh-CN')
}

onMounted(fetchUsers)
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
    font-size: 18px;
  }
}

.el-main {
  background: #f5f7fa;
  margin-left: 220px;
  padding: 20px;
}

.filter-card {
  margin-bottom: 16px;

  .filter-row {
    display: flex;
    align-items: center;
    gap: 12px;
    flex-wrap: wrap;
  }
}

.stat-bar {
  margin-bottom: 12px;
  font-size: 14px;
  color: #606266;

  strong {
    color: #1e40af;
  }
}

.user-info-cell {
  display: flex;
  align-items: center;
  gap: 10px;

  .user-meta {
    display: flex;
    flex-direction: column;
    line-height: 1.4;

    .nickname {
      font-weight: 600;
      color: #303133;
      font-size: 14px;
    }

    .email {
      color: #909399;
      font-size: 12px;
    }
  }
}

.target-info {
  font-size: 13px;
  color: #606266;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>

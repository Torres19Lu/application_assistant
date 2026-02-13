<template>
  <div class="profile-page">
    <NavBar />
    
    <div class="page-content">
      <!-- 头像卡片 -->
      <el-card class="avatar-card">
        <div class="avatar-section">
          <div class="avatar-wrapper" @click="triggerFileInput">
            <el-avatar :size="100" :src="avatarUrl" :icon="UserFilled" class="user-avatar" />
            <div class="avatar-overlay">
              <el-icon size="24"><Camera /></el-icon>
              <span>更换头像</span>
            </div>
          </div>
          <input
            ref="fileInputRef"
            type="file"
            accept="image/jpeg,image/png,image/gif,image/webp"
            style="display: none"
            @change="handleFileChange"
          />
          <div class="user-meta">
            <h2>{{ userStore.userInfo?.nickname || '用户' }}</h2>
            <p>{{ userStore.userInfo?.email }}</p>
            <el-tag v-if="userStore.isAdmin" type="danger" size="small">管理员</el-tag>
            <el-tag v-else type="success" size="small">普通用户</el-tag>
          </div>
        </div>
      </el-card>

      <!-- 个人信息卡片 -->
      <el-card class="profile-card">
        <template #header>
          <div class="card-header">
            <h2>个人信息</h2>
          </div>
        </template>
      
        <el-form :model="form" label-width="100px" class="profile-form">
          <el-form-item label="邮箱">
            <el-input v-model="form.email" disabled />
          </el-form-item>
        
          <el-form-item label="昵称">
            <el-input v-model="form.nickname" placeholder="请输入昵称" />
          </el-form-item>
        
          <el-form-item label="手机号">
            <el-input v-model="form.phone" placeholder="请输入手机号" />
          </el-form-item>
        
          <el-form-item label="目标国家">
            <el-select v-model="form.target_country" placeholder="请选择目标国家" style="width: 100%">
              <el-option label="美国" value="美国" />
              <el-option label="英国" value="英国" />
              <el-option label="加拿大" value="加拿大" />
              <el-option label="澳大利亚" value="澳大利亚" />
              <el-option label="新加坡" value="新加坡" />
              <el-option label="中国香港" value="中国香港" />
              <el-option label="日本" value="日本" />
              <el-option label="瑞士" value="瑞士" />
              <el-option label="其他" value="其他" />
            </el-select>
          </el-form-item>
        
          <el-form-item label="目标专业">
            <el-input v-model="form.target_major" placeholder="请输入目标专业" />
          </el-form-item>
        
          <el-form-item>
            <el-button type="primary" @click="saveProfile">保存修改</el-button>
            <el-button @click="resetForm">重置</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    
      <!-- 修改密码卡片 -->
      <el-card class="password-card">
        <template #header>
          <div class="card-header">
            <h3>修改密码</h3>
          </div>
        </template>
      
        <el-form :model="passwordForm" label-width="120px" :rules="passwordRules" ref="passwordFormRef">
          <el-form-item label="当前密码" prop="old_password">
            <el-input v-model="passwordForm.old_password" type="password" show-password />
          </el-form-item>
        
          <el-form-item label="新密码" prop="new_password">
            <el-input v-model="passwordForm.new_password" type="password" show-password />
          </el-form-item>
        
          <el-form-item label="确认新密码" prop="confirm_password">
            <el-input v-model="passwordForm.confirm_password" type="password" show-password />
          </el-form-item>
        
          <el-form-item>
            <el-button type="primary" @click="changePassword">修改密码</el-button>
          </el-form-item>
        </el-form>
      </el-card>
    </div>
    
    <Footer />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { UserFilled, Camera } from '@element-plus/icons-vue'
import { useUserStore } from '@/stores/user'
import { updateUserProfile, changeUserPassword, uploadAvatar } from '@/utils/api'
import NavBar from '@/components/common/NavBar.vue'
import Footer from '@/components/common/Footer.vue'

const userStore = useUserStore()
const passwordFormRef = ref(null)
const fileInputRef = ref(null)

const avatarUrl = computed(() => {
  const avatar = userStore.userInfo?.avatar
  if (avatar) {
    // 如果是相对路径，加上后端地址
    return avatar.startsWith('http') ? avatar : `http://localhost:8000${avatar}`
  }
  return ''
})

const form = ref({
  email: '',
  nickname: '',
  phone: '',
  target_country: '',
  target_major: ''
})

const passwordForm = ref({
  old_password: '',
  new_password: '',
  confirm_password: ''
})

const passwordRules = {
  old_password: [{ required: true, message: '请输入当前密码', trigger: 'blur' }],
  new_password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 8, message: '密码长度至少8位', trigger: 'blur' }
  ],
  confirm_password: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== passwordForm.value.new_password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

const triggerFileInput = () => {
  fileInputRef.value.click()
}

const handleFileChange = async (e) => {
  const file = e.target.files[0]
  if (!file) return
  
  // 验证文件大小 (5MB)
  if (file.size > 5 * 1024 * 1024) {
    ElMessage.error('图片大小不能超过5MB')
    return
  }
  
  try {
    await uploadAvatar(file)
    ElMessage.success('头像上传成功')
    await userStore.fetchUserInfo()
  } catch (error) {
    ElMessage.error('头像上传失败')
  } finally {
    // 清空 input 以便再次选择同一文件
    fileInputRef.value.value = ''
  }
}

const fetchUserProfile = () => {
  const user = userStore.userInfo
  if (user) {
    form.value = {
      email: user.email,
      nickname: user.nickname || '',
      phone: user.phone || '',
      target_country: user.target_country || '',
      target_major: user.target_major || ''
    }
  }
}

const saveProfile = async () => {
  try {
    await updateUserProfile(form.value)
    ElMessage.success('保存成功')
    await userStore.fetchUserInfo()
  } catch (error) {
    ElMessage.error('保存失败')
  }
}

const resetForm = () => {
  fetchUserProfile()
}

const changePassword = async () => {
  passwordFormRef.value.validate(async (valid) => {
    if (valid) {
      try {
        await changeUserPassword(passwordForm.value)
        ElMessage.success('密码修改成功')
        passwordForm.value = {
          old_password: '',
          new_password: '',
          confirm_password: ''
        }
      } catch (error) {
        ElMessage.error('密码修改失败')
      }
    }
  })
}

onMounted(() => {
  fetchUserProfile()
})

watch(() => userStore.userInfo, (newVal) => {
  if (newVal) {
    fetchUserProfile()
  }
})
</script>

<style scoped lang="scss">
.profile-page {
  min-height: 100vh;
  background: #f5f7fa;
  padding-top: 70px;
}

.page-content {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.avatar-card {
  margin-bottom: 20px;
}

.avatar-section {
  display: flex;
  align-items: center;
  gap: 24px;
  padding: 10px 0;
}

.avatar-wrapper {
  position: relative;
  cursor: pointer;
  border-radius: 50%;
  overflow: hidden;
  flex-shrink: 0;
  
  .user-avatar {
    display: block;
    background: linear-gradient(135deg, #1e40af, #3b82f6);
  }
  
  .avatar-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    color: white;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 4px;
    opacity: 0;
    transition: opacity 0.3s;
    border-radius: 50%;
    
    span {
      font-size: 12px;
    }
  }
  
  &:hover .avatar-overlay {
    opacity: 1;
  }
}

.user-meta {
  h2 {
    margin: 0 0 4px 0;
    font-size: 22px;
    color: #1e293b;
  }
  
  p {
    margin: 0 0 8px 0;
    color: #64748b;
    font-size: 14px;
  }
}

.profile-card,
.password-card {
  margin-bottom: 20px;
}

.card-header {
  h2, h3 {
    margin: 0;
  }
}

.profile-form {
  max-width: 500px;
}
</style>

<template>
  <div class="auth-page">
    <div class="auth-container">
      <div class="auth-left">
        <div class="brand">
          <el-icon size="48" color="white"><School /></el-icon>
          <h1>xmum留学</h1>
        </div>
        <p class="slogan">全球院校信息 · 专业录取数据 · 申请攻略指南</p>
        <div class="features">
          <div class="feature">
            <el-icon><Check /></el-icon>
            <span>海量院校专业数据</span>
          </div>
          <div class="feature">
            <el-icon><Check /></el-icon>
            <span>智能申请规划</span>
          </div>
          <div class="feature">
            <el-icon><Check /></el-icon>
            <span>独家申请攻略</span>
          </div>
        </div>
      </div>
      
      <div class="auth-right">
        <div class="auth-form">
          <div class="back-link">
            <el-button link @click="goHome">
              <el-icon><ArrowLeft /></el-icon>
              返回首页
            </el-button>
          </div>
          <h2>欢迎回来</h2>
          <p class="subtitle">登录您的账户继续</p>
          
          <el-form
            ref="formRef"
            :model="form"
            :rules="rules"
            @keyup.enter="handleSubmit"
          >
            <el-form-item prop="email">
              <el-input
                v-model="form.email"
                placeholder="邮箱地址"
                size="large"
                :prefix-icon="Message"
              />
            </el-form-item>
            
            <el-form-item prop="password">
              <el-input
                v-model="form.password"
                type="password"
                placeholder="密码"
                size="large"
                :prefix-icon="Lock"
                show-password
              />
            </el-form-item>
            
            <div class="form-options">
              <el-checkbox v-model="rememberMe">记住我</el-checkbox>
              <a href="#" class="forgot-link">忘记密码？</a>
            </div>
            
            <el-button
              type="primary"
              size="large"
              :loading="loading"
              @click="handleSubmit"
              class="submit-btn"
            >
              登录
            </el-button>
          </el-form>
          
          <div class="auth-footer">
            <p>还没有账户？ <router-link to="/register">立即注册</router-link></p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()
const formRef = ref(null)
const loading = ref(false)
const rememberMe = ref(false)

const form = reactive({
  email: '',
  password: ''
})

const rules = {
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 8, message: '密码至少8位', trigger: 'blur' }
  ]
}

const goHome = () => {
  router.push('/')
}

const handleSubmit = async () => {
  const valid = await formRef.value.validate().catch(() => false)
  if (!valid) return
  
  loading.value = true
  try {
    await userStore.loginUser({
      username: form.email,
      password: form.password
    })
    ElMessage.success('登录成功')
    router.push('/')
  } catch (error) {
    console.error('登录失败:', error)
  } finally {
    loading.value = false
  }
}
</script>

<style lang="scss" scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f7fa;
  padding: 20px;
}

.auth-container {
  display: flex;
  width: 100%;
  max-width: 1000px;
  min-height: 600px;
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
}

.auth-left {
  flex: 1;
  background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
  padding: 60px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  color: white;
  
  .brand {
    display: flex;
    align-items: center;
    gap: 16px;
    margin-bottom: 24px;
    
    h1 {
      font-size: 28px;
      font-weight: 700;
    }
  }
  
  .slogan {
    font-size: 16px;
    opacity: 0.9;
    margin-bottom: 40px;
  }
  
  .features {
    .feature {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 16px;
      font-size: 15px;
      
      .el-icon {
        background: rgba(255, 255, 255, 0.2);
        border-radius: 50%;
        padding: 4px;
      }
    }
  }
}

.auth-right {
  flex: 1;
  padding: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.auth-form {
  width: 100%;
  max-width: 360px;
  
  .back-link {
    margin-bottom: 16px;
    
    .el-button {
      color: #6b7280;
      
      &:hover {
        color: #1e40af;
      }
    }
  }
  
  h2 {
    font-size: 28px;
    font-weight: 700;
    color: $text-primary;
    margin-bottom: 8px;
  }
  
  .subtitle {
    color: $text-secondary;
    margin-bottom: 32px;
  }
  
  .form-options {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 24px;
    
    .forgot-link {
      color: $primary-color;
      text-decoration: none;
      font-size: 14px;
      
      &:hover {
        text-decoration: underline;
      }
    }
  }
  
  .submit-btn {
    width: 100%;
    height: 48px;
    font-size: 16px;
    border-radius: 8px;
  }
}

.auth-footer {
  margin-top: 32px;
  text-align: center;
  color: $text-secondary;
  font-size: 14px;
  
  a {
    color: $primary-color;
    text-decoration: none;
    font-weight: 500;
    
    &:hover {
      text-decoration: underline;
    }
  }
}

@media (max-width: 768px) {
  .auth-left {
    display: none;
  }
  
  .auth-right {
    padding: 40px 24px;
  }
}
</style>

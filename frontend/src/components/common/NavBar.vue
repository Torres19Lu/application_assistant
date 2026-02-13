<template>
  <nav class="navbar" :class="{ 'scrolled': isScrolled }">
    <div class="container">
      <div class="navbar-content">
        <router-link to="/" class="logo">
          <el-icon size="28" color="#1e40af"><School /></el-icon>
          <span>xmum留学</span>
        </router-link>
        
        <div class="nav-links">
          <router-link to="/" :class="{ active: $route.path === '/' }">首页</router-link>
          <router-link to="/universities" :class="{ active: $route.path.startsWith('/universities') }">院校库</router-link>
          <router-link to="/majors" :class="{ active: $route.path.startsWith('/majors') }">专业库</router-link>
          <router-link to="/guides" :class="{ active: $route.path.startsWith('/guides') }">申请攻略</router-link>
          <router-link to="/cases" :class="{ active: $route.path.startsWith('/cases') }">录取案例</router-link>
        </div>
        
        <div class="nav-actions">
          <template v-if="userStore.isAuthenticated">
            <router-link to="/favorites" class="action-link">
              <el-icon><Star /></el-icon>
              <span>我的收藏</span>
            </router-link>
            <el-dropdown @command="handleCommand" trigger="click">
              <span class="user-info">
                <el-avatar :size="32" :src="avatarUrl" :icon="UserFilled" />
                <span class="nickname">{{ userStore.userInfo?.nickname || '用户' }}</span>
                <el-icon><ArrowDown /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="profile">个人中心</el-dropdown-item>
                  <el-dropdown-item v-if="userStore.isAdmin" command="admin">后台管理</el-dropdown-item>
                  <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
          <template v-else>
            <router-link to="/login" class="login-btn">登录</router-link>
            <router-link to="/register" class="register-btn">注册</router-link>
          </template>
        </div>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/user'
import { ElMessage } from 'element-plus'

const router = useRouter()
const userStore = useUserStore()
const isScrolled = ref(false)

const avatarUrl = computed(() => {
  const avatar = userStore.userInfo?.avatar
  if (avatar) {
    return avatar.startsWith('http') ? avatar : `http://localhost:8000${avatar}`
  }
  return ''
})

const handleScroll = () => {
  isScrolled.value = window.scrollY > 50
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})

const handleCommand = (command) => {
  console.log('Dropdown command:', command)
  switch (command) {
    case 'profile':
      router.push('/profile')
      break
    case 'admin':
      router.push('/admin')
      break
    case 'logout':
      userStore.logout()
      ElMessage.success('已退出登录')
      router.push('/')
      break
  }
}
</script>

<style lang="scss" scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
  border-bottom: 1px solid transparent;
  
  &.scrolled {
    box-shadow: 0 2px 20px rgba(0, 0, 0, 0.08);
    border-bottom-color: #e5e7eb;
  }
}

.navbar-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 70px;
}

.logo {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  
  span {
    font-size: 20px;
    font-weight: 700;
    color: $primary-color;
  }
}

.nav-links {
  display: flex;
  gap: 32px;
  
  a {
    text-decoration: none;
    color: $text-primary;
    font-size: 15px;
    font-weight: 500;
    padding: 8px 0;
    position: relative;
    transition: color 0.3s;
    
    &:hover,
    &.active {
      color: $primary-color;
      
      &::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: $primary-color;
        border-radius: 2px;
      }
    }
  }
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 20px;
  
  .action-link {
    display: flex;
    align-items: center;
    gap: 6px;
    text-decoration: none;
    color: $text-secondary;
    font-size: 14px;
    transition: color 0.3s;
    
    &:hover {
      color: $primary-color;
    }
  }
  
  .user-info {
    display: flex;
    align-items: center;
    gap: 8px;
    cursor: pointer;
    padding: 4px 8px;
    border-radius: 20px;
    transition: background 0.3s;
    
    &:hover {
      background: #f3f4f6;
    }
    
    .nickname {
      font-size: 14px;
      color: $text-primary;
      max-width: 100px;
      overflow: hidden;
      text-overflow: ellipsis;
      white-space: nowrap;
    }
  }
  
  .login-btn,
  .register-btn {
    text-decoration: none;
    padding: 8px 20px;
    border-radius: 20px;
    font-size: 14px;
    font-weight: 500;
    transition: all 0.3s;
  }
  
  .login-btn {
    color: $primary-color;
    
    &:hover {
      background: rgba(30, 64, 175, 0.1);
    }
  }
  
  .register-btn {
    background: $primary-color;
    color: white;
    
    &:hover {
      background: $primary-dark;
    }
  }
}
</style>

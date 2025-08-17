<template>
  <header class="site-header glass">
    <img src="@/assets/ai-face-demo.png" alt="logo" class="logo" />
    <span class="site-title">Advanced Face Age Recognition</span>
    <div class="header-actions">
      <el-button
          v-if="!isLogin"
          class="fancy-btn"
          type="primary"
          icon="el-icon-user"
          @click="router.push('/login')"
      >Login</el-button>
      <el-button
          v-if="!isLogin"
          class="fancy-btn"
          type="primary"
          icon="el-icon-edit"
          @click="router.push('/register')"
      >Register</el-button>
      <el-button
          v-if="isLogin"
          class="fancy-btn"
          type="success"
          icon="el-icon-unlock"
          @click="logout"
      >Logout</el-button>
      <el-button
          class="fancy-btn admin"
          type="info"
          icon="el-icon-setting"
          @click="router.push('/admin')"
      >Admin System</el-button>
    </div>
  </header>
</template>

<script setup lang="ts">
import { useUserStore } from '@/store/user'
import { useRouter } from 'vue-router'
const store = useUserStore()
const router = useRouter()
const isLogin = store.isLogin
function logout() {
  store.logout()
  router.push('/')
}
</script>

<style scoped>
.site-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 18px 38px;
  position: relative;
  z-index: 10;
  box-shadow: 0 6px 28px #c9abff44;
  border-radius: 14px;
  background: rgba(34, 16, 58, 0.85);
  /* glassmorphism effect */
  backdrop-filter: blur(8px) saturate(120%);
}

.logo {
  height: 44px;
  margin-right: 18px;
  filter: drop-shadow(0 0 12px #ad69f8);
}

.site-title {
  font-size: 1.52rem;
  font-weight: bold;
  background: linear-gradient(90deg, #bcaaff 20%, #d88cff 60%, #7ae7ff 100%);
  -webkit-background-clip: text;
  color: transparent;
  text-shadow: 0 2px 20px #4e2179c0;
  margin-right: 26px;
  letter-spacing: 1px;
}

.header-actions {
  margin-left: auto;
  display: flex;
  gap: 14px;
}

.fancy-btn {
  font-weight: bold;
  letter-spacing: 0.02em;
  border-radius: 8px;
  transition: box-shadow 0.25s, background 0.25s, transform 0.15s;
  box-shadow: 0 4px 22px #7c41e822, 0 1px 3px #0003;
  background: linear-gradient(90deg, #925cff 0%, #8e75e2 80%);
}

.fancy-btn:hover {
  background: linear-gradient(90deg, #8d2eff 0%, #62e6ff 100%);
  box-shadow: 0 6px 36px #a36aff88, 0 2px 8px #58d1fd33;
  transform: translateY(-2px) scale(1.04);
  color: #fff !important;
}

.fancy-btn.admin {
  background: linear-gradient(90deg, #313176 0%, #a74fff 100%);
  color: #f4f4ff;
}

.fancy-btn.admin:hover {
  background: linear-gradient(90deg, #a74fff 0%, #4ee9e9 100%);
  box-shadow: 0 8px 36px #6b30a966, 0 3px 12px #54cfff66;
  color: #fff;
}
</style>

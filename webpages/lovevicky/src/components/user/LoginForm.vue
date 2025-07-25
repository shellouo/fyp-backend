<template>
  <div class="login-form">
    <h2>Login to Your Account</h2>
    <el-form :model="form" :rules="rules" ref="formRef" label-position="top">
      <el-form-item label="Username" prop="username">
        <el-input v-model="form.username" placeholder="Enter your username" />
      </el-form-item>
      <el-form-item label="Password" prop="password">
        <el-input v-model="form.password" type="password" placeholder="Enter your password" />
      </el-form-item>
      <div class="actions">
        <el-button
            type="primary"
            :loading="loading"
            class="login-btn"
            @click="handleLogin"
        >Login</el-button>
      </div>
      <div class="options">
        <span class="forgot" @click="handleForgot">Forgot password?</span>
        <span class="register" @click="$emit('switchToRegister')">Register here</span>
      </div>
      <el-alert v-if="error" type="error" :closable="false" :title="error" show-icon style="margin-top:8px" />
    </el-form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElForm } from 'element-plus'
import { useUserStore } from '@/store/user'

const form = ref({
  username: '',
  password: ''
})
const rules = {
  username: [{ required: true, message: 'Please enter username', trigger: 'blur' }],
  password: [{ required: true, message: 'Please enter password', trigger: 'blur' }]
}
const formRef = ref<InstanceType<typeof ElForm> | null>(null)
const loading = ref(false)
const error = ref('')

const store = useUserStore()

function handleLogin() {
  error.value = ''
  formRef.value?.validate(async (valid: boolean) => {
    if (!valid) return
    loading.value = true
    // 这里模拟请求
    setTimeout(() => {
      loading.value = false
      if (form.value.username === 'admin' && form.value.password === '123456') {
        store.login({ username: form.value.username, membership: 'Basic' })
        // 跳转见 Login.vue
      } else {
        error.value = 'Invalid username or password'
      }
    }, 1000)
  })
}
function handleForgot() {
  error.value = '请联系管理员重置密码'
}
</script>

<style scoped>
.login-form {
  width: 340px;
  margin: 0 auto;
  padding: 32px 24px 24px 24px;
  background: rgba(32, 23, 65, 0.7);
  border-radius: 14px;
  box-shadow: 0 4px 40px 0 rgba(64,48,160,0.15);
  backdrop-filter: blur(5px);
  animation: fadeIn 1s;
}
h2 {
  text-align: center;
  color: #fff;
  margin-bottom: 16px;
  font-weight: 600;
  letter-spacing: 1px;
}
.login-btn {
  width: 100%;
  box-shadow: 0 0 8px #ae8fff, 0 0 16px #7c3aed80;
  background: linear-gradient(90deg, #7b2ff2 0%, #f357a8 100%);
  color: #fff;
  border: none;
  transition: box-shadow 0.2s, transform 0.2s;
}
.login-btn:hover {
  box-shadow: 0 0 32px #ae8fff, 0 0 48px #7c3aed60;
  transform: translateY(-2px) scale(1.04);
  background: linear-gradient(90deg, #4a00e0 0%, #8e2de2 100%);
}
.options {
  display: flex;
  justify-content: space-between;
  margin-top: 12px;
}
.forgot, .register {
  color: #9ecfff;
  cursor: pointer;
  font-size: 13px;
  transition: color .2s;
}
.forgot:hover, .register:hover {
  color: #ffe29a;
  text-shadow: 0 0 8px #ae8fff90;
}
@keyframes fadeIn {
  0% { opacity: 0; transform: translateY(20px);}
  100% { opacity: 1; transform: none;}
}
</style>

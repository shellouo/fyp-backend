<template>
  <div class="register-form">
    <h2>Create Your Account</h2>
    <el-form :model="form" :rules="rules" ref="formRef" label-width="90px" class="animated-form">
      <el-form-item label="Username" prop="username">
        <el-input v-model="form.username" autocomplete="off" clearable />
      </el-form-item>
      <el-form-item label="Email" prop="email">
        <el-input v-model="form.email" autocomplete="off" clearable />
      </el-form-item>
      <el-form-item label="Password" prop="password">
        <el-input v-model="form.password" type="password" show-password autocomplete="off" clearable />
      </el-form-item>

      <el-form-item label="Membership" prop="membership">
        <el-radio-group v-model="form.membership">
          <el-radio label="basic">Basic - Free</el-radio>
          <el-radio label="premium">Premium - $9.99/month</el-radio>
          <el-radio label="business">Business - $29.99/month</el-radio>
        </el-radio-group>
      </el-form-item>

      <el-form-item>
        <el-button
            type="primary"
            class="glow-btn"
            :loading="loading"
            @click="onSubmit"
        >Register</el-button>
      </el-form-item>
    </el-form>
    <div class="login-link">
      Already have an account?
      <el-link @click="$emit('switchToLogin')" underline>Login here</el-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

// 表单数据
const form = ref({
  username: '',
  email: '',
  password: '',
  membership: 'basic'
})
const loading = ref(false)
const formRef = ref()
// 表单校验规则
const rules = {
  username: [
    { required: true, message: 'Username required', trigger: 'blur' },
    { min: 3, max: 16, message: '3-16 chars', trigger: 'blur' }
  ],
  email: [
    { required: true, message: 'Email required', trigger: 'blur' },
    { type: 'email', message: 'Invalid email', trigger: ['blur', 'change'] }
  ],
  password: [
    { required: true, message: 'Password required', trigger: 'blur' },
    { min: 6, max: 24, message: '6-24 chars', trigger: 'blur' }
  ],
  membership: [{ required: true, message: 'Select a plan', trigger: 'change' }]
}

// 提交注册表单
const onSubmit = () => {
  formRef.value?.validate((valid: boolean) => {
    if (!valid) return
    loading.value = true
    // 假装请求后端
    setTimeout(() => {
      loading.value = false
      ElMessage.success('Register Success! 🎉')
      // 通知父组件切换页面或自动跳转
      // 例如：emit('registerSuccess')
    }, 1200)
  })
}
</script>

<style scoped>
.register-form {
  background: rgba(40, 15, 70, 0.95);
  border-radius: 18px;
  padding: 36px 38px 20px 38px;
  box-shadow: 0 6px 36px #a98fff33;
  max-width: 440px;
  margin: 32px auto;
  animation: floatIn 0.8s cubic-bezier(.77,0,.18,1.04);
  position: relative;
}
.animated-form {
  margin-top: 22px;
}
h2 {
  font-weight: bold;
  color: #fff;
  letter-spacing: 1px;
  text-shadow: 0 2px 12px #7e54d3;
}
.login-link {
  margin-top: 18px;
  color: #b6b6f6;
  text-align: center;
}
.glow-btn {
  background: linear-gradient(90deg, #a084ff 40%, #6f4de7 100%);
  border: none;
  color: #fff;
  font-weight: bold;
  letter-spacing: 1px;
  box-shadow: 0 2px 16px #7e4dd380, 0 0 0 #fff;
  transition: box-shadow .22s, transform .17s;
}
.glow-btn:hover, .glow-btn:focus {
  box-shadow: 0 0 20px #a084ffcc, 0 0 80px #d9b3ff60;
  transform: scale(1.045) rotate(-0.5deg);
  background: linear-gradient(100deg, #8e7cfc 40%, #563bd7 100%);
}
.el-form-item__label {
  color: #dedbff;
}
.el-input__wrapper {
  background: #29205c80;
}
@keyframes floatIn {
  from { transform: translateY(40px) scale(0.95); opacity: 0; }
  to { transform: none; opacity: 1; }
}
</style>

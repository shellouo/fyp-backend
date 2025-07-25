<template>
  <div class="register-bg">
    <!-- 背景流动粒子特效层 -->
    <div class="register-particles"></div>
    <!-- 半透明毛玻璃卡片 -->
    <div class="register-glass">
      <div class="register-card animate__animated animate__fadeInDown">
        <!-- 顶部动态渐变光圈+LOGO -->
        <div class="register-logo">
          <svg width="60" height="60">
            <defs>
              <radialGradient id="shine" cx="50%" cy="50%" r="70%">
                <stop offset="0%" stop-color="#a5fffa" />
                <stop offset="60%" stop-color="#6236ff" />
                <stop offset="100%" stop-color="#1c0e32" />
              </radialGradient>
            </defs>
            <circle cx="30" cy="30" r="26" fill="url(#shine)">
              <animate attributeName="r" values="24;28;24" dur="3.2s" repeatCount="indefinite"/>
            </circle>
          </svg>
        </div>
        <h2 class="register-title">Create Your Account</h2>
        <el-form
            :model="form"
            :rules="rules"
            ref="formRef"
            label-width="98px"
            class="reg-form"
        >
          <el-form-item label="Username" prop="username">
            <el-input v-model="form.username" maxlength="18" show-word-limit placeholder="Enter your username" />
          </el-form-item>
          <el-form-item label="Email" prop="email">
            <el-input v-model="form.email" placeholder="Enter your email" />
          </el-form-item>
          <el-form-item label="Password" prop="password">
            <el-input v-model="form.password" type="password" show-password placeholder="Create a password (min 6 chars)" />
          </el-form-item>
          <el-form-item label="Membership">
            <el-radio-group v-model="form.membership">
              <el-radio label="basic">Basic (Free)</el-radio>
              <el-radio label="premium">Premium</el-radio>
              <el-radio label="business">Business</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item>
            <el-button
                type="primary"
                class="glow-btn-particles"
                :loading="loading"
                @click="onSubmit"
                @mousemove="btnParticles"
                ref="regBtn"
            >
              <span>Register</span>
              <span class="btn-particles" ref="particles"></span>
            </el-button>
          </el-form-item>
        </el-form>
        <div class="login-link">
          Already have an account?
          <el-link type="primary" @click="goLogin">Login here</el-link>
        </div>
        <!-- 卡片下方淡淡极光 -->
        <div class="neon-aurora"></div>
      </div>
    </div>
    <!-- 前景彩色粒子流（使用 CSS 动画模拟极光粒子） -->
    <div class="register-aurora-particles"></div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useUserStore } from '@/store/user'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()
const formRef = ref()
const regBtn = ref<HTMLElement>()
const particles = ref<HTMLElement>()
const loading = ref(false)

const form = ref({
  username: '',
  email: '',
  password: '',
  membership: 'basic',
})

const rules = {
  username: [
    { required: true, message: 'Username required', trigger: 'blur' },
    { min: 2, message: 'At least 2 characters', trigger: 'blur' }
  ],
  email: [
    { required: true, message: 'Email required', trigger: 'blur' },
    { type: 'email', message: 'Invalid email', trigger: ['blur', 'change'] }
  ],
  password: [
    { required: true, message: 'Password required', trigger: 'blur' },
    { min: 6, message: 'Min 6 chars', trigger: 'blur' }
  ]
}

const onSubmit = () => {
  formRef.value.validate((valid: boolean) => {
    if (valid) {
      loading.value = true
      setTimeout(() => {
        userStore.login({
          username: form.value.username,
          membership: form.value.membership as "basic" | "premium" | "business",
        })
        ElMessage.success('Registration successful!')
        loading.value = false
        router.push('/analysis-main')
      }, 1000)
    }
  })
}

function btnParticles(e: MouseEvent) {
  if (!particles.value) return
  const btn = regBtn.value!
  const rect = btn.getBoundingClientRect()
  const x = e.clientX - rect.left
  const y = e.clientY - rect.top
  particles.value.innerHTML = ''
  for (let i = 0; i < 14; i++) {
    const particle = document.createElement('span')
    particle.className = 'particle'
    particle.style.left = `${x + Math.random() * 48 - 24}px`
    particle.style.top = `${y + Math.random() * 22 - 11}px`
    particle.style.background = `radial-gradient(circle at 50% 50%, #a9faff 50%, #6541fa 100%, #fff0)`
    particle.style.opacity = Math.random() * 0.7 + 0.3
    particles.value.appendChild(particle)
    setTimeout(() => particle.remove(), 760)
  }
}

function goLogin() {
  router.push('/login')
}
</script>

<style scoped>
@import 'animate.css';

/* 深邃AI科技极光渐变背景 + 粒子特效 */
.register-bg {
  min-height: 100vh;
  width: 100vw;
  position: fixed;
  top: 0; left: 0;
  z-index: 0;
  overflow: auto;
  background: radial-gradient(ellipse 100% 80% at 60% 15%, #25194d 0%, #221943 55%, #130b27 100%),
  linear-gradient(100deg, #4531c2 0%, #292348 52%, #130b27 100%);
}

/* 1. 背景流动星星特效 */
.register-particles {
  pointer-events: none;
  position: fixed;
  top: 0; left: 0;
  width: 100vw; height: 100vh;
  z-index: 0;
  background-image:
      repeating-radial-gradient(circle at 10% 20%, #9dd1ff88 0px, #9dd1ff88 1px, transparent 2px, transparent 100px),
      repeating-radial-gradient(circle at 60% 80%, #86caff99 0px, #86caff99 1px, transparent 2px, transparent 130px),
      repeating-radial-gradient(circle at 90% 10%, #fff1fa44 0px, #fff1fa44 1.4px, transparent 3px, transparent 110px),
      repeating-radial-gradient(circle at 80% 55%, #a7e7d977 0px, #a7e7d977 1.2px, transparent 3px, transparent 140px);
  opacity: .23;
  animation: bgmove 18s linear infinite alternate;
}
@keyframes bgmove {
  0% { background-position: 0 0, 0 0, 0 0, 0 0;}
  100% { background-position: 100px 80px, 150px 210px, 70px 60px, 230px 70px;}
}

/* 2. 前景彩色流动粒子特效 (极光感) */
.register-aurora-particles {
  pointer-events: none;
  position: fixed;
  width: 100vw; height: 100vh;
  left: 0; top: 0;
  z-index: 3;
}
.register-aurora-particles::before,
.register-aurora-particles::after {
  content: '';
  position: absolute;
  border-radius: 50%;
  filter: blur(68px);
  opacity: 0.23;
  pointer-events: none;
  animation: auroraMove 12s linear infinite alternate;
}
.register-aurora-particles::before {
  width: 340px; height: 340px;
  left: 18vw; top: 38vh;
  background: radial-gradient(circle at 65% 45%, #44fff6 0, #6731d7 60%, #fff0 100%);
  animation-delay: 0s;
}
.register-aurora-particles::after {
  width: 400px; height: 350px;
  left: 62vw; top: 10vh;
  background: radial-gradient(circle at 50% 50%, #ff8be9 0, #2b66d3 60%, #fff0 100%);
  animation-delay: 4s;
}
@keyframes auroraMove {
  0% { transform: scale(1) translateY(0); opacity: 0.21;}
  80% { opacity: 0.38;}
  100% { transform: scale(1.18) translateY(28px); opacity: 0.25;}
}

/* 3. 毛玻璃特效容器 */
.register-glass {
  width: 100vw;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(22, 14, 36, 0.08);
  backdrop-filter: blur(18px) brightness(1.08);
}

/* 4. 卡片-超级霓虹边框+内光 */
.register-card {
  position: relative;
  background: rgba(24, 22, 38, 0.98);
  border-radius: 26px;
  box-shadow: 0 10px 60px 0 #3e24ff2a, 0 3px 22px 0 #00e2ff2c, 0 2px 36px #1f005510;
  padding: 52px 44px 32px 44px;
  min-width: 420px;
  max-width: 450px;
  border: 2.4px solid transparent;
  /* 霓虹光圈动画边框 */
  border-image: linear-gradient(120deg, #44e2ff 10%, #9e31ff 45%, #ff90e9 75%, #1cfbff 100%) 1;
  box-shadow: 0 2px 28px 0 #44e2ff2c, 0 1px 8px #c1a2ff44, 0 0 0 6px #4621ff14;
  transition: box-shadow .38s, border .28s;
  z-index: 9;
}
.register-card:hover {
  box-shadow: 0 8px 44px 0 #34c1ff45, 0 2px 32px #ed6cff44, 0 0 0 8px #1cfbff18;
  border-color: #8fe3ff #c2a2ff #ffafea #8efeff;
}

/* 5. 顶部动态logo光圈 */
.register-logo {
  display: flex;
  justify-content: center;
  margin-bottom: -6px;
  margin-top: -18px;
}
.register-title {
  font-family: 'Inter', 'Montserrat', 'Segoe UI', 'Arial', sans-serif;
  font-size: 2.1rem;
  font-weight: 800;
  letter-spacing: 1.1px;
  background: linear-gradient(95deg, #d5f7ff 10%, #8e97ff 45%, #ff8be9 70%, #7f54ff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 28px;
  text-align: center;
}

/* 表单美化 */
.el-form-item__label {
  color: #e6d7ff !important;
  font-size: 1.03rem;
  font-weight: 600;
  letter-spacing: .01em;
  text-shadow: 0 2px 12px #4621ff34;
}
.el-input__inner, .el-input input {
  background: rgba(44,56,98,0.27);
  border: 1.5px solid #44e2ff80;
  border-radius: 9px;
  color: #dbfaff;
  font-size: 1.08rem;
  padding: 10px 16px;
  box-shadow: 0 1.5px 8px #31f3ff18 inset;
  transition: border-color .2s;
}
.el-input__inner:focus, .el-input input:focus {
  border-color: #e298ff;
  box-shadow: 0 0 0 3px #bd64ff45;
  background: rgba(255,252,255,0.19);
}
.el-radio__label {
  color: #a8e7ff !important;
  font-size: 1rem;
  font-weight: 500;
  letter-spacing: .01em;
}
.el-radio.is-checked .el-radio__inner {
  border-color: #6e24ff;
  background: linear-gradient(135deg, #74f6e5 0%, #ffb8fb 100%);
  box-shadow: 0 2px 8px #ff92f540;
}
.el-radio__inner {
  background: rgba(28,27,40,0.17);
  border-radius: 7px;
  border-width: 2px;
  box-shadow: 0 2px 12px #a7fffa20;
}

/* 6. 注册按钮升级霓虹&动态粒子 */
.glow-btn-particles {
  position: relative;
  overflow: visible !important;
  background: linear-gradient(92deg, #4f6fff 10%, #2af9ff 60%, #ea8fff 100%);
  border: none;
  color: #fff;
  font-weight: 700;
  font-size: 1.14rem;
  border-radius: 13px;
  box-shadow: 0 2px 18px 2px #2af9ff60, 0 1px 8px #6e24ff26;
  padding: 12px 36px;
  cursor: pointer;
  letter-spacing: 0.08em;
  transition: box-shadow .2s, background .23s;
  z-index: 2;
}
.glow-btn-particles:hover {
  background: linear-gradient(90deg, #31f3ff 8%, #e98fff 88%);
  box-shadow: 0 6px 30px 0 #c0faff9c, 0 1px 24px #e98fff60;
}
.btn-particles {
  pointer-events: none;
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  border-radius: 12px;
}
.particle {
  position: absolute;
  width: 12px;
  height: 12px;
  border-radius: 50%;
  opacity: .5;
  pointer-events: none;
  animation: particle-fade .88s cubic-bezier(.61,-0.26,.7,1.43);
  filter: blur(1.2px);
}
@keyframes particle-fade {
  0% { opacity: 1; transform: scale(.7);}
  100% { opacity: 0; transform: scale(1.3);}
}

/* 卡片底部淡极光 */
.neon-aurora {
  position: absolute;
  left: 15%; right: 15%;
  bottom: -28px;
  height: 44px;
  z-index: 1;
  border-radius: 38px;
  background: radial-gradient(circle at 60% 30%, #38faff40 0, #cf78ff22 70%, #fff0 100%);
  filter: blur(12px);
  pointer-events: none;
}

/* 登录链接 */
.login-link {
  margin-top: 28px;
  text-align: center;
  color: #b3beff;
  font-size: 1.04rem;
}
.login-link .el-link {
  color: #7ceaff;
  font-weight: 700;
  margin-left: 7px;
  text-shadow: 0 1px 18px #97ffe740;
}

@media (max-width: 640px) {
  .register-card {
    min-width: 95vw;
    max-width: 99vw;
    padding: 22px 2vw 16px 2vw;
  }
  .register-title { font-size: 1.13rem;}
}

</style>


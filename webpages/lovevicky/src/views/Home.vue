



<template>
  <!-- 背景极光和星空动画 -->
  <div class="aurora-bg"></div>
  <div class="stars-bg">
    <canvas ref="canvasRef" class="stars-canvas"></canvas>
  </div>

  <!-- 顶部导航栏（商业感） -->
  <header class="top-nav">
    <div class="nav-logo">
      <img src="@/assets/ai-face-demo.png" alt="LOGO" height="32" />
      <span>FaceAgePro</span>
    </div>
    <nav>
      <a @click.prevent="go('/')" :class="{active: $route.path==='/' }">Home</a>
      <a @click.prevent="go('/analysis-main')">Analysis</a>
      <a @click.prevent="go('/docs')">Docs</a>
      <a @click.prevent="go('/pricing')">Pricing</a>
      <a @click.prevent="go('/contact')">Contact</a>
    </nav>
  </header>

  <div class="home-card">
    <div class="hero-row">
      <div class="hero-text">
        <h1>
          Advanced Face Age Recognition
        </h1>
        <p class="hero-desc">
          Accurately determine age from facial features using our AI-powered technology.<br>
          <span class="highlight">Perfect for age verification, KYC, demographic analysis and more.</span>
        </p>
        <div class="btn-group">
          <el-button class="fancy-btn" type="primary" @click="go('/analysis-main')" @mousedown="showParticles">
            <i class="el-icon-search" /> Analysis System
          </el-button>
          <el-button class="fancy-btn" @click="go('/register')" @mousedown="showParticles">
            Register
          </el-button>
          <el-button class="fancy-btn" @click="go('/login')" @mousedown="showParticles">
            Login
          </el-button>
          <el-button class="fancy-btn admin" type="info" @click="go('/admin')" @mousedown="showParticles">
            Admin System
          </el-button>
          <!-- 新增快速体验 -->
          <el-button class="fancy-btn demo" type="success" @click="tryDemo" @mousedown="showParticles">
            <i class="el-icon-magic-stick" /> Try Demo
          </el-button>
        </div>
        <!-- 新增动态商业数据 -->
        <div class="stats-row">
          <div class="stat-block">
            <span class="stat-num">{{ userCount }}</span>
            <span class="stat-label">Analyzed Faces</span>
          </div>
          <div class="stat-block">
            <span class="stat-num">{{ clientCount }}</span>
            <span class="stat-label">Business Clients</span>
          </div>
          <div class="stat-block">
            <span class="stat-num">97.3%</span>
            <span class="stat-label">Accuracy Rate</span>
          </div>
        </div>
      </div>
      <div class="hero-img">

        <CosmicPortal
            style="
      position: absolute;
      left: 50%; top: 50%; transform: translate(-50%,-50%);
      width: 350px; height: 350px;
      pointer-events: none; z-index: 1;
      border-radius: 40px;
      overflow: hidden;
      box-shadow: 0 0 60px 0 #8de4ff40, 0 0 24px 2px #6f5cff90, 0 0 0 10px #ffffff11 inset;
      background: radial-gradient(circle at 60% 30%, #5841b0 80%, #000a 100%);
      backdrop-filter: blur(6px) brightness(1.1);
      border: 2px solid #a5b8fc60;
    "
            :primary-color="'#A26AFF'"
            :secondary-color="'#23C4F8'"
            :accent-color="'#FE7EAF'"
            :vortex-color="'#ACB6FF'"
            :portal-complexity="5"
            :crystal-count="13"
        />
        <!-- 新增呼吸光圈动画 -->
        <div class="face-glow"></div>
      </div>
    </div>

    <section class="main-section">
      <h2>Introduction</h2>
      <p>
        This system uses advanced AI to estimate age from face images, for age verification, statistics, and more. <br>
        Easy integration, privacy protection, accurate & efficient!
      </p>

      <h2>Information</h2>
      <div class="info-row">
        <el-card class="info-card">
          <span class="icon"><svg viewBox="0 0 24 24" width="24" fill="none"><defs><linearGradient id="g1" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#FFD600"/><stop offset="1" stop-color="#FF5F6D"/></linearGradient></defs><path fill="url(#g1)" d="M12 2l1.4 5.32h5.6L14 11.36l1.4 5.32L12 15.68 8.6 16.68 10 11.36 5 7.32h5.6z"/></svg></span>
          <div>
            <strong>Fast Processing</strong><br>
            Speed and efficiency in age analysis.
          </div>
        </el-card>
        <el-card class="info-card">
          <span class="icon"><svg viewBox="0 0 24 24" width="24" fill="none"><defs><linearGradient id="g2" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#70e1f5"/><stop offset="1" stop-color="#ffd194"/></linearGradient></defs><path fill="url(#g2)" d="M12 2a6 6 0 016 6v1h1a1 1 0 011 1v10a2 2 0 01-2 2H6a2 2 0 01-2-2V10a1 1 0 011-1h1V8a6 6 0 016-6zm0 2a4 4 0 00-4 4v1h8V8a4 4 0 00-4-4z"/></svg></span>
          <div>
            <strong>Privacy Protection</strong><br>
            Data security and privacy ensured.
          </div>
        </el-card>
        <el-card class="info-card">
          <span class="icon"><svg viewBox="0 0 24 24" width="24" fill="none"><defs><linearGradient id="g3" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#43e97b"/><stop offset="1" stop-color="#38f9d7"/></linearGradient></defs><circle fill="url(#g3)" cx="12" cy="12" r="10"/><path d="M8 12l3 3 5-5" stroke="#fff" stroke-width="2" fill="none"/></svg></span>
          <div>
            <strong>Accuracy Rate</strong><br>
            Accurate age predictions based on facial analysis.
          </div>
        </el-card>
      </div>

      <!-- 新增 合作伙伴/logo墙 -->
      <h2>Trusted By</h2>
      <div class="logo-wall">
        <img src="https://static-1305146246.cos.ap-shanghai.myqcloud.com/logo/tencent.png" alt="Tencent" />
        <img src="https://static-1305146246.cos.ap-shanghai.myqcloud.com/logo/huawei.png" alt="Huawei" />
        <img src="https://static-1305146246.cos.ap-shanghai.myqcloud.com/logo/baidu.png" alt="Baidu" />
        <img src="https://static-1305146246.cos.ap-shanghai.myqcloud.com/logo/alibaba.png" alt="Alibaba" />
        <img src="https://static-1305146246.cos.ap-shanghai.myqcloud.com/logo/bytedance.png" alt="Bytedance" />
      </div>

      <!-- 新增用户评价 -->
      <h2>User Testimonials</h2>
      <div class="testimonials">
        <div class="testimonial-card">
          <div class="t-user">Zhang Wei, Security Manager</div>
          <div class="t-text">“FaceAgePro helped us automate age verification, and our user onboarding rate increased by 34%.”</div>
        </div>
        <div class="testimonial-card">
          <div class="t-user">Anna Lee, Product Lead</div>
          <div class="t-text">“Super accurate and easy to integrate API. Our privacy concerns都被解决了。”</div>
        </div>
      </div>

      <h2>Consulting</h2>
      <div class="consult-row">
        <span>Need custom solutions? Our team provides consulting services for implementing face age recognition in your business.</span>
        <el-button type="primary" class="fancy-btn" @click="goContact" @mousedown="showParticles">Contact Us</el-button>
      </div>
    </section>
  </div>

  <!-- 新增底部信息 -->
  <footer class="page-footer">
    <div>© 2024 FaceAgePro Inc. | All Rights Reserved.</div>
    <div class="footer-links">
      <a @click.prevent="go('/privacy')">Privacy Policy</a>
      <a @click.prevent="go('/terms')">Terms</a>
    </div>
  </footer>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import CosmicPortal from '@/components/CosmicPortal.vue'


const router = useRouter()
const $route = useRoute()

function go(path: string) {
  router.push(path)
}
function goContact() {
  window.open('mailto:business@faceagepro.com')
}
function tryDemo() {
  router.push('/analysis-main?demo=1')
}

// 动态数字动画
const userCount = ref(0)
const clientCount = ref(0)
onMounted(() => {
  let uc = 0, cc = 0
  const t1 = setInterval(() => {
    if (uc < 18012) { uc += 97; userCount.value = uc }
    else { userCount.value = 18012; clearInterval(t1) }
  }, 18)
  const t2 = setInterval(() => {
    if (cc < 102) { cc += 3; clientCount.value = cc }
    else { clientCount.value = 102; clearInterval(t2) }
  }, 25)
})

// 星空动画
const canvasRef = ref<HTMLCanvasElement | null>(null)
onMounted(() => {
  const canvas = canvasRef.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')!
  let w = window.innerWidth, h = window.innerHeight
  canvas.width = w
  canvas.height = h

  // 星星数组
  const stars: {x: number; y: number; r: number; o: number}[] = []
  function genStars() {
    stars.length = 0
    for (let i = 0; i < 160; i++) {
      stars.push({
        x: Math.random() * w,
        y: Math.random() * h,
        r: Math.random() * 1.2 + 0.3,
        o: Math.random() * 0.5 + 0.25
      })
    }
  }
  genStars()

  function auroraGradient() {
    const grd = ctx.createLinearGradient(0, 0, w, h)
    grd.addColorStop(0, '#7F4EEA')
    grd.addColorStop(0.5, '#A6C8FF')
    grd.addColorStop(1, '#5D3FD3')
    return grd
  }

  function draw() {
    ctx.clearRect(0, 0, w, h)
    // Aurora
    ctx.save()
    ctx.globalAlpha = 0.4
    ctx.fillStyle = auroraGradient()
    ctx.beginPath()
    ctx.ellipse(w/2, h*0.28, w*0.38, h*0.21, Math.PI/7, 0, Math.PI*2)
    ctx.fill()
    ctx.restore()
    // stars
    stars.forEach(star => {
      ctx.save()
      ctx.beginPath()
      ctx.globalAlpha = star.o
      ctx.arc(star.x, star.y, star.r, 0, Math.PI*2)
      ctx.fillStyle = "#fff"
      ctx.shadowColor = "#C2A8FA"
      ctx.shadowBlur = 6
      ctx.fill()
      ctx.restore()
    })
    requestAnimationFrame(draw)
  }
  draw()
  window.addEventListener('resize', () => {
    w = window.innerWidth
    h = window.innerHeight
    canvas.width = w
    canvas.height = h
    genStars()
  })
})

// 按钮粒子/光晕动画
function showParticles(e: MouseEvent) {
  const btn = e.currentTarget as HTMLElement
  if (!btn) return
  const part = document.createElement('span')
  part.className = 'btn-particle'
  part.style.left = `${e.offsetX}px`
  part.style.top = `${e.offsetY}px`
  btn.appendChild(part)
  setTimeout(() => btn.removeChild(part), 700)
}
</script>

<style scoped>
/* Aurora、星空背景，与之前类似 */
.aurora-bg {
  position: fixed; z-index: 0; width: 100vw; height: 100vh; top: 0; left: 0; pointer-events: none; overflow: hidden;
}
.aurora-bg::after {
  content: '';
  position: absolute;
  inset: 0;
  background-image: repeating-linear-gradient(100deg,#3b82f6 10%,#a5b4fc 15%,#93c5fd 20%,#ddd6fe 25%,#60a5fa 30%),
  repeating-linear-gradient(100deg,#fff 0%,#fff 7%,transparent 10%,transparent 12%,#fff 16%);
  background-size: 300%, 200%;
  background-position: 50% 50%, 50% 50%;
  opacity: 0.5;
  filter: blur(12px);
  animation: aurora 60s linear infinite;
  z-index: 0;
}
@keyframes aurora { from {background-position: 50% 50%, 50% 50%;} to {background-position: 350% 50%, 350% 50%;}}
.stars-bg {
  position: fixed; z-index: 1; width: 100vw; height: 100vh; top: 0; left: 0; overflow: hidden; pointer-events: none;
}
.stars-canvas { width: 100vw; height: 100vh; display: block; }

/* 顶部导航栏 */
.top-nav {
  z-index: 20; position: relative;
  display: flex; align-items: center; justify-content: space-between;
  max-width: 1180px; margin: 0 auto; padding: 24px 20px 6px 20px;
}
.nav-logo { display: flex; align-items: center; font-size: 1.28rem; font-weight: 700; color: #a394ff;}
.nav-logo img { margin-right: 9px; }
.top-nav nav { display: flex; gap: 24px;}
.top-nav nav a {
  color: #e2e7ffb2; font-weight: 500; text-decoration: none; font-size: 1rem; padding: 3px 11px; border-radius: 8px;
  transition: color 0.2s, background 0.2s;
}
.top-nav nav a.active,
.top-nav nav a:hover { color: #fff; background: #6d6dfd36; }

/* 主体卡片区 */
.home-card {
  position: relative; z-index: 2; max-width: 1100px; margin: 36px auto 0;
  background: rgba(28,19,48,0.81);
  border-radius: 26px; box-shadow: 0 12px 32px 0 #5b36a160;
  padding: 36px 44px 38px 44px; color: #fff;
  backdrop-filter: blur(4px); border: 1px solid #7861ff30;
}
.hero-row {
  display: flex; align-items: center; justify-content: space-between; margin-bottom: 40px; flex-wrap: wrap;
}
.hero-text { flex: 1.22; min-width: 310px;}
.hero-text .hero-desc {font-size: 1.17rem; margin-bottom: 14px;}
.hero-text .highlight { color: #a8e1fd; font-weight: 600;}
.hero-img { flex: 1; display: flex; align-items: center; justify-content: flex-end; position: relative;}
.hero-img img { max-width: 330px; min-width: 150px; border-radius: 20px; filter: drop-shadow(0 8px 40px #826cff45);}
.face-glow {
  position: absolute; left: 50%; top: 50%; transform: translate(-50%,-50%);
  width: 350px; height: 350px; border-radius: 50%;
  pointer-events: none;
  background: radial-gradient(circle, #837fff88 10%, #ed8ff680 60%, transparent 100%);
  opacity: 0.65; z-index: 0;
  animation: faceGlowPulse 3.7s ease-in-out infinite;
}
@keyframes faceGlowPulse {
  0%,100% { opacity: 0.5; transform: translate(-50%,-50%) scale(1);}
  50% { opacity: 0.85; transform: translate(-50%,-50%) scale(1.07);}
}
.btn-group { margin: 36px 0 0 0; display: flex; flex-wrap: wrap; gap: 16px;}
.fancy-btn {
  font-weight: 600; letter-spacing: 0.1em; border-radius: 18px !important;
  font-size: 1.04rem; padding: 0.7em 2.3em; position: relative; overflow: hidden;
  background: linear-gradient(90deg, #7c5fff 35%, #ca6de1 100%);
  border: none; color: #fff;
  box-shadow: 0 4px 18px #8e44ff37, 0 0 0 transparent;
  transition: background 0.3s, box-shadow 0.25s, transform 0.13s;
}
.fancy-btn.demo { background: linear-gradient(90deg,#45ffc2 10%,#51c9ff 100%);}
.fancy-btn.admin { background: linear-gradient(90deg, #c794fa 20%, #7367f0 85%);}
.fancy-btn .el-icon-search, .fancy-btn .el-icon-magic-stick { margin-right: 6px; }
.fancy-btn:before {
  content: ""; position: absolute; top: 50%; left: 50%;
  width: 160%; height: 400%; background: radial-gradient(circle, #fff2 10%, transparent 70%);
  opacity: 0; transform: translate(-50%,-50%) scale(0.6);
  transition: opacity .5s, transform .4s; z-index: 0;
}
.fancy-btn:hover, .fancy-btn:focus {
  background: linear-gradient(90deg, #b77fff 5%, #6a49f5 100%);
  box-shadow: 0 2px 32px #a988ff60; transform: translateY(-3px) scale(1.045);
}
.fancy-btn.demo:hover { background: linear-gradient(90deg,#32fcc6 10%,#38bcfc 100%);}
.fancy-btn:active { transform: scale(0.97);}
.fancy-btn:hover:before, .fancy-btn:focus:before { opacity: 1; transform: translate(-50%,-50%) scale(1.03);}
.btn-particle {
  position: absolute; pointer-events: none; width: 38px; height: 38px;
  margin-left: -19px; margin-top: -19px; border-radius: 50%;
  background: radial-gradient(circle, #cfc3f9 10%, #f3e7ff80 80%, transparent 100%);
  animation: btn-burst .7s cubic-bezier(0.1,0.6,0.8,1);
  opacity: 0.76; z-index: 3;
}
@keyframes btn-burst { 0% { opacity: 0.7; transform: scale(0.2);} 85%{ opacity: 0.42;} 100%{ opacity: 0; transform: scale(2);} }

.stats-row {
  margin-top: 32px; display: flex; gap: 36px;
}
.stat-block {
  background: rgba(65,53,110,0.25); border-radius: 13px; padding: 18px 24px 11px 24px;
  display: flex; flex-direction: column; align-items: center; min-width: 120px; box-shadow: 0 4px 18px #7769ff1a;
}
.stat-num { font-size: 1.45em; font-weight: 700; color: #8ad8fe;}
.stat-label { font-size: 1em; color: #e1deffb2;}

.main-section { margin-top: 40px; }
.info-row { display: flex; gap: 24px; margin: 22px 0 34px 0; flex-wrap: wrap;}
.info-card {
  background: rgba(80,60,145,0.22) !important; border: 1px solid #7264d9 !important;
  border-radius: 18px !important; color: #e0dcff; font-size: 1.09rem; min-width: 230px; flex: 1;
  box-shadow: 0 4px 18px #7e61ff20; display: flex; align-items: center; gap: 16px; padding: 18px 18px 14px 18px;
}
.info-card .icon { font-size: 1.8em; margin-right: 4px; display: flex; align-items: center;}
.logo-wall {
  display: flex; align-items: center; gap: 26px; margin: 20px 0 28px 0;
}
.logo-wall img { height: 36px; filter: grayscale(0.5) brightness(1.12) drop-shadow(0 2px 12px #23234323);}
.logo-wall img:hover { filter: grayscale(0) brightness(1.32);}
.testimonials {
  display: flex; gap: 22px; margin-bottom: 14px; flex-wrap: wrap;
}
.testimonial-card {
  background: rgba(61,41,117,0.20); border-radius: 16px; box-shadow: 0 2px 8px #9485ef18;
  padding: 18px 22px; min-width: 210px; flex: 1 1 210px;
}
.testimonial-card .t-user { color: #97bfff; font-weight: 600; margin-bottom: 5px;}
.testimonial-card .t-text { color: #e9e6ff;}
.consult-row { display: flex; align-items: center; gap: 22px; margin-top: 16px;}
@media (max-width: 950px) {
  .hero-row {flex-direction: column;}
  .hero-img {justify-content: center; margin: 22px 0;}
  .stats-row { flex-direction: column; gap: 12px;}
}
@media (max-width: 700px) {
  .home-card { padding: 19px 4vw 28px 4vw;}
  .main-section { font-size: 1rem;}
  .btn-group { gap: 8px;}
  .logo-wall { gap: 10px;}
}

.page-footer {
  text-align: center; margin-top: 34px; color: #cdc6f8b6; font-size: 1.02em;
  padding: 14px 0 32px 0; background: none;
  display: flex; flex-direction: column; gap: 7px; align-items: center;
}
.footer-links { display: flex; gap: 18px; margin-top: 2px;}
.footer-links a { color: #97a7e8d0; text-decoration: underline; cursor: pointer;}
.footer-links a:hover { color: #fff;}
</style>

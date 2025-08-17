<template>
  <div class="notfound-bg">
    <canvas ref="auroraCanvas" class="aurora-canvas"></canvas>
    <div class="notfound-content">
      <h1>404</h1>
      <p>Oops! The page you visited does not exist.</p>
      <el-button type="primary" @click="goHome" size="large">Return to Home</el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { ref, onMounted, nextTick } from 'vue'

const router = useRouter()
function goHome() {
  router.replace('/')
}

// 极光/粒子背景，可复用前面代码
const auroraCanvas = ref<HTMLCanvasElement|null>(null)
onMounted(() => {
  nextTick(() => {
    const canvas = auroraCanvas.value
    if (!canvas) return
    const ctx = canvas.getContext('2d')!
    let w = window.innerWidth, h = window.innerHeight
    canvas.width = w; canvas.height = h
    const stars = Array.from({ length: 70 }, () => ({
      x: Math.random() * w,
      y: Math.random() * h,
      r: Math.random() * 1.5 + 0.7,
      o: Math.random() * 0.7 + 0.2,
      vx: (Math.random() - 0.5) * 0.02,
      vy: (Math.random() - 0.5) * 0.03,
      color: `hsl(${200 + Math.random() * 60},80%,90%)`
    }))
    function drawAurora() {
      ctx.clearRect(0, 0, w, h)
      // Aurora bands
      for (let band = 0; band < 2; band++) {
        const grad = ctx.createLinearGradient(0, h*0.2, w, h*0.49)
        grad.addColorStop(0, `rgba(${180+band*20},${150+band*50},255,${0.16-band*0.03})`)
        grad.addColorStop(1, 'rgba(140,180,255,0)')
        ctx.globalAlpha = 0.5 - band*0.13
        ctx.fillStyle = grad
        ctx.beginPath()
        ctx.ellipse(w/2, h*0.36+band*20, w*0.8, h*0.14+band*10, 0.09*band, 0, 2*Math.PI)
        ctx.fill()
      }
      ctx.globalAlpha = 1
      for (let s of stars) {
        ctx.beginPath()
        ctx.arc(s.x, s.y, s.r, 0, Math.PI*2)
        ctx.fillStyle = s.color
        ctx.globalAlpha = s.o
        ctx.shadowBlur = 8
        ctx.shadowColor = "#e3e8ff"
        ctx.fill()
        ctx.globalAlpha = 1
        ctx.shadowBlur = 0
        s.x += s.vx; s.y += s.vy
        if (s.x < 0 || s.x > w) s.vx *= -1
        if (s.y < 0 || s.y > h) s.vy *= -1
      }
      requestAnimationFrame(drawAurora)
    }
    drawAurora()
    window.addEventListener('resize', () => {
      w = window.innerWidth
      h = window.innerHeight
      canvas.width = w; canvas.height = h
    })
  })
})
</script>

<style scoped>
.notfound-bg {
  position: fixed;
  inset: 0;
  width: 100vw; height: 100vh;
  background: linear-gradient(120deg,#eeebff 0%,#bcd3fa 100%);
  z-index: 0;
}
.aurora-canvas {
  width: 100vw; height: 100vh;
  position: absolute; left: 0; top: 0; z-index: 1; pointer-events: none;
}
.notfound-content {
  position: absolute;
  left: 50%; top: 40%;
  transform: translate(-50%, -50%);
  z-index: 2;
  text-align: center;
  background: rgba(255,255,255,0.92);
  border-radius: 16px;
  box-shadow: 0 4px 36px #a6a2fa18;
  padding: 44px 50px 36px 50px;
}
.notfound-content h1 {
  font-size: 68px;
  font-weight: bold;
  color: #9067fa;
  margin-bottom: 15px;
  letter-spacing: 5px;
  text-shadow: 0 6px 24px #e6ddff60;
}
.notfound-content p {
  color: #6e7299;
  font-size: 20px;
  margin-bottom: 32px;
}
</style>

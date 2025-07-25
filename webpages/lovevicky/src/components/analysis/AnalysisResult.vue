<template>
  <div class="result-container">
    <!-- 圆环进度+爆点 -->
    <canvas ref="resultCanvas" class="result-canvas"></canvas>
    <div class="result-content">
      <div class="ai-glow">AI Result</div>
      <div class="value-row">
        <span class="label">Age:</span>
        <span class="ai-number">{{ shownAge.toFixed(1) }}</span>
        <span class="unit">years</span>
      </div>
      <div class="value-row">
        <span class="label">Gender:</span>
        <span class="ai-gender">{{ shownGender }}</span>
      </div>
      <div class="value-row">
        <span class="label">Confidence:</span>
        <span class="ai-conf">{{ (shownConf*100).toFixed(1) }}%</span>
      </div>
      <el-button type="primary" @click="$emit('back')">Analyze Another</el-button>
      <el-button type="info" @click="$emit('saveHistory',result)">Save Result</el-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, nextTick } from 'vue'
const props = defineProps<{
  result: { age: number, gender: string, confidence: number }
}>()
const emits = defineEmits(['back','saveHistory'])

const shownAge = ref(0)
const shownConf = ref(0)
const shownGender = ref('...')
const resultCanvas = ref<HTMLCanvasElement|null>(null)

watch(() => props.result, (r) => {
  animateValue(shownAge, r.age)
  animateValue(shownConf, r.confidence)
  shownGender.value = ''
  setTimeout(() => { shownGender.value = r.gender }, 650)
  playCircle(r.confidence)
})

function animateValue(targetRef, end) {
  let start = 0
  const step = () => {
    if (start < end) {
      start += (end - start) * 0.18 + 0.02
      if (start > end) start = end
      targetRef.value = start
      requestAnimationFrame(step)
    } else {
      targetRef.value = end
    }
  }
  step()
}

// 动画圆环进度
function playCircle(percent: number) {
  nextTick(() => {
    const canvas = resultCanvas.value
    if (!canvas) return
    const ctx = canvas.getContext('2d')!
    const w = 140, h = 140
    canvas.width = w; canvas.height = h
    let p = 0
    // 粒子爆点参数
    let particles = Array.from({length: 24}, (_,i)=>({
      angle: i*Math.PI*2/24, r:56, show: false, speed:0.6+Math.random()*0.6
    }))
    let frame = 0
    function draw() {
      ctx.clearRect(0,0,w,h)
      // 背景流光
      const grad = ctx.createLinearGradient(0,0,w,h)
      grad.addColorStop(0,'#aab2ff'); grad.addColorStop(1,'#debfff')
      ctx.beginPath(); ctx.arc(w/2,h/2,62,0,Math.PI*2)
      ctx.strokeStyle = grad; ctx.lineWidth = 6
      ctx.globalAlpha = 0.26
      ctx.stroke(); ctx.globalAlpha=1

      // AI主圆环进度
      ctx.save()
      ctx.beginPath()
      ctx.arc(w/2,h/2,52,-Math.PI/2,-Math.PI/2 + Math.PI*2*p)
      ctx.strokeStyle = `rgba(134,80,255,0.92)`
      ctx.lineWidth = 7
      ctx.shadowBlur = 20; ctx.shadowColor = '#ffe0ff'
      ctx.stroke()
      ctx.restore()

      // 粒子爆点
      if (p > percent - 0.06 && frame < 35) {
        particles.forEach(pt=>{
          pt.show = true
          pt.r += pt.speed
        })
      }
      particles.forEach(pt=>{
        if (pt.show) {
          ctx.save()
          ctx.beginPath()
          ctx.arc(w/2 + Math.cos(pt.angle)*pt.r, h/2 + Math.sin(pt.angle)*pt.r, 3+Math.random()*2, 0, Math.PI*2)
          ctx.globalAlpha = 0.5
          ctx.fillStyle = '#ffe0e9'
          ctx.shadowBlur = 20
          ctx.shadowColor = "#fff"
          ctx.fill()
          ctx.restore()
        }
      })

      // AI中心点
      ctx.beginPath()
      ctx.arc(w/2, h/2, 12, 0, Math.PI*2)
      ctx.fillStyle = '#f4eaff'
      ctx.shadowBlur = 8; ctx.shadowColor="#a96dff"
      ctx.fill()
      ctx.shadowBlur=0
      ctx.globalAlpha=1
      frame++
      if (p < percent) {
        p += (percent-p)*0.11+0.009
        requestAnimationFrame(draw)
      }
    }
    draw()
  })
}
</script>

<style scoped>
.result-container {
  display: flex; align-items: center; justify-content: center;
  min-height: 320px;
}
.result-canvas {
  width: 140px; height: 140px; margin-right: 36px;
  filter: drop-shadow(0 2px 38px #b9a0ff99);
}
.result-content {
  min-width: 260px; padding: 18px 8px;
  background: rgba(250,246,255,0.92);
  border-radius: 16px;
  box-shadow: 0 2px 20px #c1b0ff27;
  display: flex; flex-direction: column; align-items: start;
}
.ai-glow {
  color: #7a52fa; font-size: 1.1em;
  font-weight: 700; letter-spacing: 2px;
  text-shadow: 0 0 12px #cebaff, 0 0 3px #fff;
  margin-bottom: 20px;
}
.value-row {
  font-size: 1.13em;
  margin-bottom: 12px;
}
.label {
  font-weight: bold; color: #b38dff;
  margin-right: 8px;
}
.ai-number { font-size: 1.5em; color: #7a52fa; font-weight: 900; letter-spacing: 1.2px;}
.unit { margin-left:6px; color: #9476ec; }
.ai-gender { color: #4170eb; font-weight: 700;}
.ai-conf { color: #2eb8c9; font-weight: 700;}
</style>

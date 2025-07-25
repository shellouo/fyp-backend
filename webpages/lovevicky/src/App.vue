<template>
  <div class="aurora-bg">
    <canvas ref="canvasRef" class="stars-canvas"></canvas>
  </div>
  <LayoutHeader />
  <router-view />
  <LayoutFooter />
  <FluidAuroraCursor />
</template>


<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import LayoutHeader from './components/layout/Header.vue'
import LayoutFooter from './components/layout/Footer.vue'

const canvasRef = ref<HTMLCanvasElement | null>(null)
let reqId: number
let stars: any[] = []
let auroras: any[] = []

function drawAuroraStars() {
  const canvas = canvasRef.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')!
  const W = window.innerWidth
  const H = window.innerHeight
  canvas.width = W
  canvas.height = H

  // Aurora strips
  auroras = Array.from({ length: 3 }, (_, i) => ({
    x: W * (0.2 + 0.3 * i),
    y: H * (0.2 + 0.2 * i),
    len: W * (0.7 - 0.15 * i),
    color: [
      'rgba(120,80,255,0.16)',
      'rgba(255,130,255,0.11)',
      'rgba(100,255,255,0.14)'
    ][i]
  }))

  // Stars
  stars = Array.from({ length: 160 }, () => ({
    x: Math.random() * W,
    y: Math.random() * H,
    r: Math.random() * 0.9 + 0.4,
    o: Math.random() * 0.6 + 0.4,
    dx: (Math.random() - 0.5) * 0.11,
    dy: (Math.random() - 0.5) * 0.11,
    period: Math.random() * 200 + 120,
    phase: Math.random() * Math.PI * 2
  }))

  let tick = 0
  function animate() {
    ctx.clearRect(0, 0, W, H)
    // Aurora gradient bg
    const gradient = ctx.createLinearGradient(0, 0, W, H)
    gradient.addColorStop(0, "#3b1960")
    gradient.addColorStop(0.35, "#6e39d9cc")
    gradient.addColorStop(0.7, "#b392e4cc")
    gradient.addColorStop(1, "#271245")
    ctx.fillStyle = gradient
    ctx.fillRect(0, 0, W, H)

    // Aurora strips
    for (const aurora of auroras) {
      ctx.save()
      ctx.translate(aurora.x, aurora.y)
      ctx.rotate(Math.sin(tick / 150 + aurora.x / 400) * 0.14)
      ctx.beginPath()
      for (let i = 0; i < aurora.len; i += 2) {
        const y = Math.sin((i / aurora.len) * Math.PI * 2 + tick / 80 + aurora.x / 80) * 16
        ctx.lineTo(i, y)
      }
      ctx.strokeStyle = aurora.color
      ctx.shadowColor = aurora.color
      ctx.shadowBlur = 36
      ctx.lineWidth = 11
      ctx.stroke()
      ctx.restore()
    }

    // Stars breathing/shine
    for (const star of stars) {
      star.x += star.dx
      star.y += star.dy
      if (star.x < 0 || star.x > W) star.dx *= -1
      if (star.y < 0 || star.y > H) star.dy *= -1
      const breath = 0.45 + 0.35 * Math.abs(Math.sin(tick / star.period + star.phase))
      ctx.beginPath()
      ctx.arc(star.x, star.y, star.r * breath, 0, Math.PI * 2)
      ctx.fillStyle = `rgba(220,210,255,${star.o * breath})`
      ctx.shadowColor = "#e4bfff"
      ctx.shadowBlur = 16 + 8 * breath
      ctx.fill()
    }
    tick++
    reqId = requestAnimationFrame(animate)
  }
  animate()
}

onMounted(() => {
  drawAuroraStars()
  window.addEventListener('resize', drawAuroraStars)
})
onUnmounted(() => {
  cancelAnimationFrame(reqId)
  window.removeEventListener('resize', drawAuroraStars)
})
</script>

<style>
.aurora-bg {
  position: fixed;
  left: 0; top: 0;
  width: 100vw; height: 100vh;
  z-index: 0;
  overflow: hidden;
  pointer-events: none;
}
.stars-canvas {
  width: 100vw; height: 100vh; display: block;
  background: transparent;
  opacity: 0.99;
}
</style>


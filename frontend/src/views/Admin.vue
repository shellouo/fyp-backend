<template>
  <div class="admin-bg-aurora">
    <canvas ref="auroraCanvas" class="aurora-canvas"></canvas>
  </div>
  <div class="admin-panel">
    <aside class="admin-sider">
      <ul>
        <li :class="{active: active==='user'}" @click="active='user'"><i class="el-icon-user"></i> User Management</li>
        <li :class="{active: active==='param'}" @click="active='param'"><i class="el-icon-setting"></i> Parameter Settings</li>
        <li :class="{active: active==='data'}" @click="active='data'"><i class="el-icon-files"></i> Data Management</li>
        <li :class="{active: active==='analytics'}" @click="active='analytics'"><i class="el-icon-data-analysis"></i> Analytics</li>
        <li :class="{active: active==='sys'}" @click="active='sys'"><i class="el-icon-s-tools"></i> System Settings</li>
        <li :class="{active: active==='logs'}" @click="active='logs'"><i class="el-icon-document"></i> Logs</li>
      </ul>
    </aside>
    <section class="admin-content">
      <component :is="panelComp" />
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick } from 'vue'
import UserManager from "@/components/Admin/UserManager.vue";
import ParamSettings from "@/components/Admin/ParamSettings.vue";
import DataManager from "@/components/Admin/DataManager.vue";

const active = ref('user')
const panelComp = computed(() => {
  switch(active.value) {
    case 'user': return UserManager
    case 'param': return ParamSettings
    case 'data': return DataManager
      // 其他的也可以继续补充
    default: return UserManager
  }
})

// 极光/粒子动画（可复用前面的canvas动效代码，保持美观一致性）
const auroraCanvas = ref<HTMLCanvasElement|null>(null)
onMounted(() => {
  nextTick(() => {
    const canvas = auroraCanvas.value
    if (!canvas) return
    const ctx = canvas.getContext('2d')!
    let w = window.innerWidth, h = window.innerHeight
    canvas.width = w; canvas.height = h
    const stars = Array.from({ length: 120 }, () => ({
      x: Math.random() * w,
      y: Math.random() * h,
      r: Math.random() * 1.1 + 0.3,
      o: Math.random() * 0.5 + 0.3,
      vx: (Math.random() - 0.5) * 0.04,
      vy: (Math.random() - 0.5) * 0.05,
      color: `hsl(${190 + Math.random() * 80},80%,85%)`
    }))
    function drawAurora() {
      ctx.clearRect(0, 0, w, h)
      // Aurora gradient
      for (let band = 0; band < 2; band++) {
        const grad = ctx.createLinearGradient(0, h*0.11, w, h*0.39)
        grad.addColorStop(0, `rgba(${180+band*30},${120+band*50},255,${0.18-band*0.03})`)
        grad.addColorStop(0.7, `rgba(${100+band*70},${60+band*40},255,${0.17-band*0.02})`)
        grad.addColorStop(1, 'rgba(100,120,255,0)')
        ctx.globalAlpha = 0.45 - band*0.11
        ctx.fillStyle = grad
        ctx.beginPath()
        ctx.ellipse(w/2, h*0.2+band*20, w*0.7, h*0.18+band*13, 0.1*band, 0, 2*Math.PI)
        ctx.fill()
      }
      ctx.globalAlpha = 1
      // Stars
      for (let s of stars) {
        ctx.beginPath()
        ctx.arc(s.x, s.y, s.r, 0, Math.PI*2)
        ctx.fillStyle = s.color
        ctx.globalAlpha = s.o
        ctx.shadowBlur = 8
        ctx.shadowColor = "#c3e8ff"
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
.admin-bg-aurora {
  position: fixed; inset: 0; z-index: 0;
  width: 100vw; height: 100vh; pointer-events:none;
}
.aurora-canvas {
  width: 100vw; height: 100vh;
}
.admin-panel {
  display: flex;
  z-index: 1;
  position: relative;
  min-height: 100vh;
}
.admin-sider {
  width: 210px;
  background: #f8f7fd;
  padding-top: 32px;
  border-right: 1.5px solid #e7e7f3;
}
.admin-sider ul { list-style: none; padding: 0; margin: 0;}
.admin-sider li {
  padding: 13px 30px 13px 38px;
  cursor: pointer;
  font-weight: 500;
  color: #8d7ae3;
  border-left: 4px solid transparent;
  transition: background 0.18s, color 0.16s;
}
.admin-sider li.active, .admin-sider li:hover {
  background: #ebe3ff;
  color: #5f30dd;
  border-left: 4px solid #6f43e8;
}
.admin-content {
  flex: 1;
  padding: 30px 38px;
}
</style>

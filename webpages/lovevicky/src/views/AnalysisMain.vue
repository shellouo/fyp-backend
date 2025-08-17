<template>
  <div class="analysis-main-bg">
    <canvas ref="canvasRef" class="aurora-canvas"></canvas>
    <div class="analysis-main-content">
      <h2>Welcome to Age Analysis Dashboard</h2>
      <p>
        Choose an option below to start analyzing faces or view your previous analyses.
      </p>
      <div class="main-cards">
        <!-- Upload -->
        <el-card class="card" shadow="hover" @click="goUpload">
          <div class="icon"><i class="el-icon-upload"></i></div>
          <div class="title">Upload New Image</div>
          <div class="desc">Upload a photo or take a new one to analyze faces and determine age.</div>
          <el-button type="primary" round>Go to Upload</el-button>
        </el-card>
        <!-- History -->
        <el-card class="card" shadow="hover" @click="goHistory">
          <div class="icon"><i class="el-icon-refresh"></i></div>
          <div class="title">Historical Analysis</div>
          <div class="desc">View your previous analysis results and comparisons over time.</div>
          <el-button type="primary" round>View History</el-button>
        </el-card>
      </div>
      <el-divider></el-divider>

      <section>
        <h3>Recent Analyses</h3>
        <!-- 表格展示历史分析记录 -->
        <el-table :data="records.slice(0, 5)" border stripe style="width:100%; background:#fff;">
          <el-table-column label="#" type="index" width="50"/>
          <el-table-column prop="date" label="Date" width="140"/>
          <el-table-column prop="image" label="Image" width="80">
            <template #default="scope">
              <img :src="scope.row.image" v-if="scope.row.image" style="width:32px;height:32px; border-radius:5px;"/>
            </template>
          </el-table-column>
          <el-table-column prop="result" label="Results" width="140">
            <template #default="scope">
              <span>{{ scope.row.result }}</span>
            </template>
          </el-table-column>
          <el-table-column label="Actions" width="100">
            <template #default>
              <el-button icon="el-icon-view" circle size="mini"/>
              <el-button icon="el-icon-delete" circle size="mini"/>
            </template>
          </el-table-column>
        </el-table>
        <div style="margin:16px 0 0 0;">
          <el-progress :percentage="analysisUsedPercent" style="width:50%;"/>
          <span style="margin-left:12px;">
            You have used {{analysisUsed}} of 5 free analyses this month
          </span>
          <el-button
              v-if="analysisUsed >= 5"
              type="primary"
              @click="goUpgrade"
              class="upgrade-btn"
          >Upgrade to Premium</el-button>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAnalysisStore } from '@/store/analysis'

// 极光canvas动效
const canvasRef = ref<HTMLCanvasElement|null>(null)
const drawAuroraStars = () => {
  const canvas = canvasRef.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')!
  const w = window.innerWidth
  const h = 420
  canvas.width = w
  canvas.height = h
  ctx.clearRect(0, 0, w, h)
  for (let i = 0; i < 100; i++) {
    const x = Math.random() * w
    const y = Math.random() * h
    const r = Math.random() * 1.3 + 0.5
    ctx.globalAlpha = Math.random() * 0.7 + 0.3
    ctx.beginPath()
    ctx.arc(x, y, r, 0, 2 * Math.PI)
    ctx.fillStyle = 'white'
    ctx.shadowBlur = 8
    ctx.shadowColor = '#bbf7fe'
    ctx.fill()
  }
  // Aurora 渐变带
  const auroraGrad = ctx.createLinearGradient(0, h, w, 0)
  auroraGrad.addColorStop(0, '#c084fc')
  auroraGrad.addColorStop(0.3, '#6366f1')
  auroraGrad.addColorStop(0.7, '#818cf8')
  auroraGrad.addColorStop(1, '#f472b6')
  ctx.globalAlpha = 0.18
  ctx.beginPath()
  ctx.moveTo(0, h * 0.6)
  ctx.bezierCurveTo(w * 0.25, h * 0.7, w * 0.75, h * 0.3, w, h * 0.5)
  ctx.lineTo(w, h)
  ctx.lineTo(0, h)
  ctx.closePath()
  ctx.fillStyle = auroraGrad
  ctx.fill()
  ctx.globalAlpha = 1
}
onMounted(() => {
  drawAuroraStars()
  window.addEventListener('resize', drawAuroraStars)
})

// 跳转逻辑
const router = useRouter()
const goUpload = () => router.push('/analysis')
const goHistory = () => router.push('/upload')
const goUpgrade = () => { /* 升级实现 */ }

// 数据
const analysisStore = useAnalysisStore()
// 数据结构要确保有 date, image, result 等字段
const records = ref(analysisStore.records.map((item: any, i: number) => ({
  ...item,
  date: item.date || new Date().toLocaleDateString(),
  image: item.image || '',
  result: item.result || '--'
})))
const analysisUsed = records.value.length
const analysisUsedPercent = Math.min((analysisUsed / 5) * 100, 100)
</script>

<style scoped>
.analysis-main-bg {
  position: relative;
  min-height: 100vh;
  background: linear-gradient(120deg, #312e81 0%, #a21caf 60%, #64748b 100%);
  overflow: hidden;
}
.aurora-canvas {
  position: absolute;
  left: 0; top: 0; width: 100vw; height: 420px; z-index: 1; pointer-events: none;
}
.analysis-main-content {
  position: relative; z-index: 2; padding: 40px 40px 0 40px;
  max-width: 1100px; margin: 0 auto;
  color: #fff;
}
.main-cards {
  display: flex; gap: 32px; margin: 32px 0;
}
.card {
  flex: 1;
  background: #f7f8fc;
  border-radius: 10px;
  text-align: center; padding: 30px 14px 16px 14px;
  box-shadow: 0 2px 16px #dfc3fa30;
  transition: box-shadow .2s;
  cursor: pointer;
}
.card:hover { box-shadow: 0 10px 40px #c6b8f770; }
.icon { font-size: 44px; color: #8c5cff; margin-bottom: 8px;}
.title { font-size: 19px; font-weight: bold; margin-bottom: 6px; color: #7c3aed;}
.desc { font-size: 13px; color: #777; margin-bottom: 16px;}
.upgrade-btn { margin-left: 24px; animation: glowPulse 1.2s infinite alternate;}
@keyframes glowPulse {
  from { box-shadow:0 0 18px 0 #a21caf60 }
  to   { box-shadow:0 0 24px 6px #f472b690 }
}
</style>

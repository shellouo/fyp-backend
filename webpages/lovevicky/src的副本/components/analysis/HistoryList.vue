<template>
  <div class="history-list">
    <div v-for="(h,i) in history" :key="i" class="history-item">
      <span class="date">{{ h.time }}</span>
      <span class="age">{{ h.age.toFixed(1) }}</span> yrs
      <span class="gender">{{ h.gender }}</span>
      <span class="conf">{{ (h.confidence*100).toFixed(1) }}%</span>
    </div>
  </div>
</template>
<script setup lang="ts">
const props = defineProps<{ history: any[] }>()
</script>
<style scoped>
.history-list { margin: 30px 0; }
.history-item {
  background: rgba(240,245,255,0.98);
  border-radius: 7px;
  margin-bottom: 9px; padding: 7px 20px;
  box-shadow: 0 1px 6px #b4c4ff11;
  font-size: 15px;
}
.date { color: #a6a9b8; margin-right: 16px; }
.age { color: #7a52fa; font-weight: bold; margin: 0 7px;}
.gender { color: #4170eb; font-weight: 600; margin: 0 6px;}
.conf { color: #2eb8c9; font-weight: 600; margin: 0 6px;}
</style>

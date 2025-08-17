<<template>
  <div class="stars-bg">
    <!-- 可以插入canvas极光/粒子动画效果 -->
  </div>
  <div class="center-container">
    <LoginForm @switchToRegister="goRegister" @loginSuccess="goAnalysisMain" />
  </div>
</template>

<script setup lang="ts">
import LoginForm from '@/components/user/LoginForm.vue'
import { useRouter } from 'vue-router'
import { watchEffect } from 'vue'
import { useUserStore } from "@/store/user"

const router = useRouter()
const store = useUserStore()

// 登录状态监听，已登录就跳转（支持第三方登录等情况）
watchEffect(() => {
  if (store.isLogin) {
    router.replace('/analysis-main')
  }
})

// 登录表单内主动触发（比如表单submit时传递 @loginSuccess）
function goAnalysisMain() {
  router.push('/analysis-main')
}
function goRegister() {
  router.push('/register')
}
</script>

<style scoped>
.stars-bg {
  position: fixed;
  z-index: 0;
  left: 0; top: 0; right: 0; bottom: 0;
  width: 100vw; height: 100vh;
  background: radial-gradient(ellipse at 60% 40%, #9f79ff 10%, #252142 100%);
  animation: auroraMove 8s linear infinite alternate;
  /* 可以引入canvas特效或粒子动效 */
}
.center-container {
  position: relative;
  z-index: 1;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
}
@keyframes auroraMove {
  0% { background-position: 0% 50%;}
  100% { background-position: 100% 50%;}
}
</style>


import { createPinia } from 'pinia'

// ---- 插件扩展区（如持久化/自定义插件/中间件）----

// 例如：使用 pinia-plugin-persistedstate 持久化插件
// import piniaPersistedstate from 'pinia-plugin-persistedstate'

// 创建 pinia 实例
const pinia = createPinia()

// 使用插件（可选，按需开启）
// pinia.use(piniaPersistedstate)

// 你可以在这里挂载多个插件，便于后期维护
// pinia.use(yourCustomPlugin)

export default pinia




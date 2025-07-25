
import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import { useUserStore } from '../store/user'

// 路由懒加载
import Home from '../views/Home.vue'

const Register = () => import('../views/Register.vue')
const Login = () => import('../views/Login.vue')
const AnalysisMain = () => import('../views/AnalysisMain.vue')
const Upload = () => import('../views/Upload.vue')
const Analysis = () => import('../views/Analysis.vue')
const Admin = () => import('../views/Admin.vue')
const NotFound = () => import('../views/NotFound.vue') // 404页可选

const routes: RouteRecordRaw[] = [
    { path: '/', name: 'Home', component: Home },
    { path: '/register', name: 'Register', component: Register },
    { path: '/login', name: 'Login', component: Login },
    // 受保护页面（需要用户登录）
    {
        path: '/analysis-main',
        name: 'AnalysisMain',
        component: AnalysisMain,
        meta: { requiresAuth: true }
    },
    {
        path: '/upload',
        name: 'Upload',
        component: Upload,
        meta: { requiresAuth: true }
    },
    {
        path: '/analysis',
        name: 'Analysis',
        component: Analysis,
        meta: { requiresAuth: true }
    },
    // 管理员专属页面
    {
        path: '/admin',
        name: 'Admin',
        component: Admin,
        meta: { requiresAuth: true, requiresAdmin: true }
    },
    // 404 Not Found
    { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFound }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

// 路由守卫：鉴权+自动跳转+高亮反馈
router.beforeEach(async (to, from, next) => {
    const store = useUserStore()

    // 可选：自动检测用户登录（比如刷新后自动读本地缓存或cookie）
    await store.autoLoginIfNeeded?.()

    // 需要登录
    if (to.meta.requiresAuth && !store.isLogin) {
        return next({ path: '/login', query: { redirect: to.fullPath } })
    }
    // 需要管理员权限
    if (to.meta.requiresAdmin && !store.isAdmin) {
        return next({ path: '/', query: { error: 'NoAdminPermission' } })
    }
    // 登录页禁止已登录用户访问
    if ((to.path === '/login' || to.path === '/register') && store.isLogin) {
        return next({ path: '/analysis-main' })
    }
    next()
})




export default router
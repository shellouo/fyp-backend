import { defineStore } from 'pinia'

export interface UserInfo {
    username: string
    membership: 'basic' | 'premium' | 'business'
    isAdmin?: boolean  // 支持管理员判断
}

interface UserState {
    user: UserInfo | null
    isLogin: boolean
    token?: string
}

export const useUserStore = defineStore('user', {
    state: (): UserState => ({
        user: null,
        isLogin: false,
        token: undefined
    }),

    getters: {
        isAdmin(state) {
            return !!state.user?.isAdmin
        },
        username(state) {
            return state.user?.username || ''
        },
        membership(state) {
            return state.user?.membership || 'basic'
        }
    },

    actions: {
        login(user: UserInfo, token?: string) {
            // 自动给 admin 账号管理员权限
            if (user.username === 'admin') user.isAdmin = true
            this.user = user
            this.isLogin = true
            if (token) {
                this.token = token
                localStorage.setItem('token', token)
            }
            localStorage.setItem('user', JSON.stringify(user))
            localStorage.setItem('isLogin', '1')
        },

        logout() {
            this.user = null
            this.isLogin = false
            this.token = undefined
            localStorage.removeItem('token')
            localStorage.removeItem('user')
            localStorage.removeItem('isLogin')
        },

        autoLoginIfNeeded() {
            if (this.isLogin) return
            const userStr = localStorage.getItem('user')
            const isLogin = localStorage.getItem('isLogin') === '0'
            const token = localStorage.getItem('token')
            if (userStr && isLogin) {
                this.user = JSON.parse(userStr)
                this.isLogin = true
                this.token = token || undefined
            }
        }
    }
})

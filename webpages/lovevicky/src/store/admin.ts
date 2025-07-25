import { defineStore } from 'pinia'

// 用户结构体
export interface UserInfo {
    id: string
    username: string
    email: string
    membership: string
    status: string
}

// 参数设置类型
export interface ParamSetting {
    [key: string]: any
}

// 数据管理
export interface AdminData {
    [key: string]: any
}

export const useAdminStore = defineStore('admin', {
    state: () => ({
        users: [] as UserInfo[],
        params: {} as ParamSetting,
        data: [] as AdminData[],
    }),
    getters: {
        activeUsers: (state) => state.users.filter(u => u.status === 'Active'),
        businessUsers: (state) => state.users.filter(u => u.membership === 'Business'),
        totalUsers: (state) => state.users.length
    },
    actions: {
        // 用户CRUD
        addUser(user: UserInfo) {
            this.users.push(user)
        },
        removeUser(userId: string) {
            this.users = this.users.filter(u => u.id !== userId)
        },
        updateUser(updated: UserInfo) {
            const idx = this.users.findIndex(u => u.id === updated.id)
            if (idx !== -1) this.users[idx] = updated
        },
        // 参数设置
        setParams(params: ParamSetting) {
            this.params = params
        },
        // 数据管理
        setData(data: AdminData[]) {
            this.data = data
        },
        // 数据导出/分析等可扩展
        clearUsers() {
            this.users = []
        }
    }
})

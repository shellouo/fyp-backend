import { defineStore } from 'pinia'

// 定义分析记录类型
export interface AnalysisRecord {
    id: string
    image: string        // 图片URL
    result: any          // 年龄分析结果结构体（可进一步定义类型）
    createdAt: string
}

// 分析结果结构体类型（可根据后端返回进一步细化）
export interface AnalysisResult {
    estimatedAge: number
    confidence: number
    gender?: string
    [key: string]: any
}

export const useAnalysisStore = defineStore('analysis', {
    state: () => ({
        records: [] as AnalysisRecord[],      // 历史记录
        currentResult: null as AnalysisResult | null
    }),
    getters: {
        recentRecords: (state) => state.records.slice(0, 5), // 最近5条分析
    },
    actions: {
        // 新增分析记录
        addRecord(record: AnalysisRecord) {
            this.records.unshift(record)
            // 持久化：可用 localStorage/sessionStorage 或API
            localStorage.setItem('analysisRecords', JSON.stringify(this.records))
        },
        // 设置当前分析结果
        setCurrent(result: AnalysisResult) {
            this.currentResult = result
        },
        // 加载历史记录（页面初始化时调用）
        loadRecords() {
            const data = localStorage.getItem('analysisRecords')
            if (data) {
                this.records = JSON.parse(data)
            }
        },
        // 清空历史
        clearHistory() {
            this.records = []
            localStorage.removeItem('analysisRecords')
        }
    }
})

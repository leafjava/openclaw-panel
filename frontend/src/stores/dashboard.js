import { defineStore } from 'pinia'
import { ref } from 'vue'
import { fetchDashboardStats } from '@/api/stats'

export const useDashboardStore = defineStore('dashboard', () => {
  const stats = ref(null)
  const loading = ref(false)
  const error = ref(null)

  async function load() {
    loading.value = true
    error.value = null
    try {
      const res = await fetchDashboardStats()
      stats.value = res.data
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }

  return { stats, loading, error, load }
})

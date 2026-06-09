import { defineStore } from 'pinia'
import { ref } from 'vue'
import { fetchChromeNewsList } from '@/api/news'

export const useChromeNewsStore = defineStore('chromeNews', () => {
  const items = ref([])
  const loading = ref(false)
  const error = ref(null)
  const totalCount = ref(0)
  const currentPage = ref(1)

  async function load(params = {}) {
    loading.value = true
    error.value = null
    try {
      const res = await fetchChromeNewsList(params)
      items.value = res.data.results
      totalCount.value = res.data.count
      currentPage.value = params.page || 1
    } catch (e) {
      error.value = e.message
    } finally {
      loading.value = false
    }
  }

  return { items, loading, error, totalCount, currentPage, load }
})

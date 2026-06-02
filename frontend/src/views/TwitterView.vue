<script setup>
import { onMounted, ref, watch } from 'vue'
import { useTwitterStore } from '@/stores/twitter'

const store = useTwitterStore()
const filters = ref({ category: '', username: '', page: 1 })

onMounted(() => store.load())

watch(filters, () => {
  const params = { ...filters.value }
  if (!params.category) delete params.category
  if (!params.username) delete params.username
  store.load(params)
}, { deep: true })

function prevPage() {
  if (filters.value.page > 1) filters.value.page--
}
function nextPage() {
  const maxPage = Math.ceil(store.totalCount / 20)
  if (filters.value.page < maxPage) filters.value.page++
}

function categoryClass(cat) {
  const map = {
    娱乐: 'bg-pink-100 text-pink-600',
    币圈: 'bg-orange-100 text-orange-600',
    金融: 'bg-emerald-100 text-emerald-600',
    IT: 'bg-blue-100 text-blue-600',
  }
  return map[cat] || 'bg-gray-100 text-gray-600'
}

function formatTime(dt) {
  if (!dt) return ''
  const d = new Date(dt)
  const now = new Date()
  const diff = now - d
  const mins = Math.floor(diff / 60000)
  if (mins < 1) return '刚刚'
  if (mins < 60) return `${mins} 分钟前`
  const hours = Math.floor(mins / 60)
  if (hours < 24) return `${hours} 小时前`
  const days = Math.floor(hours / 24)
  if (days < 7) return `${days} 天前`
  return d.toLocaleDateString('zh-CN')
}
</script>

<template>
  <div>
    <h1 class="text-2xl font-bold text-gray-900 mb-6">
      <i class="fa fa-twitter mr-2"></i> Twitter 动态
    </h1>

    <!-- 过滤栏 -->
    <div class="bg-white rounded-xl shadow-sm p-4 mb-6 border border-gray-100 flex flex-wrap gap-3 items-center">
      <div class="relative flex-1 min-w-[200px] max-w-xs">
        <i class="fa fa-search absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-sm"></i>
        <input
          v-model="filters.username"
          placeholder="用户名..."
          class="w-full pl-9 pr-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
        />
      </div>
      <div class="relative flex-1 min-w-[200px] max-w-xs">
        <i class="fa fa-filter absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-sm"></i>
        <input
          v-model="filters.category"
          placeholder="分类（娱乐 / 币圈 / 金融 / IT）"
          class="w-full pl-9 pr-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
        />
      </div>
      <button
        @click="filters = { category: '', username: '', page: 1 }"
        class="px-4 py-2 text-sm text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
      >
        <i class="fa fa-refresh mr-1"></i> 重置
      </button>
    </div>

    <!-- 加载 -->
    <div v-if="store.loading" class="text-center py-12 text-gray-400">
      <i class="fa fa-spinner fa-spin text-3xl"></i>
      <p class="mt-2">加载中...</p>
    </div>

    <!-- 错误 -->
    <div v-else-if="store.error" class="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
      <i class="fa fa-exclamation-circle mr-1"></i> {{ store.error }}
    </div>

    <!-- 动态流 -->
    <div v-else class="space-y-3">
      <div
        v-for="item in store.items"
        :key="item.id"
        class="bg-white rounded-xl shadow-sm border border-gray-100 p-5 hover:shadow-md transition-shadow"
      >
        <div class="flex gap-3">
          <!-- 头像 -->
          <div class="flex-shrink-0 w-10 h-10 rounded-full bg-sky-100 flex items-center justify-center">
            <i class="fa fa-user text-sky-500"></i>
          </div>

          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2 mb-1">
              <span class="font-semibold text-gray-900">@{{ item.username }}</span>
              <span
                class="inline-flex px-2 py-0.5 rounded-full text-xs font-medium"
                :class="categoryClass(item.category)"
              >
                {{ item.category }}
              </span>
              <span class="text-xs text-gray-400 ml-auto">{{ formatTime(item.post_time) }}</span>
            </div>
            <p class="text-sm text-gray-700 leading-relaxed whitespace-pre-wrap">{{ item.content }}</p>
          </div>
        </div>
      </div>

      <!-- 空状态 -->
      <div v-if="store.items.length === 0" class="bg-white rounded-xl border border-gray-100 p-12 text-center text-gray-400">
        <i class="fa fa-inbox text-4xl block mb-3"></i> 暂无数据
      </div>
    </div>

    <!-- 分页 -->
    <div class="flex items-center justify-between mt-6" v-if="store.totalCount > 0">
      <span class="text-sm text-gray-500">共 {{ store.totalCount }} 条</span>
      <div class="flex gap-2">
        <button
          @click="prevPage"
          :disabled="filters.page <= 1"
          class="px-4 py-2 text-sm border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
        >
          <i class="fa fa-chevron-left mr-1"></i> 上一页
        </button>
        <span class="px-4 py-2 text-sm text-gray-600">第 {{ filters.page }} 页</span>
        <button
          @click="nextPage"
          :disabled="filters.page >= Math.ceil(store.totalCount / 20)"
          class="px-4 py-2 text-sm border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
        >
          下一页 <i class="fa fa-chevron-right ml-1"></i>
        </button>
      </div>
    </div>
  </div>
</template>

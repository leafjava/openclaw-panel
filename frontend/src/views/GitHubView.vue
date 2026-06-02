<script setup>
import { onMounted, ref, watch } from 'vue'
import { useGitHubStore } from '@/stores/github'

const store = useGitHubStore()
const filters = ref({ language: '', min_stars: null, page: 1 })

onMounted(() => store.load())

watch(filters, () => {
  const params = { ...filters.value }
  if (!params.language) delete params.language
  if (!params.min_stars) delete params.min_stars
  store.load(params)
}, { deep: true })

function prevPage() {
  if (filters.value.page > 1) filters.value.page--
}
function nextPage() {
  const maxPage = Math.ceil(store.totalCount / 20)
  if (filters.value.page < maxPage) filters.value.page++
}

function getLangColor(lang) {
  const map = {
    Python: 'bg-blue-100 text-blue-700',
    JavaScript: 'bg-yellow-100 text-yellow-700',
    TypeScript: 'bg-sky-100 text-sky-700',
    Java: 'bg-orange-100 text-orange-700',
    Go: 'bg-cyan-100 text-cyan-700',
    Rust: 'bg-amber-100 text-amber-700',
    'C++': 'bg-pink-100 text-pink-700',
    Ruby: 'bg-red-100 text-red-700',
    PHP: 'bg-purple-100 text-purple-700',
  }
  return map[lang] || 'bg-gray-100 text-gray-700'
}
</script>

<template>
  <div>
    <h1 class="text-2xl font-bold text-gray-900 mb-6">
      <i class="fa fa-github mr-2"></i> GitHub 热点
    </h1>

    <!-- 过滤栏 -->
    <div class="bg-white rounded-xl shadow-sm p-4 mb-6 border border-gray-100 flex flex-wrap gap-3 items-center">
      <div class="relative flex-1 min-w-[200px] max-w-xs">
        <i class="fa fa-search absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 text-sm"></i>
        <input
          v-model="filters.language"
          placeholder="编程语言..."
          class="w-full pl-9 pr-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
        />
      </div>
      <input
        v-model.number="filters.min_stars"
        type="number"
        placeholder="最低 Stars"
        class="w-36 px-3 py-2 border border-gray-300 rounded-lg text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none"
      />
      <button
        @click="filters = { language: '', min_stars: null, page: 1 }"
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

    <!-- 表格 -->
    <div v-else class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
      <div class="overflow-x-auto">
        <table class="w-full">
          <thead class="bg-gray-50 border-b">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">项目</th>
              <th class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider hidden md:table-cell">描述</th>
              <th class="px-6 py-3 text-right text-xs font-semibold text-gray-500 uppercase tracking-wider">Stars</th>
              <th class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider">语言</th>
              <th class="px-6 py-3 text-left text-xs font-semibold text-gray-500 uppercase tracking-wider hidden sm:table-cell">日期</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr v-for="item in store.items" :key="item.id" class="hover:bg-gray-50 transition-colors">
              <td class="px-6 py-4">
                <a :href="item.url" target="_blank" rel="noopener" class="text-indigo-600 hover:text-indigo-800 hover:underline font-medium text-sm">
                  {{ item.title }}
                </a>
              </td>
              <td class="px-6 py-4 text-sm text-gray-500 max-w-sm truncate hidden md:table-cell">
                {{ item.description || '-' }}
              </td>
              <td class="px-6 py-4 text-right">
                <span class="text-sm font-mono font-semibold text-gray-900">
                  {{ item.stars.toLocaleString() }}
                </span>
              </td>
              <td class="px-6 py-4">
                <span
                  class="inline-flex px-2.5 py-0.5 rounded-full text-xs font-medium"
                  :class="getLangColor(item.language)"
                >
                  {{ item.language || 'N/A' }}
                </span>
              </td>
              <td class="px-6 py-4 text-sm text-gray-500 hidden sm:table-cell">{{ item.trending_date }}</td>
            </tr>
            <tr v-if="store.items.length === 0">
              <td colspan="5" class="px-6 py-12 text-center text-gray-400">
                <i class="fa fa-inbox text-3xl block mb-2"></i> 暂无数据
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- 分页 -->
    <div class="flex items-center justify-between mt-4" v-if="store.totalCount > 0">
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

<script setup>
import { onMounted, computed } from 'vue'
import { useDashboardStore } from '@/stores/dashboard'

const store = useDashboardStore()

onMounted(() => store.load())

const cards = computed(() => [
  {
    title: 'GitHub 热点',
    icon: 'fa-github',
    count: store.stats?.github_count ?? '-',
    color: 'from-gray-700 to-gray-900',
    link: '/github',
  },
  {
    title: '新闻热点',
    icon: 'fa-newspaper-o',
    count: store.stats?.news_count ?? '-',
    color: 'from-blue-500 to-blue-700',
    link: '/news',
  },
  {
    title: 'Chrome 新闻',
    icon: 'fa-chrome',
    count: store.stats?.chrome_news_count ?? '-',
    color: 'from-emerald-500 to-emerald-700',
    link: '/chrome-news',
  },
  {
    title: 'Twitter 动态',
    icon: 'fa-twitter',
    count: store.stats?.twitter_count ?? '-',
    color: 'from-sky-400 to-sky-600',
    link: '/twitter',
  },
])
</script>

<template>
  <div>
    <h1 class="text-2xl font-bold text-gray-900 mb-6">仪表盘</h1>

    <!-- 加载状态 -->
    <div v-if="store.loading" class="text-center py-12 text-gray-400">
      <i class="fa fa-spinner fa-spin text-3xl"></i>
      <p class="mt-2">加载中...</p>
    </div>

    <!-- 错误状态 -->
    <div v-else-if="store.error" class="bg-red-50 border border-red-200 rounded-lg p-4 text-red-700">
      <i class="fa fa-exclamation-circle mr-1"></i> {{ store.error }}
    </div>

    <!-- 统计卡片 -->
    <template v-else>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-6 mb-8">
        <RouterLink
          v-for="card in cards"
          :key="card.title"
          :to="card.link"
          class="rounded-xl bg-gradient-to-br shadow-lg p-6 text-white transition-transform hover:scale-105 hover:shadow-xl"
          :class="card.color"
        >
          <div class="flex items-center justify-between">
            <div>
              <p class="text-sm opacity-80">{{ card.title }}</p>
              <p class="text-4xl font-bold mt-2">{{ card.count }}</p>
            </div>
            <i :class="`fa ${card.icon} text-5xl opacity-20`"></i>
          </div>
        </RouterLink>
      </div>

      <!-- 分类统计 -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6" v-if="store.stats">
        <!-- GitHub Top 语言 -->
        <div class="bg-white rounded-xl shadow-sm p-5 border border-gray-100">
          <h3 class="font-semibold text-gray-800 mb-3 flex items-center gap-2">
            <i class="fa fa-code text-indigo-500"></i> Top 编程语言
          </h3>
          <ul v-if="store.stats.top_languages.length" class="space-y-2">
            <li
              v-for="(lang, idx) in store.stats.top_languages"
              :key="lang.language"
              class="flex justify-between items-center py-1.5 px-2 rounded hover:bg-gray-50"
            >
              <span class="text-sm text-gray-600">
                <span class="inline-block w-5 h-5 rounded-full bg-indigo-100 text-indigo-600 text-xs text-center leading-5 mr-2">{{ idx + 1 }}</span>
                {{ lang.language || '(无)' }}
              </span>
              <span class="font-mono text-sm text-gray-900 font-medium">{{ lang.count }}</span>
            </li>
          </ul>
          <p v-else class="text-sm text-gray-400 italic">暂无数据</p>
        </div>

        <!-- 新闻 Top 分类 -->
        <div class="bg-white rounded-xl shadow-sm p-5 border border-gray-100">
          <h3 class="font-semibold text-gray-800 mb-3 flex items-center gap-2">
            <i class="fa fa-tags text-blue-500"></i> Top 新闻分类
          </h3>
          <ul v-if="store.stats.top_news_categories.length" class="space-y-2">
            <li
              v-for="(cat, idx) in store.stats.top_news_categories"
              :key="cat.category"
              class="flex justify-between items-center py-1.5 px-2 rounded hover:bg-gray-50"
            >
              <span class="text-sm text-gray-600">
                <span class="inline-block w-5 h-5 rounded-full bg-blue-100 text-blue-600 text-xs text-center leading-5 mr-2">{{ idx + 1 }}</span>
                {{ cat.category || '(无)' }}
              </span>
              <span class="font-mono text-sm text-gray-900 font-medium">{{ cat.count }}</span>
            </li>
          </ul>
          <p v-else class="text-sm text-gray-400 italic">暂无数据</p>
        </div>

        <!-- Chrome News Top 分类 -->
        <div class="bg-white rounded-xl shadow-sm p-5 border border-gray-100">
          <h3 class="font-semibold text-gray-800 mb-3 flex items-center gap-2">
            <i class="fa fa-chrome text-emerald-500"></i> Top Chrome 分类
          </h3>
          <ul v-if="store.stats.top_chrome_news_categories?.length" class="space-y-2">
            <li
              v-for="(cat, idx) in store.stats.top_chrome_news_categories"
              :key="cat.category"
              class="flex justify-between items-center py-1.5 px-2 rounded hover:bg-gray-50"
            >
              <span class="text-sm text-gray-600">
                <span class="inline-block w-5 h-5 rounded-full bg-emerald-100 text-emerald-600 text-xs text-center leading-5 mr-2">{{ idx + 1 }}</span>
                {{ cat.category || '(无)' }}
              </span>
              <span class="font-mono text-sm text-gray-900 font-medium">{{ cat.count }}</span>
            </li>
          </ul>
          <p v-else class="text-sm text-gray-400 italic">暂无数据</p>
        </div>

        <!-- Twitter Top 分类 -->
        <div class="bg-white rounded-xl shadow-sm p-5 border border-gray-100">
          <h3 class="font-semibold text-gray-800 mb-3 flex items-center gap-2">
            <i class="fa fa-pie-chart text-sky-500"></i> Top Twitter 分类
          </h3>
          <ul v-if="store.stats.top_twitter_categories.length" class="space-y-2">
            <li
              v-for="(cat, idx) in store.stats.top_twitter_categories"
              :key="cat.category"
              class="flex justify-between items-center py-1.5 px-2 rounded hover:bg-gray-50"
            >
              <span class="text-sm text-gray-600">
                <span class="inline-block w-5 h-5 rounded-full bg-sky-100 text-sky-600 text-xs text-center leading-5 mr-2">{{ idx + 1 }}</span>
                {{ cat.category || '(无)' }}
              </span>
              <span class="font-mono text-sm text-gray-900 font-medium">{{ cat.count }}</span>
            </li>
          </ul>
          <p v-else class="text-sm text-gray-400 italic">暂无数据</p>
        </div>
      </div>
    </template>
  </div>
</template>

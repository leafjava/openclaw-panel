<script setup>
import { RouterLink, RouterView } from 'vue-router'
</script>

<template>
  <div class="min-h-screen bg-gray-50">
    <!-- 顶部导航 -->
    <nav class="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-50">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center h-14">
          <!-- Logo -->
          <RouterLink to="/" class="flex items-center gap-2 mr-8">
            <i class="fa fa-database text-indigo-600 text-xl"></i>
            <span class="text-lg font-bold text-gray-900">OpenClaw Panel</span>
          </RouterLink>

          <!-- 导航链接 -->
          <div class="flex gap-1">
            <RouterLink
              to="/"
              class="px-3 py-1.5 rounded-md text-sm font-medium transition-colors"
              :class="$route.path === '/' ? 'bg-indigo-50 text-indigo-700' : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'"
            >
              <i class="fa fa-dashboard mr-1"></i> 仪表盘
            </RouterLink>
            <RouterLink
              to="/github"
              class="px-3 py-1.5 rounded-md text-sm font-medium transition-colors"
              :class="$route.path === '/github' ? 'bg-indigo-50 text-indigo-700' : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'"
            >
              <i class="fa fa-github mr-1"></i> GitHub 热点
            </RouterLink>
            <RouterLink
              to="/news"
              class="px-3 py-1.5 rounded-md text-sm font-medium transition-colors"
              :class="$route.path === '/news' ? 'bg-indigo-50 text-indigo-700' : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'"
            >
              <i class="fa fa-newspaper-o mr-1"></i> 新闻热点
            </RouterLink>
            <RouterLink
              to="/chrome-news"
              class="px-3 py-1.5 rounded-md text-sm font-medium transition-colors"
              :class="$route.path === '/chrome-news' ? 'bg-indigo-50 text-indigo-700' : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'"
            >
              <i class="fa fa-chrome mr-1"></i> Chrome 新闻
            </RouterLink>
            <RouterLink
              to="/twitter"
              class="px-3 py-1.5 rounded-md text-sm font-medium transition-colors"
              :class="$route.path === '/twitter' ? 'bg-indigo-50 text-indigo-700' : 'text-gray-600 hover:text-gray-900 hover:bg-gray-100'"
            >
              <i class="fa fa-twitter mr-1"></i> Twitter 动态
            </RouterLink>
          </div>
        </div>
      </div>
    </nav>

    <!-- 页面内容 -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
      <RouterView />
    </main>
  </div>
</template>

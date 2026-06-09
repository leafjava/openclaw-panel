import api from './index'

export function fetchNewsHotspots(params = {}) {
  return api.get('/news/', { params })
}

export function fetchNewsHotspot(id) {
  return api.get(`/news/${id}/`)
}

export function fetchChromeNewsList(params = {}) {
  return api.get('/chrome-news/', { params })
}

export function fetchChromeNewsItem(id) {
  return api.get(`/chrome-news/${id}/`)
}

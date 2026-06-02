import api from './index'

export function fetchNewsHotspots(params = {}) {
  return api.get('/news/', { params })
}

export function fetchNewsHotspot(id) {
  return api.get(`/news/${id}/`)
}

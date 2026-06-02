import api from './index'

export function fetchGitHubHotspots(params = {}) {
  return api.get('/github/', { params })
}

export function fetchGitHubHotspot(id) {
  return api.get(`/github/${id}/`)
}

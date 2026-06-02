import api from './index'

export function fetchTwitterPosts(params = {}) {
  return api.get('/twitter/', { params })
}

export function fetchTwitterPost(id) {
  return api.get(`/twitter/${id}/`)
}

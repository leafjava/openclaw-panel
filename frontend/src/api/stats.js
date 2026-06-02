import api from './index'

export function fetchDashboardStats() {
  return api.get('/stats/')
}

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    GitHubHotspotViewSet,
    NewsHotspotViewSet,
    TwitterPostViewSet,
    dashboard_stats,
)

router = DefaultRouter()
router.register(r'github', GitHubHotspotViewSet, basename='github')
router.register(r'news', NewsHotspotViewSet, basename='news')
router.register(r'twitter', TwitterPostViewSet, basename='twitter')

urlpatterns = [
    path('stats/', dashboard_stats, name='dashboard-stats'),
    path('', include(router.urls)),
]

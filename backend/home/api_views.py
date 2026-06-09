from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from .models import GitHubHotspot, NewsHotspot, ChromeNews, TwitterPost
from .serializers import (
    GitHubHotspotSerializer,
    NewsHotspotSerializer,
    ChromeNewsSerializer,
    TwitterPostSerializer,
)
from .filters import GitHubHotspotFilter, NewsHotspotFilter, ChromeNewsFilter, TwitterPostFilter


class GitHubHotspotViewSet(viewsets.ReadOnlyModelViewSet):
    """GitHub 热点 API（只读）"""
    queryset = GitHubHotspot.objects.all()
    serializer_class = GitHubHotspotSerializer
    filterset_class = GitHubHotspotFilter
    ordering_fields = ['stars', 'trending_date', 'created_at']
    ordering = ['-stars']


class NewsHotspotViewSet(viewsets.ReadOnlyModelViewSet):
    """新闻热点 API（只读）"""
    queryset = NewsHotspot.objects.all()
    serializer_class = NewsHotspotSerializer
    filterset_class = NewsHotspotFilter
    ordering_fields = ['score', 'publish_date', 'created_at']
    ordering = ['-score']


class ChromeNewsViewSet(viewsets.ReadOnlyModelViewSet):
    """Chrome 新闻 API（只读）"""
    queryset = ChromeNews.objects.all()
    serializer_class = ChromeNewsSerializer
    filterset_class = ChromeNewsFilter
    ordering_fields = ['score', 'publish_date', 'created_at']
    ordering = ['-score']


class TwitterPostViewSet(viewsets.ReadOnlyModelViewSet):
    """Twitter 动态 API（只读）"""
    queryset = TwitterPost.objects.all()
    serializer_class = TwitterPostSerializer
    filterset_class = TwitterPostFilter
    ordering_fields = ['post_time', 'created_at']
    ordering = ['-post_time']


@api_view(['GET'])
def dashboard_stats(request):
    """仪表盘统计接口"""
    return Response({
        'github_count': GitHubHotspot.objects.count(),
        'news_count': NewsHotspot.objects.count(),
        'chrome_news_count': ChromeNews.objects.count(),
        'twitter_count': TwitterPost.objects.count(),
        'top_languages': list(
            GitHubHotspot.objects.values('language')
            .annotate(count=Count('id'))
            .order_by('-count')[:5]
        ),
        'top_news_categories': list(
            NewsHotspot.objects.values('category')
            .annotate(count=Count('id'))
            .order_by('-count')[:5]
        ),
        'top_chrome_news_categories': list(
            ChromeNews.objects.values('category')
            .annotate(count=Count('id'))
            .order_by('-count')[:5]
        ),
        'top_twitter_categories': list(
            TwitterPost.objects.values('category')
            .annotate(count=Count('id'))
            .order_by('-count')[:5]
        ),
    })

import django_filters
from .models import GitHubHotspot, NewsHotspot, ChromeNews, TwitterPost


class GitHubHotspotFilter(django_filters.FilterSet):
    """GitHub 热点过滤器"""
    language = django_filters.CharFilter(lookup_expr='icontains', label='语言')
    trending_date = django_filters.DateFilter(label='趋势日期')
    trending_after = django_filters.DateFilter(field_name='trending_date', lookup_expr='gte', label='起始日期')
    trending_before = django_filters.DateFilter(field_name='trending_date', lookup_expr='lte', label='截止日期')
    min_stars = django_filters.NumberFilter(field_name='stars', lookup_expr='gte', label='最低 Stars')

    class Meta:
        model = GitHubHotspot
        fields = ['language', 'trending_date', 'min_stars']


class NewsHotspotFilter(django_filters.FilterSet):
    """新闻热点过滤器"""
    category = django_filters.CharFilter(lookup_expr='icontains', label='分类')
    source = django_filters.CharFilter(lookup_expr='icontains', label='来源')
    min_score = django_filters.NumberFilter(field_name='score', lookup_expr='gte', label='最低评分')
    max_score = django_filters.NumberFilter(field_name='score', lookup_expr='lte', label='最高评分')
    publish_date = django_filters.DateFilter(label='发布日期')
    publish_after = django_filters.DateFilter(field_name='publish_date', lookup_expr='gte', label='起始日期')
    publish_before = django_filters.DateFilter(field_name='publish_date', lookup_expr='lte', label='截止日期')

    class Meta:
        model = NewsHotspot
        fields = ['category', 'source', 'min_score', 'max_score', 'publish_date']


class ChromeNewsFilter(django_filters.FilterSet):
    """Chrome 新闻过滤器"""
    category = django_filters.CharFilter(lookup_expr='icontains', label='分类')
    source = django_filters.CharFilter(lookup_expr='icontains', label='来源')
    min_score = django_filters.NumberFilter(field_name='score', lookup_expr='gte', label='最低评分')
    max_score = django_filters.NumberFilter(field_name='score', lookup_expr='lte', label='最高评分')
    publish_date = django_filters.DateFilter(label='发布日期')
    publish_after = django_filters.DateFilter(field_name='publish_date', lookup_expr='gte', label='起始日期')
    publish_before = django_filters.DateFilter(field_name='publish_date', lookup_expr='lte', label='截止日期')

    class Meta:
        model = ChromeNews
        fields = ['category', 'source', 'min_score', 'max_score', 'publish_date']


class TwitterPostFilter(django_filters.FilterSet):
    """Twitter 动态过滤器"""
    category = django_filters.CharFilter(lookup_expr='icontains', label='分类')
    username = django_filters.CharFilter(lookup_expr='icontains', label='用户名')
    post_after = django_filters.DateTimeFilter(field_name='post_time', lookup_expr='gte', label='起始时间')
    post_before = django_filters.DateTimeFilter(field_name='post_time', lookup_expr='lte', label='截止时间')

    class Meta:
        model = TwitterPost
        fields = ['category', 'username']

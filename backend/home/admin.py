from django.contrib import admin
from .models import GitHubHotspot, NewsHotspot, TwitterPost


@admin.register(GitHubHotspot)
class GitHubHotspotAdmin(admin.ModelAdmin):
    list_display = ('title', 'stars', 'language', 'trending_date', 'created_at')
    list_filter = ('language', 'trending_date')
    search_fields = ('title', 'description')
    date_hierarchy = 'trending_date'


@admin.register(NewsHotspot)
class NewsHotspotAdmin(admin.ModelAdmin):
    list_display = ('title', 'score', 'category', 'source', 'publish_date', 'created_at')
    list_filter = ('category', 'source', 'score')
    search_fields = ('title', 'summary')
    date_hierarchy = 'publish_date'


@admin.register(TwitterPost)
class TwitterPostAdmin(admin.ModelAdmin):
    list_display = ('username', 'category', 'content_preview', 'post_time', 'created_at')
    list_filter = ('category', 'username')
    search_fields = ('content', 'username')
    date_hierarchy = 'post_time'

    @admin.display(description='内容预览')
    def content_preview(self, obj):
        return obj.content[:50]

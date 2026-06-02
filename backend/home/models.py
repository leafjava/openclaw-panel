from django.db import models
from django.utils import timezone


class GitHubHotspot(models.Model):
    """GitHub 热点项目"""
    title = models.CharField(max_length=500, verbose_name='项目名称')
    url = models.URLField(max_length=500, unique=True, verbose_name='项目链接')
    description = models.TextField(blank=True, default='', verbose_name='项目描述')
    stars = models.PositiveIntegerField(default=0, verbose_name='Stars 数')
    language = models.CharField(max_length=100, blank=True, default='', verbose_name='编程语言')
    trending_date = models.DateField(default=timezone.now, verbose_name='趋势日期')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='收录时间')

    class Meta:
        ordering = ['-stars']
        verbose_name = 'GitHub 热点'
        verbose_name_plural = 'GitHub 热点'

    def __str__(self):
        return f'{self.title} ({self.stars}⭐)'


class NewsHotspot(models.Model):
    """新闻热点"""
    title = models.CharField(max_length=500, verbose_name='标题')
    url = models.URLField(max_length=500, verbose_name='原文链接')
    source = models.CharField(max_length=100, verbose_name='来源')
    summary = models.TextField(verbose_name='摘要')
    score = models.PositiveSmallIntegerField(verbose_name='AI 评分')  # 1-10 分
    category = models.CharField(max_length=50, verbose_name='分类')  # IT、币圈等
    publish_date = models.DateField(verbose_name='发布日期')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='收录时间')

    class Meta:
        ordering = ['-score']
        verbose_name = '新闻热点'
        verbose_name_plural = '新闻热点'

    def __str__(self):
        return f'[{self.score}分] {self.title} - {self.source}'


class TwitterPost(models.Model):
    """Twitter/X 关注博主动态"""
    post_id = models.CharField(max_length=100, unique=True, verbose_name='推文 ID')
    username = models.CharField(max_length=100, verbose_name='用户名')
    content = models.TextField(verbose_name='内容')
    category = models.CharField(max_length=50, verbose_name='分类')  # 娱乐、币圈、金融、IT
    post_time = models.DateTimeField(verbose_name='发布时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='收录时间')

    class Meta:
        ordering = ['-post_time']
        verbose_name = 'Twitter 动态'
        verbose_name_plural = 'Twitter 动态'

    def __str__(self):
        return f'@{self.username}: {self.content[:80]}'

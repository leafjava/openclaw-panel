from rest_framework import serializers
from .models import GitHubHotspot, NewsHotspot, ChromeNews, TwitterPost


class GitHubHotspotSerializer(serializers.ModelSerializer):
    class Meta:
        model = GitHubHotspot
        fields = '__all__'


class NewsHotspotSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsHotspot
        fields = '__all__'


class ChromeNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChromeNews
        fields = '__all__'


class TwitterPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = TwitterPost
        fields = '__all__'

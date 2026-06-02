"""
GitHub 热点采集命令
用法: python manage.py fetch_github
"""
import requests
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from home.models import GitHubHotspot


class Command(BaseCommand):
    help = '抓取 GitHub Trending AI/ML/LLM 相关热门仓库'

    def handle(self, *args, **options):
        self.stdout.write('开始抓取 GitHub 热点...')

        repos = self.fetch_trending_repos()
        saved_count = 0

        for repo in repos:
            _, created = GitHubHotspot.objects.update_or_create(
                url=repo['url'],
                defaults={
                    'title': repo['title'],
                    'description': repo.get('description', ''),
                    'stars': repo['stars'],
                    'language': repo.get('language', ''),
                    'trending_date': date.today(),
                }
            )
            if created:
                saved_count += 1
                self.stdout.write(self.style.SUCCESS(f'  新增: {repo["title"]} ({repo["stars"]}⭐)'))

        self.stdout.write(self.style.SUCCESS(f'完成！新增 {saved_count} 条，共处理 {len(repos)} 条'))

    def fetch_trending_repos(self):
        """使用 GitHub Search API 搜索 AI/ML 相关热门仓库"""
        yesterday = (date.today() - timedelta(days=1)).isoformat()
        keywords = 'AI+machine-learning+LLM+deep-learning+open-source+tool'

        url = 'https://api.github.com/search/repositories'
        params = {
            'q': f'{keywords}+created:>{yesterday}',
            'sort': 'stars',
            'order': 'desc',
            'per_page': 15,
        }
        headers = {
            'Accept': 'application/vnd.github+json',
            'User-Agent': 'OpenClaw-Panel/1.0',
        }

        # 如果有 GitHub Token 则使用，提升 API 速率限制
        import os
        token = os.environ.get('GITHUB_TOKEN')
        if token:
            headers['Authorization'] = f'Bearer {token}'

        try:
            resp = requests.get(url, params=params, headers=headers, timeout=30)
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as e:
            self.stderr.write(f'GitHub API 请求失败: {e}')
            return self.fetch_trending_fallback()

        repos = []
        for item in data.get('items', []):
            repos.append({
                'title': item['full_name'],
                'url': item['html_url'],
                'description': (item.get('description') or '')[:500],
                'stars': item['stargazers_count'],
                'language': item.get('language') or '',
            })

        return sorted(repos, key=lambda r: r['stars'], reverse=True)[:15]

    def fetch_trending_fallback(self):
        """备用方案：爬取 GitHub Trending 页面"""
        try:
            from bs4 import BeautifulSoup
            resp = requests.get(
                'https://github.com/trending?since=daily',
                headers={'User-Agent': 'OpenClaw-Panel/1.0'},
                timeout=30,
            )
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'html.parser')
            repos = []

            for article in soup.find_all('article', class_='Box-row')[:15]:
                h2 = article.find('h2')
                if not h2:
                    continue
                a_tag = h2.find('a')
                if not a_tag:
                    continue
                full_name = a_tag.get('href', '').strip('/')

                desc_tag = article.find('p', class_='col-9')
                description = desc_tag.text.strip() if desc_tag else ''

                lang_tag = article.find('span', itemprop='programmingLanguage')
                language = lang_tag.text.strip() if lang_tag else ''

                stars_tag = article.find('span', class_='d-inline-block float-sm-right')
                stars_text = stars_tag.text.strip() if stars_tag else '0'
                stars = int(''.join(filter(str.isdigit, stars_text)) or 0)

                repos.append({
                    'title': full_name,
                    'url': f'https://github.com/{full_name}',
                    'description': description[:500],
                    'stars': stars,
                    'language': language,
                })

            self.stdout.write(f'  从 Trending 页面获取到 {len(repos)} 条')
            return sorted(repos, key=lambda r: r['stars'], reverse=True)[:15]

        except Exception as e:
            self.stderr.write(f'Trending 页面爬取也失败: {e}')
            return []

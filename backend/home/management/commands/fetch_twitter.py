"""
Twitter 动态采集 + AI 分类命令
用法: python manage.py fetch_twitter
"""
import os
import json
import requests
from datetime import datetime
from django.utils import timezone
from django.core.management.base import BaseCommand
from home.models import TwitterPost
from openai import OpenAI


class Command(BaseCommand):
    help = '抓取 Twitter 关注博主动态并 AI 分类'

    # 默认监控的 Twitter 用户（可通过环境变量 TWITTER_USERS 追加，逗号分隔）
    DEFAULT_USERS = [
        # 在此添加要监控的用户名，例如: 'elonmusk', 'VitalikButerin'
    ]

    def add_arguments(self, parser):
        parser.add_argument('--users', type=str, help='指定用户名（逗号分隔），覆盖默认列表')

    def handle(self, *args, **options):
        self.stdout.write('开始抓取 Twitter 动态...')

        # 获取 API Key
        bearer_token = os.environ.get('TWITTER_BEARER_TOKEN')
        if not bearer_token:
            self.stderr.write('错误: 未设置 TWITTER_BEARER_TOKEN 环境变量')
            return

        api_key = os.environ.get('OPENAI_API_KEY')
        if not api_key:
            self.stderr.write('错误: 未设置 OPENAI_API_KEY 环境变量')
            return

        client = OpenAI(
            api_key=api_key,
            base_url=os.environ.get('OPENAI_BASE_URL', 'https://api.openai.com/v1'),
        )
        model = os.environ.get('OPENAI_MODEL', 'gpt-4o-mini')

        # 获取要监控的用户列表
        if options.get('users'):
            users = [u.strip() for u in options['users'].split(',') if u.strip()]
        else:
            users = self.DEFAULT_USERS[:]
            env_users = os.environ.get('TWITTER_USERS', '')
            if env_users:
                users.extend([u.strip() for u in env_users.split(',') if u.strip()])

        if not users:
            self.stderr.write('未配置监控用户。请设置 TWITTER_USERS 环境变量或使用 --users 参数')
            self.stderr.write('示例: python manage.py fetch_twitter --users "elonmusk,VitalikButerin"')
            return

        self.stdout.write(f'监控用户: {", ".join(users)}')

        saved_count = 0
        for username in users:
            tweets = self.fetch_user_tweets(bearer_token, username)
            self.stdout.write(f'  @{username}: 获取 {len(tweets)} 条推文')

            for tweet in tweets:
                # AI 分类
                category = self.ai_classify(client, model, tweet['content'])
                if category is None:
                    continue

                # 保存
                _, created = TwitterPost.objects.update_or_create(
                    post_id=tweet['post_id'],
                    defaults={
                        'username': tweet['username'],
                        'content': tweet['content'],
                        'category': category,
                        'post_time': tweet['post_time'],
                    }
                )
                if created:
                    saved_count += 1
                    self.stdout.write(self.style.SUCCESS(f'    [{category}] {tweet["content"][:50]}'))

        self.stdout.write(self.style.SUCCESS(f'完成！新增 {saved_count} 条动态'))

    def fetch_user_tweets(self, bearer_token, username, max_results=10):
        """通过 Twitter API v2 获取用户最新推文"""
        # 先根据用户名获取 user_id
        user_id = self.get_user_id(bearer_token, username)
        if not user_id:
            return []

        url = f'https://api.x.com/2/users/{user_id}/tweets'
        params = {
            'max_results': min(max_results, 10),
            'tweet.fields': 'created_at,text',
            'exclude': 'retweets,replies',
        }
        headers = {
            'Authorization': f'Bearer {bearer_token}',
            'User-Agent': 'OpenClaw-Panel/1.0',
        }

        try:
            resp = requests.get(url, params=params, headers=headers, timeout=30)
            resp.raise_for_status()
            data = resp.json()
        except requests.RequestException as e:
            self.stderr.write(f'    API 请求失败: {e}')
            return []

        tweets = []
        for tweet in data.get('data', []):
            tweets.append({
                'post_id': tweet['id'],
                'username': username,
                'content': tweet['text'],
                'post_time': datetime.fromisoformat(tweet['created_at'].replace('Z', '+00:00')),
            })

        return tweets

    def get_user_id(self, bearer_token, username):
        """根据用户名获取 Twitter user_id"""
        url = f'https://api.x.com/2/users/by/username/{username}'
        headers = {
            'Authorization': f'Bearer {bearer_token}',
            'User-Agent': 'OpenClaw-Panel/1.0',
        }

        try:
            resp = requests.get(url, headers=headers, timeout=30)
            resp.raise_for_status()
            return resp.json()['data']['id']
        except Exception as e:
            self.stderr.write(f'    获取 @{username} 的 user_id 失败: {e}')
            return None

    def ai_classify(self, client, model, content):
        """调用 OpenAI 兼容 API 对推文分类"""
        prompt = f"""请将以下推文分类。分类选项：娱乐、币圈、金融、IT、其他。

推文内容：
{content}

请只返回一个 JSON 对象，不要包含其他文字：
{{"category": "币圈"}}"""

        try:
            message = client.chat.completions.create(
                model=model,
                max_tokens=50,
                temperature=0.3,
                messages=[
                    {"role": "system", "content": "你只返回 JSON，不返回其他内容。"},
                    {"role": "user", "content": prompt},
                ],
            )
            text = message.choices[0].message.content.strip()
            if '```' in text:
                text = text.split('```')[1]
                if text.startswith('json'):
                    text = text[4:]
                text = text.strip()
            result = json.loads(text)
            category = result.get('category', '其他')
            # 确保分类在有效选项中
            valid_categories = ['娱乐', '币圈', '金融', 'IT', '其他']
            return category if category in valid_categories else '其他'
        except Exception as e:
            self.stderr.write(f'    AI 分类失败: {e}')
            return '其他'

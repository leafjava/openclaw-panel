"""
Chrome 新闻资讯采集 + AI 评分命令
用法: python manage.py fetch_chromeNews
"""
import os
import json
import requests
from datetime import date
from django.core.management.base import BaseCommand
from home.models import ChromeNews
from openai import OpenAI


# RSS 源配置
RSS_SOURCES = [
    {
        'name': 'TechCrunch',
        'url': 'https://techcrunch.com/feed/',
        'category': 'IT',
    },
    {
        'name': 'CoinDesk',
        'url': 'https://www.coindesk.com/arc/outboundfeeds/rss/',
        'category': '币圈',
    },
    {
        'name': 'BBC Technology',
        'url': 'https://feeds.bbci.co.uk/news/technology/rss.xml',
        'category': 'IT',
    },
    {
        'name': 'Reuters Technology',
        'url': 'https://www.reutersagency.com/feed/?taxonomy=best-sectors&post_type=best&best-sectors=tech',
        'category': 'IT',
    },
]


class Command(BaseCommand):
    help = '抓取 Chrome 新闻资讯并调用 AI 评分，score >= 5 的存入数据库'

    def handle(self, *args, **options):
        self.stdout.write('开始抓取 Chrome 新闻资讯...')

        api_key = os.environ.get('OPENAI_API_KEY')
        if not api_key:
            self.stderr.write('错误: 未设置 OPENAI_API_KEY 环境变量')
            return

        client = OpenAI(
            api_key=api_key,
            base_url=os.environ.get('OPENAI_BASE_URL', 'https://api.openai.com/v1'),
        )
        model = os.environ.get('OPENAI_MODEL', 'gpt-4o-mini')
        all_news = []

        # 1. 从各个 RSS 源抓取
        for source in RSS_SOURCES:
            items = self.fetch_rss(source)
            all_news.extend(items)
            self.stdout.write(f'  {source["name"]}: 获取 {len(items)} 条')

        self.stdout.write(f'共获取 {len(all_news)} 条，开始 AI 评分...')

        saved_count = 0
        for i, news in enumerate(all_news):
            # 2. 调用 AI API 进行评分和摘要
            result = self.ai_score(client, model, news)
            if result is None:
                continue

            score = result.get('score', 0)
            if score < 5:
                continue

            # 3. 存入数据库
            _, created = ChromeNews.objects.update_or_create(
                url=news['url'],
                defaults={
                    'title': news['title'],
                    'source': news['source'],
                    'summary': result.get('summary_zh', news.get('summary', '')),
                    'score': score,
                    'category': result.get('category', news['category']),
                    'publish_date': news.get('publish_date', date.today()),
                }
            )
            if created:
                saved_count += 1
                self.stdout.write(self.style.SUCCESS(f'  [{score}分] {news["title"][:50]}'))

        self.stdout.write(self.style.SUCCESS(f'完成！保留 {saved_count} 条（评分 ≥ 5）'))

    def fetch_rss(self, source):
        """解析 RSS 源"""
        try:
            import xml.etree.ElementTree as ET
            resp = requests.get(source['url'], timeout=30, headers={'User-Agent': 'OpenClaw-Panel/1.0'})
            resp.raise_for_status()
            root = ET.fromstring(resp.content)

            # RSS 2.0 格式
            items = []
            for item in root.iter('item'):
                title = item.find('title')
                link = item.find('link')
                desc = item.find('description')
                pub_date = item.find('pubDate')

                if title is None or link is None:
                    continue

                # 清理 HTML 标签获取纯文本摘要
                summary = desc.text if desc is not None else ''
                if summary:
                    from bs4 import BeautifulSoup
                    soup = BeautifulSoup(summary, 'html.parser')
                    summary = soup.get_text()[:500]

                items.append({
                    'title': title.text.strip() if title.text else '',
                    'url': link.text.strip() if link.text else '',
                    'summary': summary,
                    'source': source['name'],
                    'category': source['category'],
                    'publish_date': date.today(),
                })

            return items
        except Exception as e:
            self.stderr.write(f'  RSS 解析失败 ({source["name"]}): {e}')
            return []

    def ai_score(self, client, model, news):
        """调用 OpenAI 兼容 API 评分"""
        prompt = f"""你是一个新闻质量评估器。请对以下新闻进行评分和分类。

新闻标题: {news['title']}
新闻来源: {news['source']}
内容摘要: {news.get('summary', '无')}

评分标准（1-10分）:
- 相关性: 是否与 IT、AI、区块链、科技、金融相关
- 时效性: 是否是近期热点
- 信息密度: 是否包含实质性内容
- 可信度: 来源是否可靠

分类选项: IT、币圈、金融、科技、其他

请只返回一个 JSON 对象，不要包含其他文字:
{{"score": 7, "category": "IT", "summary_zh": "用中文写一句简短摘要（20字以内）"}}"""

        try:
            message = client.chat.completions.create(
                model=model,
                max_tokens=200,
                temperature=0.3,
                messages=[
                    {"role": "system", "content": "你只返回 JSON，不返回其他内容。"},
                    {"role": "user", "content": prompt},
                ],
            )
            text = message.choices[0].message.content.strip()
            # 提取 JSON（可能包裹在 ``` 中）
            if '```' in text:
                text = text.split('```')[1]
                if text.startswith('json'):
                    text = text[4:]
                text = text.strip()
            return json.loads(text)
        except (json.JSONDecodeError, Exception) as e:
            self.stderr.write(f'  AI 评分失败: {e}')
            return None

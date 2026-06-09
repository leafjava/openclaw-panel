"""
保存新闻热点数据到数据库（接收 Claude Code Skill 传入的 JSON）
用法: python manage.py save_news --json '[{...}]'
"""
import json
from datetime import date
from django.core.management.base import BaseCommand
from home.models import NewsHotspot


class Command(BaseCommand):
    help = '保存新闻热点数据到数据库'

    def add_arguments(self, parser):
        parser.add_argument('--json', type=str, required=True, help='JSON 数组字符串')

    def handle(self, *args, **options):
        try:
            data = json.loads(options['json'])
            new_count = 0
            for item in data:
                _, created = NewsHotspot.objects.update_or_create(
                    url=item['url'],
                    defaults={
                        'title': item.get('title', ''),
                        'source': item.get('source', ''),
                        'summary': item.get('summary', ''),
                        'score': item.get('score', 0),
                        'category': item.get('category', '其他'),
                        'publish_date': date.fromisoformat(
                            item.get('publish_date', str(date.today()))
                        ),
                    }
                )
                if created:
                    new_count += 1
            self.stdout.write(self.style.SUCCESS(
                f'新闻: 新增 {new_count} 条（评分 ≥ 5），共处理 {len(data)} 条'
            ))
        except json.JSONDecodeError as e:
            self.stderr.write(f'JSON 解析失败: {e}')
        except Exception as e:
            self.stderr.write(f'保存失败: {e}')

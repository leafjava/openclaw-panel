"""
保存 Twitter 推文到数据库（接收 Claude Code Skill 传入的 JSON）
用法: python manage.py save_twitter --json '[{...}]'
"""
import json
from datetime import datetime
from django.core.management.base import BaseCommand
from home.models import TwitterPost


class Command(BaseCommand):
    help = '保存 Twitter 推文到数据库'

    def add_arguments(self, parser):
        parser.add_argument('--json', type=str, required=True, help='JSON 数组字符串')

    def handle(self, *args, **options):
        try:
            data = json.loads(options['json'])
            new_count = 0
            for item in data:
                post_time_str = item.get('post_time', '')
                post_time = datetime.fromisoformat(
                    post_time_str.replace('Z', '+00:00')
                ) if post_time_str else datetime.now()

                _, created = TwitterPost.objects.update_or_create(
                    post_id=item['post_id'],
                    defaults={
                        'username': item.get('username', ''),
                        'content': item.get('content', ''),
                        'category': item.get('category', '其他'),
                        'post_time': post_time,
                    }
                )
                if created:
                    new_count += 1
            self.stdout.write(self.style.SUCCESS(
                f'Twitter: 新增 {new_count} 条，共处理 {len(data)} 条'
            ))
        except json.JSONDecodeError as e:
            self.stderr.write(f'JSON 解析失败: {e}')
        except Exception as e:
            self.stderr.write(f'保存失败: {e}')

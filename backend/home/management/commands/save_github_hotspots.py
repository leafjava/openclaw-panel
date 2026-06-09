import json
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = '保存 GitHub 热点数据'

    def add_arguments(self, parser):
        parser.add_argument('--json', type=str, required=True)

    def handle(self, *args, **options):
        data = json.loads(options['json'])
        # TODO: 替换为你的 Model，例如 from home.models import GitHubHotspot
        # 然后保存数据到数据库
        self.stdout.write(self.style.SUCCESS(f'收到 {len(data)} 条 GitHub 热点数据'))

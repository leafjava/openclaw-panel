#!/bin/bash
# OpenClaw Panel 一键部署脚本
# 适用于 Ubuntu 20.04+ / Debian 11+
set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  OpenClaw Panel 一键部署脚本${NC}"
echo -e "${GREEN}========================================${NC}"

# ------ 1. 基础依赖 ------
echo -e "${YELLOW}[1/7] 安装系统依赖...${NC}"
sudo apt update
sudo apt install -y python3 python3-pip python3-venv nginx mysql-server git curl

# ------ 2. 创建目录结构 ------
echo -e "${YELLOW}[2/7] 创建目录...${NC}"
sudo mkdir -p /opt/openclaw-panel /var/log/openclaw
sudo chown -R $USER:$USER /opt/openclaw-panel
sudo chown -R www-data:www-data /var/log/openclaw

# ------ 3. 克隆项目（如已手动克隆则跳过）------
if [ ! -f "/opt/openclaw-panel/backend/manage.py" ]; then
    echo -e "${YELLOW}[3/7] 请手动将项目代码放置到 /opt/openclaw-panel/${NC}"
    echo "    然后重新运行此脚本"
    exit 1
fi

# ------ 4. Python 虚拟环境 ------
echo -e "${YELLOW}[4/7] 配置 Python 环境...${NC}"
cd /opt/openclaw-panel
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
pip install gunicorn

# ------ 5. 前端构建 ------
echo -e "${YELLOW}[5/7] 构建前端...${NC}"
cd /opt/openclaw-panel/frontend
npm install && npm run build

# ------ 6. Django 初始化 ------
echo -e "${YELLOW}[6/7] 初始化 Django...${NC}"
cd /opt/openclaw-panel/backend
source ../venv/bin/activate

# 加载环境变量
set -a
source config/.env
set +a

python manage.py migrate
python manage.py collectstatic --noinput

# ------ 7. 启动服务 ------
echo -e "${YELLOW}[7/7] 启动服务...${NC}"

# systemd 服务
sudo cp /opt/openclaw-panel/deploy/openclaw.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable openclaw
sudo systemctl restart openclaw

# nginx
sudo cp /opt/openclaw-panel/deploy/nginx.conf /etc/nginx/sites-available/openclaw
sudo ln -sf /etc/nginx/sites-available/openclaw /etc/nginx/sites-enabled/
sudo nginx -t && sudo systemctl reload nginx

# cron 定时任务
crontab /opt/openclaw-panel/deploy/crontab

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}  部署完成！${NC}"
echo -e "${GREEN}  访问地址: http://服务器IP${NC}"
echo -e "${GREEN}========================================${NC}"

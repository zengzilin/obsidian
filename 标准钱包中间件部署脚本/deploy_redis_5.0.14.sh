#!/bin/bash
set -e

# ==========================
# Redis 5.0.14 安装脚本（Rocky Linux 8/9）
# ==========================

REDIS_VERSION="5.0.14"
REDIS_USER="redis"
INSTALL_DIR="/usr/local/bin"
CONFIG_FILE="/etc/redis.conf"
DATA_DIR="/var/lib/redis"
LOG_DIR="/var/log/redis"
PASSWORD="redis"  # 请修改为更安全的密码

echo "🚀 开始安装 Redis $REDIS_VERSION ..."

# 1. 安装依赖
echo "📦 安装编译依赖..."
dnf install -y gcc make  tcl wget tar procps

# 2. 创建 redis 用户（无登录 shell）
if ! id "$REDIS_USER" &>/dev/null; then
    useradd --system --no-create-home --shell /sbin/nologin "$REDIS_USER"
    echo "✅ 创建系统用户: $REDIS_USER"
fi

# 3. 下载并编译 Redis
cd /tmp
if [ ! -f "redis-$REDIS_VERSION.tar.gz" ]; then
    wget "https://download.redis.io/releases/redis-$REDIS_VERSION.tar.gz"
fi
tar xzf "redis-$REDIS_VERSION.tar.gz"
cd "redis-$REDIS_VERSION"

echo "🔨 编译 Redis..."
make -j$(nproc)

# 可选：运行测试（耗时约1-2分钟）
# make test

echo "💾 安装二进制文件到 $INSTALL_DIR ..."
make install

# 4. 创建数据和日志目录
mkdir -p "$DATA_DIR" "$LOG_DIR"
chown -R "$REDIS_USER:$REDIS_USER" "$DATA_DIR" "$LOG_DIR"

# 5. 生成配置文件（基于默认模板修改）
cat > "$CONFIG_FILE" <<EOF
# Redis 5.0.14 配置文件（适用于生产环境基础配置）

bind 0.0.0.0 ::1
protected-mode yes
port 6379
tcp-backlog 511
timeout 0
tcp-keepalive 300

# 守护进程模式（由 systemd 管理，此处设为 no）
daemonize no

# 由 systemd 管理 PID，不写 pidfile
# pidfile /var/run/redis_6379.pid

# 日志级别：notice（推荐）
loglevel notice
logfile "$LOG_DIR/redis.log"

# 数据库持久化目录
dir $DATA_DIR

# 启用 RDB 快照（默认）
save 900 1
save 300 10
save 60 10000

# 启用 AOF（可选，此处关闭）
appendonly no

# 安全建议：设置密码（取消注释并修改）
requirepass $PASSWORD

# 禁用高危命令（可选）
# rename-command FLUSHDB ""
# rename-command FLUSHALL ""

# 最大内存（根据需求调整，例如 256MB）
# maxmemory 268435456
# maxmemory-policy allkeys-lru

EOF

chown "$REDIS_USER:$REDIS_USER" "$CONFIG_FILE"
chmod 644 "$CONFIG_FILE"

# 6. 创建 systemd 服务文件
cat > /etc/systemd/system/redis.service <<EOF
[Unit]
Description=Redis In-Memory Data Store (5.0.14)
After=network.target

[Service]
User=$REDIS_USER
Group=$REDIS_USER
ExecStart=$INSTALL_DIR/redis-server $CONFIG_FILE
ExecStop=/bin/kill -s TERM \$MAINPID
Restart=always
RestartSec=5
Type=simple

# 安全加固（可选）
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=$DATA_DIR $LOG_DIR

[Install]
WantedBy=multi-user.target
EOF

# 7. 重载 systemd 并启动服务
systemctl daemon-reload
systemctl enable --now redis.service

# 8. 验证状态
if systemctl is-active --quiet redis; then
    echo "✅ Redis $REDIS_VERSION 已成功安装并启动！"
    echo "📋 配置文件: $CONFIG_FILE"
    echo "📋 redis初始密码: $PASSWORD"
    echo "📂 数据目录: $DATA_DIR"
    echo "📄 日志文件: $LOG_DIR/redis.log"
    echo "🔍 检查状态: systemctl status redis"
    echo "🧪 测试连接: redis-cli ping （应返回 PONG）"
else
    echo "❌ Redis 启动失败，请检查日志：journalctl -u redis -n 50"
    exit 1
fi

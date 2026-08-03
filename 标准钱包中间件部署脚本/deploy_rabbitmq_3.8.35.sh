#!/usr/bin/env bash
set -euo pipefail

# ==========================
# Rabbitmq 3.8.35 安装脚本（Rocky Linux/AlmaLinux 8/9）
# ==========================

RABBITMQ_VERSION="3.8.35"
RABBITMQ_RPM="rabbitmq-server-3.8.35-1.el8.noarch.rpm"
RABBITMQ_RPM_URL="https://github.com/rabbitmq/rabbitmq-server/releases/download/v3.8.35/${RABBITMQ_RPM}"
ERLANG_VERSION="24.3.4.10-1.el9"
RABBITMQ_CONF="/etc/rabbitmq/rabbitmq.conf"
ADMIN_USER="${1:-admin}"
ADMIN_PASSWORD="${2:-ChangeMe123!}"

wait_for_rabbitmq() {
  local retries=30
  local delay=2

  for ((i=1; i<=retries; i++)); do
    if rabbitmqctl await_startup >/dev/null 2>&1 && rabbitmqctl status >/dev/null 2>&1; then
      return 0
    fi
    sleep "${delay}"
  done

  echo "RabbitMQ 未在预期时间内完成启动，请检查服务日志。"
  echo "排查命令: journalctl -u rabbitmq-server -xe --no-pager"
  exit 1
}

if [[ "$(id -u)" -ne 0 ]]; then
  echo "请使用 root 用户执行此脚本。"
  echo "用法: sudo bash $0 [admin_user] [admin_password]"
  exit 1
fi

if ! command -v curl >/dev/null 2>&1; then
  dnf install -y curl
fi

echo "[1/9] 导入 RabbitMQ 签名证书"
rpm --import https://github.com/rabbitmq/signing-keys/releases/download/3.0/rabbitmq-release-signing-key.asc

echo "[2/9] 配置 Erlang 和 RabbitMQ 软件源"
curl -s https://packagecloud.io/install/repositories/rabbitmq/erlang/script.rpm.sh | bash
curl -s https://packagecloud.io/install/repositories/rabbitmq/rabbitmq-server/script.rpm.sh | bash

echo "[3/9] 安装指定版本 Erlang ${ERLANG_VERSION}"
dnf install -y "erlang-${ERLANG_VERSION}"

echo "[4/9] 下载 RabbitMQ Server ${RABBITMQ_VERSION} RPM 包"
curl -L -o "/tmp/${RABBITMQ_RPM}" "${RABBITMQ_RPM_URL}"

echo "[5/9] 安装 RabbitMQ Server"
dnf install -y "/tmp/${RABBITMQ_RPM}"

echo "[6/9] 创建 RabbitMQ 配置文件"
mkdir -p /etc/rabbitmq
cat > "${RABBITMQ_CONF}" <<EOF
listeners.tcp.default = 5672
management.listener.port = 15672
management.listener.ssl = false
EOF

echo "[7/9] 启用管理插件"
rabbitmq-plugins enable --offline rabbitmq_management

echo "[8/9] 启动并设置开机自启"
systemctl enable rabbitmq-server
systemctl restart rabbitmq-server
wait_for_rabbitmq

echo "[9/9] 创建管理员用户并授权"
if rabbitmqctl list_users -q | awk '{print $1}' | grep -Fxq "${ADMIN_USER}"; then
  rabbitmqctl change_password "${ADMIN_USER}" "${ADMIN_PASSWORD}"
else
  rabbitmqctl add_user "${ADMIN_USER}" "${ADMIN_PASSWORD}"
fi
rabbitmqctl set_user_tags "${ADMIN_USER}" administrator
rabbitmqctl set_permissions -p / "${ADMIN_USER}" ".*" ".*" ".*"

echo
echo "RabbitMQ 部署完成。"
echo "管理后台: http://$(hostname -I | awk '{print $1}'):15672"
echo "用户名: ${ADMIN_USER}"
echo "密码: ${ADMIN_PASSWORD}"
echo "配置文件: ${RABBITMQ_CONF}"

#!/usr/bin/env bash
set -euo pipefail

SERVICE_NAME="gcsfuse-tiqmo-logs"
SERVICE_FILE="/etc/systemd/system/${SERVICE_NAME}.service"
MOUNT_DIR="/mnt/tiqmo_logs"
BUCKET_NAME="tiqmo-p-wallyt-logs-bucket"

if [[ "$(id -u)" -ne 0 ]]; then
  echo "请使用 root 用户执行此脚本。"
  echo "用法: sudo bash $0"
  exit 1
fi

if ! command -v gcsfuse >/dev/null 2>&1; then
  echo "未检测到 gcsfuse，请先安装后再执行。"
  exit 1
fi

if command -v fusermount3 >/dev/null 2>&1; then
  FUSERMOUNT_BIN="$(command -v fusermount3)"
elif command -v fusermount >/dev/null 2>&1; then
  FUSERMOUNT_BIN="$(command -v fusermount)"
else
  echo "未检测到 fusermount 或 fusermount3。"
  exit 1
fi

mkdir -p "${MOUNT_DIR}"

if [[ -f /etc/fuse.conf ]] && ! grep -q '^user_allow_other' /etc/fuse.conf; then
  echo 'user_allow_other' >> /etc/fuse.conf
fi

cat > "${SERVICE_FILE}" <<EOF
[Unit]
Description=Mount GCS bucket ${BUCKET_NAME} with gcsfuse
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStartPre=/usr/bin/mkdir -p ${MOUNT_DIR}
ExecStart=/usr/bin/gcsfuse --foreground -o allow_other --implicit-dirs --stat-cache-ttl 10s --type-cache-ttl 10s --file-mode=777 --dir-mode=777 ${BUCKET_NAME} ${MOUNT_DIR}
ExecStop=${FUSERMOUNT_BIN} -u ${MOUNT_DIR}
Restart=always
RestartSec=5
KillMode=process

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable "${SERVICE_NAME}"
systemctl restart "${SERVICE_NAME}"

echo "部署完成。"
echo "查看状态: systemctl status ${SERVICE_NAME}"
echo "查看日志: journalctl -u ${SERVICE_NAME} -f"

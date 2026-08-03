# GCP vm的auditd.conf文件安全配置过于严格导致vm起不来

原错误配置和正确配置对比

| 配置项 | 当前值 (`/etc/audit/auditd.conf`<br/>) | 原值 (`.bak`<br/>) | 含义 |
| --- | --- | --- | --- |
| `max_log_file_action` | `ROTATE` | `keep_logs` | 日志满时轮转 vs 可能无限追加 |
| `admin_space_left_action` | `syslog` | `single` | <font style="color:#DF2A3F;">空间不足时仅告警 vs 切换单用户模式</font> |
| `disk_full_action` | `syslog` | `halt` | <font style="color:#DF2A3F;">磁盘满时仅告警 vs 立即关机</font> |

正确配置

```plain
 #
# This file controls the configuration of the audit daemon
#

local_events = yes
write_logs = yes
log_file = /var/log/audit/audit.log
log_group = root
log_format = ENRICHED
flush = INCREMENTAL_ASYNC
freq = 50
max_log_file = 6
num_logs = 5
priority_boost = 4
name_format = NONE
##name = mydomain
max_log_file_action = ROTATE
space_left = 75
space_left_action = email
verify_email = yes
action_mail_acct = root
admin_space_left = 50
admin_space_left_action = syslog
disk_full_action = syslog
disk_error_action = syslog
use_libwrap = yes
##tcp_listen_port = 60
tcp_listen_queue = 5
tcp_max_per_addr = 1
##tcp_client_ports = 1024-65535
tcp_client_max_idle = 0
transport = TCP
krb5_principal = auditd
##krb5_key_file = /etc/audit/audit.key
distribute_network = no
q_depth = 2000
overflow_action = SYSLOG
max_restarts = 10
plugin_dir = /etc/audit/plugins.d
end_of_event_timeout = 2  
```


> 更新: 2026-02-12 19:50:38  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/ydnh89ou05yq170t>
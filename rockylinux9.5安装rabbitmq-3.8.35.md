# rocky linux 9.5安装 rabbitmq-3.8.35

# 添加证书

```plain
rpm--import https://github.com/rabbitmq/signing-keys/releases/download/3.0/rabbitmq-release-signing-key.asc
```

# 安装erlang源和rabbitmq-server源

```plain
curl -s https://packagecloud.io/install/repositories/rabbitmq/erlang/script.rpm.sh | sudo bash
curl -s https://packagecloud.io/install/repositories/rabbitmq/rabbitmq-server/script.rpm.sh | sudo bash
```

# 安装rabbitmq erlang 24版本

<font style="color:#DF2A3F;">版本太高，rabbitmq server会起不来！！！</font>

```plain
dnf --enablerepo=rabbitmq_erlang list erlang --showduplicates | grep "24\."
dnf install -y erlang-24.3.4.10-1.el9
```

# 下载rabbitmq-server rpm包并安装

<https://github.com/rabbitmq/rabbitmq-server/releases/download/v3.8.35/rabbitmq-server-3.8.35-1.el8.noarch.rpm>

```plain
dnf install -y  rabbitmq-server-3.8.35-1.el8.noarch.rpm
```

# 创建配置文件

**<font style="color:#DF2A3F;">RPM 安装不会自动创建 </font>**<code>**<font style="color:#DF2A3F;">rabbitmq.conf</font>**</code>

<font style="color:rgb(6, 10, 38);"></font>

cd /etc/rabbitmq/

```plain
sudo tee /etc/rabbitmq/rabbitmq.conf <<EOF
# 监听端口
listeners.tcp.default = 5672

# 管理插件端口（需启用 rabbitmq_management）
management.listener.port = 15672
management.listener.ssl = false

# 默认用户（仅首次启动时生效）
default_user = admin
default_pass = YourSecurePassword

# 数据目录（可选，默认为 /var/lib/rabbitmq）
# data_dir = /var/lib/rabbitmq
EOF
```

# 启用插件

<font style="color:#DF2A3F;">不启用插件的话，rabbitmq自定义的配置不会生效！！</font>

```plain
rabbitmq-plugins enable rabbitmq_management
```

```plain
systemctl restart rabbitmq-server
```

# 创建用户并授予管理员权限

rabbitmqctl add\_user admin StandENpWGwer4r!

rabbitmqctl set\_user\_tags admin administrator

# rabbitmq修改密码

rabbitmqctl change\_password admin StandENpWGwer4r!


> 更新: 2026-01-20 11:47:07  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/vkwym4ua1vf2sf0d>
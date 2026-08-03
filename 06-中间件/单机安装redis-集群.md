# 单机安装redis-集群

前提我已经用rpm安装了单机的redis，可以复用。

 sudo mkdir -p /etc/redis-cluster/{7001,7002,7003,7004,7005,7006}

```plain
sudo tee /etc/redis-cluster/7001/redis.conf <<EOF
port 7001
bind 0.0.0.0
cluster-enabled yes
cluster-config-file nodes-7001.conf
cluster-node-timeout 5000
appendonly yes
daemonize yes
pidfile /var/run/redis-7001.pid
logfile /var/log/redis-7001.log
dir /etc/redis-cluster/7001
EOF
```



for port in {7001..7006}; do   sudo sed -i "s|logfile /var/log/redis-cluster-$port.log|logfile ./redis.log|" /etc/redis-cluster/$port/redis.conf; done

for port in {7001..7006}; do   sudo -u redis redis-server /etc/redis-cluster/$port/redis.conf; done



> 更新: 2026-02-06 15:47:34  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/xf7rbvzfv0agfz2f>
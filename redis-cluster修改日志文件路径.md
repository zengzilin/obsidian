# redis-cluster修改日志文件路径

redis-cluster日志默认输出是redis stdout

现在需要持久化存储，通过通过修改values.yaml添加额外的configmap修改日志路径

:::color2
global:

# imageRegistry: "docker.repo.swifer.co"

storageClass: middleware-nfs

redis:

```
password: tiqmo
```

\#image:

# registry: docker.io

# repository: bitnami/redis-cluster

# tag: 7.0.8-debian-11-r14

# pullPolicy: IfNotPresent

```
#readinessProbe:

# enabled: false
```

**<font style="color:#DF2A3F;">redis:</font>**

**<font style="color:#DF2A3F;">  podAntiAffinityPreset: hard</font>**

**<font style="color:#DF2A3F;">  configmap:</font>**

**<font style="color:#DF2A3F;">       logfile /bitnami/redis/data/redis.log</font>**

resources:

```
## Example:

## limits:

##    cpu: 100m

##    memory: 128Mi

##

## Examples:

## requests:

##    cpu: 100m

##    memory: 128Mi

##

##requests:

##  cpu: 500m

##  memory: 500Mi
```

service:

ports:

```
redis: 6379
```

persistence:

enabled: true

size: 10Gi

\#volumePermissions:

\#enabled: true

cluster:

init: true

# 3 master 3 slave

nodes: 6

# each master has only one replicas

replicas: 1

update:

```
## @param cluster.update.addNodes Boolean to specify if you want to add nodes after the upgrade

## Setting this to true a hook will add nodes to the Redis&reg; cluster after the upgrade. currentNumberOfNodes and currentNumberOfReplicas is required

##

#addNodes: true

## @param cluster.update.currentNumberOfNodes Number of currently deployed Redis&reg; nodes

##

## @param cluster.update.currentNumberOfReplicas Number of currently deployed Redis&reg; replicas

##

## @param cluster.update.newExternalIPs External IPs obtained from the services for the new nodes to add to the cluster

##

newExternalIPs: []
```

metrics:

enabled: true

:::

<font style="color:#DF2A3F;"></font>

### <font style="color:rgba(0, 0, 0, 0.9);">一、NFS存储场景下的核心问题分析</font>

1. **<font style="color:rgba(0, 0, 0, 0.9);">数据残留导致配置损坏</font>**<font style="color:rgba(0, 0, 0, 0.9);">\ </font><font style="color:rgba(0, 0, 0, 0.9);">Redis集群的</font><code><font style="color:rgba(0, 0, 0, 0.9);">nodes.conf</font></code><font style="color:rgba(0, 0, 0, 0.9);"> </font><font style="color:rgba(0, 0, 0, 0.9);">和持久化数据可能残留在NFS共享目录中，即使删除PVC/PV，若NFS服务端未清理文件，重建Pod时仍会加载旧数据，导致配置冲突</font>[<font style="color:rgb(22, 119, 255);">5</font>](https://blog.csdn.net/weixin_38299857/article/details/121019699)[<font style="color:rgb(22, 119, 255);">8</font>](https://blog.csdn.net/qq_38026977/article/details/105227642)<font style="color:rgba(0, 0, 0, 0.9);">。</font>
2. **<font style="color:rgba(0, 0, 0, 0.9);">PV回收策略未生效</font>**<font style="color:rgba(0, 0, 0, 0.9);">\ </font><font style="color:rgba(0, 0, 0, 0.9);">Kubernetes中PV的回收策略（如</font><code><font style="color:rgba(0, 0, 0, 0.9);">Retain</font></code><font style="color:rgba(0, 0, 0, 0.9);">或</font><code><font style="color:rgba(0, 0, 0, 0.9);">Delete</font></code><font style="color:rgba(0, 0, 0, 0.9);">）可能未正确配置，导致NFS存储的数据未被自动清理</font>[<font style="color:rgb(22, 119, 255);">8</font>](https://blog.csdn.net/qq_38026977/article/details/105227642)<font style="color:rgba(0, 0, 0, 0.9);">。</font>

***

### <font style="color:rgba(0, 0, 0, 0.9);">二、针对性解决方案</font>

#### <font style="color:rgba(0, 0, 0, 0.9);">1.</font><font style="color:rgba(0, 0, 0, 0.9);"> </font>**<font style="color:rgba(0, 0, 0, 0.9);">手动清理NFS数据残留</font>**

```plain
bash

复制
# 登录NFS服务器 






ssh root@nfs-server-ip       
 
# 进入Redis数据存储目录（路径参考PVC配置）






cd /nfs/data/redis  
 
# 删除所有Redis节点残留文件（包括nodes.conf 和rdb/aof文件）

rm -rf ./* 
```

或者进入其中一个好的pod.

kubectl exec -it redis-cluster-0 /bin/bash

cd  /bitnami/redis/data

1001@redis-cluster-0:/bitnami/redis/data$ ls

appendonlydir  dump.rdb  nodes.conf  nodes.conf.bak  nodes.sh


> 更新: 2025-03-04 15:36:10  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/yv22vqmsaspdiqaw>
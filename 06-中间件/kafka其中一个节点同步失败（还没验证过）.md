# kafka其中一个节点同步失败（还没验证过）

**<font style="color:#DF2A3F;">还没试过！！！</font>**

# **修复步骤**

## 停止问题节点；

备份该节点的 `/bitnami/kafka/data`；

## 删除目录下的以下文件：

只删除 KRaft 的 metadata 部分，而不碰 topic 数据。

在你的情况下，应执行以下命令（⚠️ 必须先停止 Kafka 容器）：

```plain
docker stop kafka-1
cd /bitnami/kafka/data
rm -rf __cluster_metadata-0
rm -f bootstrap.checkpoint recovery-point-offset-checkpoint replication-offset-checkpoint
```

不要删掉：

* `meta.properties`
* `__consumer_offsets-*`
* 任何业务 topic 目录（如 `bulk-*`、`tiqmo-*`）

## 重启该节点，让它重新从 controller 同步元数据。


> 更新: 2025-10-08 23:17:15  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/kp0w2na4zic2fzit>
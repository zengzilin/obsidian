# kafka 主题（Topic）相关操作

#### 1. 列出所有主题

**bash**

```bash
bin/kafka-topics.sh --bootstrap-server localhost:9092 --list
```

此命令用于显示 Kafka 集群中所有的主题名称。

#### 2. 创建主题

cd /opt/bitnami/kafka/

**bash**

```bash
bin/kafka-topics.sh --bootstrap-server localhost:9092 --create --topic test_topic --partitions 3 --replication-factor 1
```

参数解释：

* `--create`：表明要创建一个新的主题。
* `--topic`：指定新主题的名称。
* `--partitions`：设置主题的分区数量。
* `--replication-factor`：设置每个分区的副本数量。

#### 3. 描述主题详情

**bash**

```bash
bin/kafka-topics.sh --bootstrap-server localhost:9092 --describe --topic test_topic
```

该命令会输出指定主题的详细信息，如分区数、副本因子、每个分区的领导者和副本信息等。

#### 4. 删除主题

**bash**

```bash
bin/kafka-topics.sh --bootstrap-server localhost:9092 --delete --topic test_topic
```

使用 `--delete` 参数可以删除指定的主题，但需要确保 `server.properties` 中 `delete.topic.enable=true`。

#### 5. 修改主题配置

**bash**

```bash
bin/kafka-topics.sh --bootstrap-server localhost:9092 --alter --topic test_topic --config retention.ms=3600000
```

`--alter` 用于修改主题的配置，这里将 `test_topic` 的消息保留时间设置为 1 小时（3600000 毫秒）。

#### 6.查看主题配置

```plain
bin/kafka-configs.sh \
  --bootstrap-server localhost:9092 \
  --entity-type topics \
  --entity-name tiqmo-svrlog \
  --describe
```

### 生产者（Producer）相关操作

#### 发送消息到主题

**bash**

```bash
bin/kafka-console-producer.sh --bootstrap-server localhost:9092 --topic test_topic
```

运行此命令后，你可以在控制台输入消息，按回车键即可将消息发送到指定主题。

### 消费者（Consumer）相关操作

#### 从主题消费消息

**bash**

```bash
bin/kafka-console-consumer.sh --bootstrap-server localhost:9092 --topic test_topic --from-beginning
```

参数解释：

* `--from-beginning`：表示从主题的最早消息开始消费。如果不指定该参数，将从当前最新的消息开始消费。

#### 查看消费者组信息

**bash**

```bash
bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list
```

此命令用于列出所有的消费者组。

#### 描述消费者组详情

**bash**

```bash
bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --describe --group test_group
```

该命令会输出指定消费者组的详细信息，如每个分区的消费偏移量等。

### 其他操作

#### 检查 Kafka 集群健康状态

**bash**

```bash
bin/kafka-topics.sh --bootstrap-server localhost:9092 --describe --topics-with-overrides
```

通过查看主题的详细信息，可以间接了解集群的健康状态。

#### 重置消费者组偏移量

**bash**

```bash
bin/kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group test_group --topic test_topic --reset-offsets --to-earliest --execute
```

此命令将 `test_group` 消费者组在 `test_topic` 主题上的消费偏移量重置到最早的消息位置。


> 更新: 2025-12-30 09:59:45  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/yeivlsl0wm100vcv>
# ELK / Elastic APM 日志采集优化建议

## 1. 当前现状

当前 `traces-apm-default` 数据量较大：

- 7 天 APM traces 数据约 `6.9TB`
- Data stream：`traces-apm-default`
- 当前副本策略：`1 primary + 1 replica`
- 当前 APM traces backing index 单个索引约 `80GB ~ 90GB`
- 估算单个 primary shard 约 `40GB ~ 45GB`
- Elasticsearch 集群为 3 个 data node

从 24 小时 transaction 统计看，APM 数据主要集中在少数高流量服务。

---

## 2. 24 小时 Top 服务统计

| 排名 | 服务名 | 24小时 transaction 数 | 约 QPS |
|---:|---|---:|---:|
| 1 | `wallyt-cms-service` | 42,535,649 | 492/s |
| 2 | `wallyt-intf-web` | 23,841,537 | 276/s |
| 3 | `market-base-service` | 22,811,513 | 264/s |
| 4 | `wallyt-intf-service` | 21,782,207 | 252/s |
| 5 | `wallyt-tms-service` | 17,217,140 | 199/s |
| 6 | `wallyt-mch-service` | 9,236,045 | 107/s |
| 7 | `wallyt-oms-online` | 8,611,445 | 100/s |
| 8 | `aia-cms-service` | 6,230,027 | 72/s |
| 9 | `aia-acs-service` | 5,788,715 | 67/s |
| 10 | `market-api-service` | 5,364,203 | 62/s |

前 5 个服务合计约：

```text
128,188,046 transactions / day
```

这几个服务是 APM traces 爆量的主要来源，应优先优化。

---

## 3. 优化目标

优化目标分为三类：

1. **降低 APM traces 写入量**
   - 调整采样率
   - 忽略健康检查、metrics、prometheus 等无价值请求
   - 限制单个 transaction 的 span 数量

2. **降低 Elasticsearch 存储成本**
   - APM traces 历史索引副本改为 `0`
   - 未来新建索引默认副本为 `0`
   - 启用 `best_compression`

3. **保持排障能力**
   - 核心服务保留较高采样率
   - 高 QPS 网关/接口服务降低采样率
   - 错误、慢请求后续可通过 Tail-based Sampling 精细化保留

---

## 4. 推荐采集策略

### 4.1 全局默认策略

适用于普通服务：

```text
transaction_sample_rate = 0.1
transaction_ignore_urls = /actuator/*,/health,/healthz,/ready,/readiness,/liveness,/metrics,/prometheus,/favicon.ico
capture_body = off
span_stack_trace_min_duration = -1ms
stack_trace_limit = 20
transaction_max_spans = 100
```

说明：

| 参数 | 建议值 | 作用 |
|---|---:|---|
| `transaction_sample_rate` | `0.1` | transaction 采样率 10% |
| `transaction_ignore_urls` | 见上方 | 忽略健康检查、metrics、prometheus 等无价值请求 |
| `capture_body` | `off` | 不采集请求 body，降低容量和敏感信息风险 |
| `span_stack_trace_min_duration` | `-1ms` | 关闭 span 堆栈采集 |
| `stack_trace_limit` | `20` | 限制堆栈深度 |
| `transaction_max_spans` | `100` | 限制单个 transaction 最大 span 数 |

---

### 4.2 高流量服务单独策略

建议对前 5 个服务分别创建 Agent Configuration：

| 服务名 | 建议采样率 |
|---|---:|
| `wallyt-cms-service` | `0.05` |
| `wallyt-intf-web` | `0.02 ~ 0.05` |
| `market-base-service` | `0.05` |
| `wallyt-intf-service` | `0.05` |
| `wallyt-tms-service` | `0.05` |

每个服务建议配置：

```text
transaction_sample_rate = 0.05
transaction_ignore_urls = /actuator/*,/health,/healthz,/ready,/readiness,/liveness,/metrics,/prometheus,/favicon.ico
capture_body = off
span_stack_trace_min_duration = -1ms
stack_trace_limit = 20
transaction_max_spans = 100
```

如果 `wallyt-intf-web` 属于网关、高 QPS Web 层，可以直接设置：

```text
transaction_sample_rate = 0.02
```

---

## 5. 配置位置

这些参数应该配置在 **APM Agent 侧**，不是 Kibana 的 `APM -> Settings -> General settings` 页面。

优先推荐配置位置：

```text
Kibana -> Observability/APM -> Settings -> Agent Configuration
```

然后点击：

```text
Create configuration
```

---

## 6. 在 Kibana Agent Configuration 中配置

### 6.1 创建全局默认配置

路径：

```text
APM -> Settings -> Agent Configuration -> Create configuration
```

配置范围：

```text
Service name: 留空 / All services
Environment: production 或留空
```

如果服务没有上报 `service.environment`，建议 Environment 先留空。

配置项：

```text
transaction_sample_rate = 0.1
transaction_ignore_urls = /actuator/*,/health,/healthz,/ready,/readiness,/liveness,/metrics,/prometheus,/favicon.ico
capture_body = off
span_stack_trace_min_duration = -1ms
stack_trace_limit = 20
transaction_max_spans = 100
```

---

### 6.2 创建高流量服务单独配置

例如 `wallyt-cms-service`：

```text
Service name: wallyt-cms-service
Environment: production 或留空
```

配置项：

```text
transaction_sample_rate = 0.05
transaction_ignore_urls = /actuator/*,/health,/healthz,/ready,/readiness,/liveness,/metrics,/prometheus,/favicon.ico
capture_body = off
span_stack_trace_min_duration = -1ms
stack_trace_limit = 20
transaction_max_spans = 100
```

其他高流量服务同理：

```text
wallyt-intf-web
market-base-service
wallyt-intf-service
wallyt-tms-service
```

---

## 7. Java Agent 本地配置方式

如果 Kibana Agent Configuration 不生效，可以改服务启动配置。

### 7.1 环境变量方式

适用于 Docker / Kubernetes：

```bash
ELASTIC_APM_TRANSACTION_SAMPLE_RATE=0.1
ELASTIC_APM_TRANSACTION_IGNORE_URLS=/actuator/*,/health,/healthz,/ready,/readiness,/liveness,/metrics,/prometheus,/favicon.ico
ELASTIC_APM_CAPTURE_BODY=off
ELASTIC_APM_SPAN_STACK_TRACE_MIN_DURATION=-1ms
ELASTIC_APM_STACK_TRACE_LIMIT=20
ELASTIC_APM_TRANSACTION_MAX_SPANS=100
```

Kubernetes Deployment 示例：

```yaml
env:
  - name: ELASTIC_APM_TRANSACTION_SAMPLE_RATE
    value: "0.1"
  - name: ELASTIC_APM_TRANSACTION_IGNORE_URLS
    value: "/actuator/*,/health,/healthz,/ready,/readiness,/liveness,/metrics,/prometheus,/favicon.ico"
  - name: ELASTIC_APM_CAPTURE_BODY
    value: "off"
  - name: ELASTIC_APM_SPAN_STACK_TRACE_MIN_DURATION
    value: "-1ms"
  - name: ELASTIC_APM_STACK_TRACE_LIMIT
    value: "20"
  - name: ELASTIC_APM_TRANSACTION_MAX_SPANS
    value: "100"
```

高流量服务可单独降低采样率：

```yaml
- name: ELASTIC_APM_TRANSACTION_SAMPLE_RATE
  value: "0.05"
```

网关类服务可进一步降低：

```yaml
- name: ELASTIC_APM_TRANSACTION_SAMPLE_RATE
  value: "0.02"
```

---

### 7.2 JVM 参数方式

```bash
java \
  -javaagent:/path/to/elastic-apm-agent.jar \
  -Delastic.apm.transaction_sample_rate=0.1 \
  -Delastic.apm.transaction_ignore_urls=/actuator/*,/health,/healthz,/ready,/readiness,/liveness,/metrics,/prometheus,/favicon.ico \
  -Delastic.apm.capture_body=off \
  -Delastic.apm.span_stack_trace_min_duration=-1ms \
  -Delastic.apm.stack_trace_limit=20 \
  -Delastic.apm.transaction_max_spans=100 \
  -jar app.jar
```

---

### 7.3 `elasticapm.properties` 方式

```properties
transaction_sample_rate=0.1
transaction_ignore_urls=/actuator/*,/health,/healthz,/ready,/readiness,/liveness,/metrics,/prometheus,/favicon.ico
capture_body=off
span_stack_trace_min_duration=-1ms
stack_trace_limit=20
transaction_max_spans=100
```

或使用完整前缀：

```properties
elastic.apm.transaction_sample_rate=0.1
elastic.apm.transaction_ignore_urls=/actuator/*,/health,/healthz,/ready,/readiness,/liveness,/metrics,/prometheus,/favicon.ico
elastic.apm.capture_body=off
elastic.apm.span_stack_trace_min_duration=-1ms
elastic.apm.stack_trace_limit=20
elastic.apm.transaction_max_spans=100
```

---

## 8. Elasticsearch 存储侧优化

### 8.1 现有 APM traces 索引副本改为 0

适用于当前已有 backing indices：

```http
PUT /.ds-traces-apm-default-*/_settings
{
  "index": {
    "number_of_replicas": 0
  }
}
```

作用：

- 取消 APM traces 副本恢复压力
- 降低磁盘占用
- 理论上可把 `6.9TB` 降至约 `3.4TB`

风险：

- APM traces 暂时无副本保护
- 如果节点损坏，对应 primary shard 数据存在丢失风险

---

### 8.2 未来 APM traces 索引默认副本 0 + best compression

当前模板中已经包含：

```text
traces-apm@custom
```

且当前 `traces-apm@custom` 为空，可以更新：

```http
PUT _component_template/traces-apm@custom
{
  "template": {
    "settings": {
      "index.number_of_replicas": 0,
      "index.codec": "best_compression"
    }
  },
  "_meta": {
    "package": {
      "name": "apm"
    },
    "managed_by": "fleet",
    "managed": true,
    "description": "Custom settings for APM traces: no replicas and best compression"
  }
}
```

说明：

- 不直接修改 Fleet managed template
- 使用官方预留的 `traces-apm@custom`
- 只影响未来新建的 backing index

---

### 8.3 手动 rollover 让新配置尽快生效

```http
POST /traces-apm-default/_rollover
```

如果普通 rollover 未触发，可按需强制 rollover：

```http
POST /traces-apm-default/_rollover
{
  "conditions": {}
}
```

---

## 9. 验证命令

### 9.1 查看集群健康

```http
GET _cluster/health?pretty
```

重点关注：

```json
"status"
"unassigned_shards"
"initializing_shards"
"relocating_shards"
```

---

### 9.2 查看恢复任务

```http
GET _cat/recovery?v&active_only=true&s=time:desc&h=index,shard,time,stage,source_node,target_node,bytes_percent,translog_ops,translog_ops_recovered,translog_ops_percent
```

没有输出表示当前没有活跃恢复任务。

---

### 9.3 查看 APM traces 索引大小

```http
GET _cat/indices/.ds-traces-apm-default-*?v&s=store.size:desc&h=index,pri,rep,docs.count,pri.store.size,store.size
```

副本为 `0` 后，理论上：

```text
store.size ≈ pri.store.size
```

副本为 `1` 时通常是：

```text
store.size ≈ pri.store.size * 2
```

---

### 9.4 查看最近 24 小时 Top 服务

```http
GET traces-apm-default/_search
{
  "size": 0,
  "query": {
    "bool": {
      "filter": [
        {
          "range": {
            "@timestamp": {
              "gte": "now-24h"
            }
          }
        },
        {
          "term": {
            "processor.event": "transaction"
          }
        }
      ]
    }
  },
  "aggs": {
    "top_services": {
      "terms": {
        "field": "service.name",
        "size": 20
      }
    }
  }
}
```

---

### 9.5 查看某个服务 Top Transaction

将 `your-service-name` 替换为实际服务名：

```http
GET traces-apm-default/_search
{
  "size": 0,
  "query": {
    "bool": {
      "filter": [
        {
          "range": {
            "@timestamp": {
              "gte": "now-24h"
            }
          }
        },
        {
          "term": {
            "processor.event": "transaction"
          }
        },
        {
          "term": {
            "service.name": "your-service-name"
          }
        }
      ]
    }
  },
  "aggs": {
    "top_transactions": {
      "terms": {
        "field": "transaction.name",
        "size": 30
      }
    }
  }
}
```

重点查找：

```text
/actuator/health
/actuator/prometheus
/health
/metrics
/prometheus
/favicon.ico
定时轮询接口
内部心跳接口
高频查询接口
```

---

### 9.6 查看最近 1 小时服务 transaction 数

配置变更后观察是否下降：

```http
GET traces-apm-default/_search
{
  "size": 0,
  "query": {
    "bool": {
      "filter": [
        {
          "range": {
            "@timestamp": {
              "gte": "now-1h"
            }
          }
        },
        {
          "term": {
            "processor.event": "transaction"
          }
        }
      ]
    }
  },
  "aggs": {
    "by_service": {
      "terms": {
        "field": "service.name",
        "size": 20
      }
    }
  }
}
```

---

### 9.7 查看 Span 是否爆量

```http
GET traces-apm-default/_search
{
  "size": 0,
  "query": {
    "bool": {
      "filter": [
        {
          "range": {
            "@timestamp": {
              "gte": "now-24h"
            }
          }
        },
        {
          "term": {
            "processor.event": "span"
          }
        }
      ]
    }
  },
  "aggs": {
    "top_services": {
      "terms": {
        "field": "service.name",
        "size": 20
      }
    }
  }
}
```

如果 span 也集中在高流量服务，`transaction_max_spans = 100` 很有必要。

---

## 10. 预估优化效果

当前 top 20 加其他服务约：

```text
1.81 亿 transactions / day
```

如果执行：

- 前 5 个服务采样率降到 `5%`
- 其他服务默认采样率降到 `10%`

粗略估算：

```text
前5：1.28亿 * 5% = 640万 / day
其他：约5310万 * 10% = 531万 / day
合计：约1170万 / day
```

总体下降约：

```text
93%+
```

如果当前 7 天 traces 为 `6.9TB`，长期可能降至：

```text
6.9TB * 6.5% ≈ 450GB
```

如果再把副本从 `1` 改为 `0`，长期可能进一步降至：

```text
200GB ~ 300GB 级别
```

实际效果会受 span 数、异常量、字段大小、服务流量变化影响。

---

## 11. 推荐落地顺序

### 第一阶段：立即止血

1. 现有 APM traces 副本改为 `0`
2. `traces-apm@custom` 设置未来副本 `0` + `best_compression`
3. 对前 5 个高流量服务单独设置采样率 `0.05`
4. 全局默认采样率设置为 `0.1`
5. 统一忽略 health / metrics / prometheus / actuator

---

### 第二阶段：观察与微调

1. 观察最近 1 小时 transaction 数是否下降
2. 查前 5 个服务 Top Transaction
3. 如果仍然过高，将网关/高频接口服务降到 `0.02`
4. 如果是非核心服务，可进一步降到 `0.01`
5. 核心交易类服务建议保持 `0.1 ~ 0.2`

---

### 第三阶段：长期治理

1. 确认 ILM 7 天删除策略真实生效
2. 定期检查 top services / top transactions
3. 如版本和架构支持，启用 Tail-based Sampling
4. 错误和慢请求 100% 保留，正常请求低采样
5. 对高基数字段、无价值 labels/tags 做治理

---

## 12. 注意事项

1. `transaction_sample_rate` 改小后，正常请求样本会减少，但错误和异常仍需要通过策略保留。
2. 如果使用 Kibana Agent Configuration，需确认 Agent 支持并启用了 central config。
3. `Service name` 必须和 APM 上报的 `service.name` 完全一致。
4. `Environment` 必须和服务上报的 `service.environment` 匹配；不确定时可先留空。
5. `number_of_replicas = 0` 会降低存储和恢复压力，但会减少数据冗余保护。
6. `best_compression` 对未来新 segment 更有效，历史数据不会立刻全部重新压缩。
7. 修改 Agent 配置后建议观察至少 1 小时，再判断效果。

# ELK 日志延迟优化策略

先看数据，ES 才是瓶颈，不是 Logstash：                                                                                                                                                                                                                                                                                     

  ┌─────────────────┬─────────────────────┬─────────────────┐                                                                                                                                                                                                                                                                  │      容器       │         CPU         │      内存       │

  ├─────────────────┼─────────────────────┼─────────────────┤

  │ elasticsearch02 │ 1221% (占满 ~12 核) │ 62.79% (29.4GB) │

  ├─────────────────┼─────────────────────┼─────────────────┤

  │ logstash        │ 389%                │ 13.67%          │

  ├─────────────────┼─────────────────────┼─────────────────┤

  │ kafka           │ 47%                 │ 3.09%           │

  └─────────────────┴─────────────────────┴─────────────────┘



  Logstash 25 个 worker 在疯狂往一个已经过载的 ES 打 bulk 请求，ES 处理不过来 → 索引延迟 → 日志展示延迟。



  ---

  Logstash Pipeline 调整



  核心思路：减少并发压力，增大单批效率



  # logstash.yml 或 pipelines.yml

  pipeline.workers: 8          # 从 25 降到 8，减少对 ES 的并发冲击

  pipeline.batch.size: 2000    # 从 100 提升到 2000，减少 bulk 请求次数

  pipeline.batch.delay: 50     # ms，适当等待凑批



  为什么反向操作？workers 少 → ES 并发 bulk 请求少 → ES 线程池不堆积；batch 大 → 每次 bulk 更高效，HTTP 开销摊薄。



  ---

  ES 侧调整（更关键）



  1. 降低 refresh 频率（最有效）

  curl -X PUT "localhost:9200/_settings" -H 'Content-Type: application/json' -d'

  {

    "index": {

      "refresh_interval": "30s"

    }

  }'

  默认 1s refresh 会频繁触发 segment merge，是 CPU 飙高的主因。



  2. 单节点关掉副本

  curl -X PUT "localhost:9200/_settings" -H 'Content-Type: application/json' -d'

  {

    "index": {

      "number_of_replicas": 0

    }

  }'



  3. 检查 JVM Heap 设置



  ES 当前用了 29.4GB，如果 heap 设置超过 31GB 会关闭 compressed oops，GC 压力剧增。建议：

  # jvm.options

  -Xms24g

  -Xmx24g

  24GB = 总内存的一半，且在 31GB 安全线以下。



  4. 检查 shard 数量

  curl "localhost:9200/_cat/shards?v&h=index,shard,state,docs,store" | head -30

  shard 过多（每个 shard 都要 refresh）也会放大 CPU 消耗。



  ---

  优先级



  1. 先改 refresh_interval 到 30s — 立竿见影，CPU 会明显下降

  2. 调 Logstash workers 到 8，batch.size 到 2000

  3. 确认 JVM heap ≤ 24g

  4. 观察 ES CPU 降到合理水位（< 400%）后，再根据延迟情况微调 batch.size



✻ Sautéed for 37s



> 更新: 2026-02-27 09:12:56  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/trrkds17osf49ddy>
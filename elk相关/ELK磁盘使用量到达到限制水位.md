# ELK磁盘使用量到达到限制水位

报错：<font style="color:#DF2A3F;"> [2026-04-28T00:55:33.504+00:00][ERROR][plugins.taskManager] Error updating task delete_inactive_background_task_nodes:task during claim: {"type":"cluster_block_exception","reason":"index [.kibana_task_manager_8.7.1_001] blocked by: [TOO_MANY_REQUESTS/12/disk usage exceeded flood-stage watermark, index has read-only-allow-delete block; for more information, see </font>[<font style="color:#DF2A3F;">https://www.elastic.co/guide/en/elasticsearch/reference/8.19/fix-watermark-errors.html];"}</font>](https://www.elastic.co/guide/en/elasticsearch/reference/8.19/fix-watermark-errors.html];"})

<font style="color:#DF2A3F;">[2026-04-28T00:55:33.504+00:00][ERROR][plugins.taskManager] Error updating task Fleet-Metrics-Task:1.1.1:task during claim: {"type":"cluster_block_exception","reason":"index [.kibana_task_manager_8.7.1_001] blocked by: [TOO_MANY_REQUESTS/12/disk usage exceeded flood-stage watermark, index has read-only-allow-delete block; for more information, see </font>[<font style="color:#DF2A3F;">https://www.elastic.co/guide/en/elasticsearch/reference/8.19/fix-watermark-errors.html];"}</font>](https://www.elastic.co/guide/en/elasticsearch/reference/8.19/fix-watermark-errors.html];"})

<font style="color:#DF2A3F;">[2026-04-28T00:55:33.504+00:00][ERROR][plugins.taskManager] Error updating task Fleet-Usage-Logger-Task:task during claim: {"type":"cluster_block_exception","reason":"index [.kibana_task_manager_8.7.1_001] blocked by: [TOO_MANY_REQUESTS/12/disk usage exceeded flood-stage watermark, index has read-only-allow-delete block; for more information, see </font>[<font style="color:#DF2A3F;">https://www.elastic.co/guide/en/elasticsearch/reference/8.19/fix-watermark-errors.html];"}</font>](https://www.elastic.co/guide/en/elasticsearch/reference/8.19/fix-watermark-errors.html];"})

<font style="color:#DF2A3F;">[2026-04-28T00:55:33.505+00:00][ERROR][plugins.taskManager] Error updating task fleet:automatic-agent-upgrade-task:1.0.0:task during claim: {"type":"cluster_block_exception","reason":"index [.kibana_task_manager_8.7.1_001] blocked by: [TOO_MANY_REQUESTS/12/disk usage exceeded flood-stage watermark, index has read-only-allow-delete block; for more information, see </font>[<font style="color:#DF2A3F;">https://www.elastic.co/guide/en/elasticsearch/reference/8.19/fix-watermark-errors.html];"}</font>](https://www.elastic.co/guide/en/elasticsearch/reference/8.19/fix-watermark-errors.html];"})

<font style="color:#DF2A3F;">[2026-04-28T00:55:39.401+00:00][ERROR][plugins.taskManager] Kibana Discovery Service couldn't update this node's last_seen timestamp. id: 2ffd1569-4220-49e4-a251-c6c0ff6836b3, last_seen: 2026-04-28T00:55:39.374Z, error:index [.kibana_task_manager_8.7.1_001] blocked by: [TOO_MANY_REQUESTS/12/disk usage exceeded flood-stage watermark, index has read-only-allow-delete block; for more information, see </font>[<font style="color:#DF2A3F;">https://www.elastic.co/guide/en/elasticsearch/reference/8.19/fix-watermark-errors.html];:</font>](https://www.elastic.co/guide/en/elasticsearch/reference/8.19/fix-watermark-errors.html];:)<font style="color:#DF2A3F;"> cluster_block_exception</font>

<font style="color:#DF2A3F;">        Root causes:</font>

<font style="color:#DF2A3F;">                cluster_block_exception: index [.kibana_task_manager_8.7.1_001] blocked by: [TOO_MANY_REQUESTS/12/disk usage exceeded flood-stage watermark, index has read-only-allow-delete block; for more information, see </font>[<font style="color:#DF2A3F;">https://www.elastic.co/guide/en/elasticsearc</font>](https://www.elastic.co/guide/en/elasticsearc)





# 查看索引使用量（从大到小排序）
 curl -u elastic:xg+kZxZ_sFFK76pvDgz0 "[http://localhost:9200/_cat/indices?v&s=store.size:desc"](http://localhost:9200/_cat/indices?v&s=store.size:desc")



# 删除用量大的旧索引
 curl -u elastic:'xg+kZxZ_sFFK76pvDgz0' -X DELETE "[http://localhost:9200/.ds-logs-svrlog-wallet-2025.12.29-000001,.ds-logs-svrlog-account-2025.12.29-000001,.ds-logs-svrlog-wallet-pre2-2025.12.29-000001,.ds-logs-svrlog-acquiring-2025.12.29-000001,.ds-logs-svrlog-account-pre2-2025.12.29-000001,.ds-logs-svrlog-acquiring-pre2-2025.12.29-000001?ignore_unavailable=true&pretty"](http://localhost:9200/.ds-logs-svrlog-wallet-2025.12.29-000001,.ds-logs-svrlog-account-2025.12.29-000001,.ds-logs-svrlog-wallet-pre2-2025.12.29-000001,.ds-logs-svrlog-acquiring-2025.12.29-000001,.ds-logs-svrlog-account-pre2-2025.12.29-000001,.ds-logs-svrlog-acquiring-pre2-2025.12.29-000001?ignore_unavailable=true&pretty")

curl -u elastic:xg+kZxZ_sFFK76pvDgz0 -X PUT "[http://localhost:9200/_all/_settings?pretty"](http://localhost:9200/_all/_settings?pretty") -H "Content-Type: application/json" -d '{

  "index.blocks.read_only_allow_delete": null

}'

{

  "acknowledged" : true

}





> 更新: 2026-04-28 09:12:05  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/gttpa279n2wkczb3>
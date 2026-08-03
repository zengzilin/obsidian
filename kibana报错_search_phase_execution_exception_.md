# kibana 报错"search_phase_execution_exception"

search\_phase\_execution\_exception: Search rejected due to missing shards \[\[.kibana\_task\_manager\_8.7.0\_001]\[0]]. Consider using `allow_partial_search_results` setting to bypass this error.'. Retrying attempt 2 in 4 seconds. \[2025-05-06T02:09:24.115+00:00]\[INFO ]\[savedobjects-service] \[.kibana\_task\_manager] OUTDATED\_DOCUMENTS\_SEARCH\_OPEN\_PIT -> OUTDATED\_DOCUMENTS\_SEARCH\_OPEN\_PIT. took: 2008ms.

# 解决方案：

参考文章

<https://blog.csdn.net/chaogaoxiaojifantong/article/details/122569432>

curl -u elastic:changeme -X GET "localhost:9200/.kibana\_task\_manager\_8.7.0\_001/\_settings" 命令删除报没有权限。

# 需要用内置用户kibana\_system删除

curl -u kibana\_system:changeme -X DELETE "localhost:9200/.kibana\_task\_manager\_8.7.0\_001"

<font style="color:rgba(0, 0, 0, 0.85);">curl -u kibana\_system:changeme -X DELETE "</font>[<font style="color:rgba(0, 0, 0, 0.85) !important;">localhost:9200/.kibana\_task\_manager\_8.7.0\_001</font>](https://localhost:9200/.kibana_task_manager_8.7.0_001)<font style="color:rgba(0, 0, 0, 0.85);">" 执行这个命令之后报错 Response: { error: { root\_cause: \[ { type: 'no\_shard\_available\_action\_exception', reason: null } ], type: 'search\_phase\_execution\_exception', reason: 'all shards failed', phase: 'query', grouped: true, failed\_shards: \[ { shard: 0, index: '.ds-logs-apm.error-default-2025.04.12-000006', node: null, reason: { type: 'no\_shard\_available\_action\_exception', reason: null } } ] }, status: 503 }</font>


> 更新: 2025-05-06 10:49:15  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/fysvw3twiaxg7b7l>
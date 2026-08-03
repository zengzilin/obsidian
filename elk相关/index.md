# elk相关

<font style="color:rgb(255, 255, 255);background-color:rgb(45, 101, 247);">kibana报错“”[2024-04-25T01:42:05.452+00:00][ERROR][plugins.taskManager] Failed to poll for work: [parent] Data too large, data for [<http_request>] would be [2043954130/1.9gb], which is larger than the limit of [2040109465/1.8gb], real usage: [2043937352/1.9gb], new bytes reserved: [16778/16.3kb], usages [eql_sequence=0/0b, fielddata=381956/373kb, request=0/0b, inflight_requests=16778/16.3kb, model_inference=0/0b] “”</font>

<font style="color:rgb(255, 255, 255);background-color:rgb(45, 101, 247);"></font>

**<font style="color:rgb(6, 6, 7);">清理或减少缓存</font>**<font style="color:rgb(6, 6, 7);">：如果 fielddata 缓存占用了太多的内存，您可以尝试清理缓存。使用如下的 cURL 命令可以清理 fielddata 缓存：</font>

<font style="color:rgb(6, 6, 7);">curl -u elastic:changeme_tiqmo -X POST '</font>[<font style="color:rgb(6, 6, 7);">http://localhost:9200/_cache/clear?fielddata=true'</font>](http://localhost:9200/_cache/clear?fielddata=true')

<font style="color:rgb(6, 6, 7);">清理缓存之后，kibana正常登录</font>

<font style="color:rgb(6, 6, 7);"></font>

<font style="color:rgb(255, 255, 255);background-color:rgb(45, 101, 247);"></font>



> 更新: 2024-04-25 10:18:53  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/ro3hpy83iv4hvbe2>
# apm报错 索引文档数量过多

{"log.level":"error","@timestamp":"2025-05-08T05:32:48.376Z","message":"failed to index document (illegal_argument_exception): Number of documents in the index can't exceed [2147483519]","component":{"binary":"apm-server","dataset":"elastic_agent.apm_server","id":"apm-default","type":"apm"},"log":{"source":"apm-default"},"log.origin":{"file.line":279,"file.name":"go-docappender@v0.1.0/appender.go"},"service.name":"apm-server","ecs.version":"1.6.0","ecs.version":"1.6.0"}

{"log.level":"error","@timestamp":"2025-05-08T05:32:48.376Z","message":"failed to index document (illegal_argument_exception): Number of documents in the index can't exceed [2147483519]","component":{"binary":"apm-server","dataset":"elastic_agent.apm_server","id":"apm-default","type":"apm"},"log":{"source":"apm-default"},"log.origin":{"file.line":279,"file.name":"go-docappender@v0.1.0/appender.go"},"service.name":"apm-server","ecs.version":"1.6.0","ecs.version":"1.6.0"}

{"log.level":"error","@timestamp":"2025-05-08T05:32:48.376Z","message":"failed to index document (illegal_argument_exception): Number of documents in the index can't exceed [2147483519]","component":{"binary":"apm-server","dataset":"elastic_agent.apm_server","id":"apm-default","type":"apm"},"log":{"source":"apm-default"},"ecs.version":"1.6.0","log.origin":{"file.line":279,"file.name":"go-docappender@v0.1.0/appender.go"},"service.name":"apm-server","ecs.version":"1.6.0"}

{"log.level":"error","@timestamp":"2025-05-08T05:32:48.376Z","message":"failed to index document (illegal_argument_exception): Number of documents in the index can't exceed [2147483519]","component":{"binary":"apm-server","dataset":"elastic_agent.apm_server","id":"apm-default","type":"apm"},"log":{"source":"apm-default"},"service.name":"apm-server","ecs.version":"1.6.0","log.origin":{"file.line":279,"file.name":"go-docappender@v0.1.0/appender.go"},"ecs.version":"1.6.0"}

{"log.level":"error","@timestamp":"2025-05-08T05:32:48.376Z","message":"failed to index document (illegal_argument_exception): Number of documents in the index can't exceed [2147483519]","component":{"binary":"apm-server","dataset":"elastic_agent.apm_server","id":"apm-default","type":"apm"},"log":{"source":"apm-default"},"ecs.version":"1.6.0","log.origin":{"file.line":279,"file.name":"go-docappender@v0.1.0/appender.go"},"service.name":"apm-server","ecs.version":"1.6.0"}

{"log.level":"error","@timestamp":"2025-05-08T05:32:48.376Z","message":"failed to index document (illegal_argument_exception): Number of documents in the index can't exceed [2147483519]","component":{"binary":"apm-server","dataset":"elastic_agent.apm_server","id":"apm-default","type":"apm"},"log":{"source":"apm-default"},"log.origin":{"file.line":279,"file.name":"go-docappender@v0.1.0/appender.go"},"service.name":"apm-server","ecs.version":"1.6.0","ecs.version":"1.6.0"}

{"log.level":"error","@timestamp":"2025-05-08T05:32:48.378Z","message":"failed to index document (illegal_argument_exception): Number of documents in the index can't exceed [2147483519]","component":{"binary":"apm-server","dataset":"elastic_agent.apm_server","id":"apm-default","type":"apm"},"log":{"source":"apm-default"},"log.origin":{"file.line":279,"file.name":"go-docappender@v0.1.0/appender.go"},"service.name":"apm-server","ecs.version":"1.6.0","ecs.version":"1.6.0"}

{"log.level":"error","@timestamp":"2025-05-08T05:32:48.378Z","message":"failed to index document (illegal_argument_exception): Number of documents in the index can't exceed [2147483519]","component":{"binary":"apm-server","dataset":"elastic_agent.apm_server","id":"apm-default","type":"apm"},"log":{"source":"apm-default"},"log.origin":{"file.line":279,"file.name":"go-docappender@v0.1.0/appender.go"},"service.name":"apm-server","ecs.version":"1.6.0","ecs.version":"1.6.0"}

{"log.level":"error","@timestamp":"2025-05-08T05:32:48.378Z","message":"failed to index document (illegal_argument_exception): Number of documents in the index can't exceed [2147483519]","component":{"binary":"apm-server","dataset":"elastic_agent.apm_server","id":"apm-default","type":"apm"},"log":{"source":"apm-default"},"ecs.version":"1.6.0","log.origin":{"file.line":279,"file.name":"go-docappender@v0.1.0/appender.go"},"service.name":"apm-server","ecs.version":"1.6.0"}

{"log.level":"error","@timestamp":"2025-05-08T05:32:48.378Z","message":"failed to index document (^C



apm相关的索引太大了，而且索引策略名字不对，自动清理没生效



解决方法，新建索引策略。重新关联。

# 1.找出较大的apm隐藏索引
![1746694108160-143bbf8c-4b74-47c8-b6ed-4c54a13402d3.png](./img/r7i8E1g0-1DB7i6F/1746694108160-143bbf8c-4b74-47c8-b6ed-4c54a13402d3-742945.png)

逐个点开查看

![1746694193612-48075d29-7d9b-4ea2-a593-65e8bb48ec2f.png](./img/r7i8E1g0-1DB7i6F/1746694193612-48075d29-7d9b-4ea2-a593-65e8bb48ec2f-478836.png)

比如下面这个报index lifecycle policy不存在，表明，这个索引没有清理策略，索引永远不会被清理，导致上述报错

![1746694235974-35990815-fa06-417c-ba75-770461d066cd.png](./img/r7i8E1g0-1DB7i6F/1746694235974-35990815-fa06-417c-ba75-770461d066cd-700643.png)

# 2.新建索引生命周期管理策略**<font style="color:#DF2A3F;">metrics-apm.service_transaction_interval_metrics-default_policy.1m</font>**
**<font style="color:#DF2A3F;"></font>**

**<font style="color:rgb(189, 39, 30);">Index lifecycle error</font>**

<font style="color:rgb(52, 55, 65);">illegal_argument_exception: policy [metrics-apm.service_transaction_interval_metrics-default_policy.1m] does not exist</font>

**<font style="color:#DF2A3F;">metrics-apm.service_transaction_interval_metrics-default_policy.1m</font>**

<font style="color:rgb(52, 55, 65);background-color:rgb(248, 233, 233);">修改现有的，改名字就会另存为一个新的</font>

![1746694859344-5aad3e31-565b-4994-8c0e-70d9f1ed9314.png](./img/r7i8E1g0-1DB7i6F/1746694859344-5aad3e31-565b-4994-8c0e-70d9f1ed9314-432363.png)

# <font style="color:rgb(52, 55, 65);background-color:#FFFFFF;">3.如果新建索引清理策略之后，还没有触发清理机制，可以手动触发</font>
![1746694767490-d140d058-8f49-4fa5-ba0e-83690ea57724.png](./img/r7i8E1g0-1DB7i6F/1746694767490-d140d058-8f49-4fa5-ba0e-83690ea57724-076540.png)



> 更新: 2025-05-08 17:02:28  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/nnyyw4g644gzagxs>
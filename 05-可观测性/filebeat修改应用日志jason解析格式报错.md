# filebeat修改 应用日志jason解析格式报错

{"log.level":"info","@timestamp":"2026-03-04T13:24:43.323+0300","log.origin":{"file.name":"instance/beat.go","file.line":496},"message":"filebeat stopped.","service.name":"filebeat","ecs.version":"1.6.0"}

<font style="color:#DF2A3F;">{"log.level":"error","@timestamp":"2026-03-04T13:24:43.323+0300","log.origin":{"file.name":"instance/beat.go","file.line":1142},"message":"Exiting: Failed to start crawler: starting input failed: error while initializing input: When using the JSON decoder and multiline together, you need to specify a message_key value accessing 'filebeat.inputs.0' (source:'filebeat.yml')","service.name":"filebeat","ecs.version":"1.6.0"}</font>

<font style="color:#DF2A3F;">Exiting: Failed to start crawler: starting input failed: error while initializing input: When using the JSON decoder and multiline together, you need to specify a message_key value accessing 'filebeat.inputs.0' (source:'filebeat.yml')</font>

<font style="color:#DF2A3F;"></font>

![1772620472055-fa60c1e0-0610-4670-9e6a-903d34665f4c.png](./img/JoIj7OWpjLbstnvV/1772620472055-fa60c1e0-0610-4670-9e6a-903d34665f4c-860373.png)



> 更新: 2026-03-04 18:35:35  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/flkfh76gyv893y3t>
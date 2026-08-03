# logstash内置字段介绍以及elk磁盘使用优化

# <font style="color:rgba(0, 0, 0, 0.9);">1. </font>**<font style="color:rgba(0, 0, 0, 0.9);">核心字段</font>**

* <code>**<font style="color:rgba(0, 0, 0, 0.9);">@timestamp</font>**</code><font style="color:rgba(0, 0, 0, 0.9);">\ </font><font style="color:rgba(0, 0, 0, 0.9);">事件被Logstash处理的时间戳，默认是Logstash接收事件的时间。用户可通过</font><code><font style="color:rgba(0, 0, 0, 0.9);">date</font></code><font style="color:rgba(0, 0, 0, 0.9);">插件覆盖此字段，例如从日志中提取时间作为实际时间</font>[<font style="color:rgb(22, 119, 255);">5</font>](https://www.lmlphp.com/user/79978/article/item/2633084/)[<font style="color:rgb(22, 119, 255);">7</font>](https://blog.51cto.com/u_16099329/7217615)<font style="color:rgba(0, 0, 0, 0.9);">。</font>
* <code>**<font style="color:rgba(0, 0, 0, 0.9);">@version</font>**</code><font style="color:rgba(0, 0, 0, 0.9);">\ </font><font style="color:rgba(0, 0, 0, 0.9);">事件的版本号，标识Logstash处理事件的格式版本，通常为固定值</font><code><font style="color:rgba(0, 0, 0, 0.9);">1</font></code><font style="color:rgba(0, 0, 0, 0.9);">。</font>
* <code>**<font style="color:rgba(0, 0, 0, 0.9);">host</font>**</code><font style="color:rgba(0, 0, 0, 0.9);">\ </font><font style="color:rgba(0, 0, 0, 0.9);">运行Logstash的主机信息，包含主机名、IP地址等。用户可通过</font><code><font style="color:rgba(0, 0, 0, 0.9);">mutate</font></code><font style="color:rgba(0, 0, 0, 0.9);">插件修改或补充此字段（如从日志路径提取IP）</font>[<font style="color:rgb(22, 119, 255);">1</font>](https://blog.csdn.net/xpsallwell/article/details/77198215)[<font style="color:rgb(22, 119, 255);">5</font>](https://www.lmlphp.com/user/79978/article/item/2633084/)<font style="color:rgba(0, 0, 0, 0.9);">。</font>
* <code>**<font style="color:rgba(0, 0, 0, 0.9);">message</font>**</code><font style="color:rgba(0, 0, 0, 0.9);">\ </font><font style="color:rgba(0, 0, 0, 0.9);">原始日志的完整内容。在过滤阶段可能被截断或修改，例如通过</font><code><font style="color:rgba(0, 0, 0, 0.9);">truncate</font></code><font style="color:rgba(0, 0, 0, 0.9);">插件限制长度</font>[<font style="color:rgb(22, 119, 255);">1</font>](https://blog.csdn.net/xpsallwell/article/details/77198215)

***

# <font style="color:rgba(0, 0, 0, 0.9);">2. </font>**<font style="color:rgba(0, 0, 0, 0.9);">元数据字段</font>**

* <code>**<font style="color:rgba(0, 0, 0, 0.9);">@metadata</font>**</code><font style="color:rgba(0, 0, 0, 0.9);">\ </font><font style="color:rgba(0, 0, 0, 0.9);">用于存储临时数据的特殊字段，内容不会输出到最终事件中，常用于条件判断或中间处理。例如，</font><code><font style="color:rgba(0, 0, 0, 0.9);">[@metadata][type]</font></code><font style="color:rgba(0, 0, 0, 0.9);">可辅助动态路由</font>[<font style="color:rgb(22, 119, 255);">2</font>](https://blog.csdn.net/smithallenyu/article/details/52181249)[<font style="color:rgb(22, 119, 255);">7</font>](https://blog.51cto.com/u_16099329/7217615)<font style="color:rgba(0, 0, 0, 0.9);">。</font>
* <code>**<font style="color:rgba(0, 0, 0, 0.9);">tags</font>**</code><font style="color:rgba(0, 0, 0, 0.9);">\ </font><font style="color:rgba(0, 0, 0, 0.9);">标记事件的数组字段，用于分类或标识处理状态（如解析失败时添加</font><code><font style="color:rgba(0, 0, 0, 0.9);">_grokparsefailure</font></code><font style="color:rgba(0, 0, 0, 0.9);">标签）。用户可通过条件语句动态添加或删除标签</font>[<font style="color:rgb(22, 119, 255);">1</font>](https://blog.csdn.net/xpsallwell/article/details/77198215)[<font style="color:rgb(22, 119, 255);">2</font>](https://blog.csdn.net/smithallenyu/article/details/52181249)<font style="color:rgba(0, 0, 0, 0.9);">。</font>
* <code>**<font style="color:rgba(0, 0, 0, 0.9);">type</font>**</code><font style="color:rgba(0, 0, 0, 0.9);">\ </font><font style="color:rgba(0, 0, 0, 0.9);">事件的类型标识（旧版本中常见），通常由用户自定义。例如在配置中通过</font><code><font style="color:rgba(0, 0, 0, 0.9);">[@metadata][type]</font></code><font style="color:rgba(0, 0, 0, 0.9);">设置类型为</font><code><font style="color:rgba(0, 0, 0, 0.9);">log</font></code>[<font style="color:rgb(22, 119, 255);">1</font>](https://blog.csdn.net/xpsallwell/article/details/77198215)<font style="color:rgba(0, 0, 0, 0.9);">。</font>

### <font style="color:rgba(0, 0, 0, 0.9);"> </font>

# <font style="color:rgba(0, 0, 0, 0.9);">3.pipeline</font>**<font style="color:rgba(0, 0, 0, 0.9);">扩展字段（动态生成）</font>**

* <code>**<font style="color:rgba(0, 0, 0, 0.9);">[log][file][path]</font>**</code><font style="color:rgba(0, 0, 0, 0.9);">\ </font><font style="color:rgba(0, 0, 0, 0.9);">日志文件路径，用户可通过</font><code><font style="color:rgba(0, 0, 0, 0.9);">grok</font></code><font style="color:rgba(0, 0, 0, 0.9);">插件解析路径并提取子字段（如应用名、环境等）</font>
* <code>**<font style="color:rgba(0, 0, 0, 0.9);">[event][original]</font>**</code><font style="color:rgba(0, 0, 0, 0.9);">\ </font><font style="color:rgba(0, 0, 0, 0.9);">原始事件的副本，用户可选择在最终输出中移除此字段以节省存储</font>
* <font style="color:rgba(0, 0, 0, 0.9);">举例：</font>

![1746771950550-8184786a-feea-4456-8929-05174d78e435.png](./img/UeMLIfWpjdU7YeAN/1746771950550-8184786a-feea-4456-8929-05174d78e435-736991.png)


> 更新: 2025-05-09 14:28:19  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/irb4dtuogfo31ys5>
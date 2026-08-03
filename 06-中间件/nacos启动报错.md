# nacos启动报错

# 1.故障一 NFS存储IO 错误导致nacos failure

解决方案，换成local-path存储

# 2.故障二 报数据库连接错误

:::info <font style="color:rgb(17, 17, 51);background-color:rgb(245, 247, 255);">ider.java:215) at com.mysql.cj.protocol.a.NativeProtocol.connect(NativeProtocol.java:1428) at com.mysql.cj.NativeSession.connect(NativeSession.java:133) at com.mysql.cj.jdbc.ConnectionImpl.connectWithRetries(ConnectionImpl.java:829) ... 136 common frames omitted</font><font style="color:#DF2A3F;background-color:rgb(245, 247, 255);"> Caused by: com.mysql.cj.exceptions.UnableToConnectException: Public Key Retrieval is not allowed at sun.reflect.NativeConstructorAccessorImpl.newInstance0(Native Method) at</font><font style="color:rgb(17, 17, 51);background-color:rgb(245, 247, 255);"> sun.reflect.NativeConstructorAccessorImpl.newInstance(NativeConstructorAccessorImpl.java:62) at sun.reflect.DelegatingConstructorAccessorImpl.newInstance(DelegatingConstructorAccessorImpl.java:45)</font>

:::

原因：<font style="color:rgb(17, 17, 51);">是 </font>**<font style="color:rgb(17, 17, 51);">MySQL 8.0+</font>**<font style="color:rgb(17, 17, 51);"> 使用 </font><code><font style="color:rgb(17, 17, 51);background-color:rgba(175, 184, 193, 0.2);">caching_sha2_password</font></code><font style="color:rgb(17, 17, 51);"> 认证插件时，客户端（这里是 Nacos）在连接数据库时未启用“允许公钥检索”（Public Key Retrieval）导致的。</font>

解决方案：修改连接参数 添加 <font style="color:#DF2A3F;">allowPublicKeyRetrieval=true</font>

```
  param: <font style="color:#DF2A3F;">characterEncoding=utf8&connectTimeout=1000&socketTimeout=3000&autoReconnect=true&useSSL=false&allowPublicKeyRetrieval=true</font>
```

NACOS\_AUTH\_ENABLE: true

NACOS\_AUTH\_IDENTITY\_KEY: nacos

NACOS\_AUTH\_IDENTITY\_VALUE: nacos

NACOS\_AUTH\_TOKEN: "Ym1GbmIzTWdhWE1nZG1WeWVTQm5iMjlrSUhOdlpuUjNZWEpsQ2c9PQo="

# 3.故障三，修复了前两个问题之后，日志没有报错，但是就是起不来

原因：nacos我启用了集群模式，但是我只设置了一个节点副本

![1764754603611-bd72358f-6bf1-42aa-adbd-878d662d5bdf.png](./img/jDuUSLs9_sPfcN3C/1764754603611-bd72358f-6bf1-42aa-adbd-878d662d5bdf-873075.png)

## <font style="color:rgb(17, 17, 51);">关键知识：</font>

* <font style="color:rgb(17, 17, 51);">Nacos 集群模式基于</font><font style="color:rgb(17, 17, 51);"> </font>**<font style="color:rgb(17, 17, 51);">JRaft</font>**<font style="color:rgb(17, 17, 51);"> </font><font style="color:rgb(17, 17, 51);">实现一致性协议。</font>
* **<font style="color:#DF2A3F;">Raft 要求多数派（quorum）存活才能提供服务</font>**<font style="color:#DF2A3F;">。</font>
* **<font style="color:rgb(17, 17, 51);">1 节点集群的 quorum = 1</font>**<font style="color:rgb(17, 17, 51);">，理论上可以工作。</font>
* **<font style="color:rgb(17, 17, 51);">但是</font>**<font style="color:rgb(17, 17, 51);">：Nacos 在</font><font style="color:rgb(17, 17, 51);"> </font>**<font style="color:rgb(17, 17, 51);">首次启动时</font>**<font style="color:rgb(17, 17, 51);">，如果发现</font><font style="color:rgb(17, 17, 51);"> </font><code><font style="color:rgb(17, 17, 51);background-color:rgba(175, 184, 193, 0.2);">member.list</font></code><font style="color:rgb(17, 17, 51);"> </font><font style="color:rgb(17, 17, 51);">只有自己，且</font><font style="color:rgb(17, 17, 51);"> </font>**<font style="color:rgb(17, 17, 51);">未配置</font>\*\*\*\*<font style="color:rgb(17, 17, 51);"> </font>**<code>**<font style="color:rgb(17, 17, 51);background-color:rgba(175, 184, 193, 0.2);">nacos.core.cluster.embedded.enabled=false</font>**</code><font style="color:rgb(17, 17, 51);">，它会尝试以</font><font style="color:rgb(17, 17, 51);"> </font>**<font style="color:rgb(17, 17, 51);">embedded 模式</font>**<font style="color:rgb(17, 17, 51);"> </font><font style="color:rgb(17, 17, 51);">启动 Raft，但可能因网络或初始化顺序问题卡住。</font>

<font style="color:rgb(17, 17, 51);">更重要的是：</font><font style="color:#DF2A3F;">Nacos 的 readiness 探针会检查 Raft 状态。如果 Raft 未就绪（比如还在等待其他节点），就会返回 500。</font>

## <font style="color:rgb(17, 17, 51);">✅</font><font style="color:rgb(17, 17, 51);"> 解决方案</font>

### <font style="color:rgb(17, 17, 51);">✅</font><font style="color:rgb(17, 17, 51);"> 方案一：【推荐】部署</font><font style="color:rgb(17, 17, 51);"> </font>**<font style="color:rgb(17, 17, 51);">3 节点集群</font>**<font style="color:rgb(17, 17, 51);">（生产标准）</font>

<font style="color:rgb(17, 17, 51);">修改 StatefulSet 的 </font><code><font style="color:rgb(17, 17, 51);background-color:rgba(175, 184, 193, 0.2);">replicas: 3</font></code><font style="color:rgb(17, 17, 51);">，并确保：</font>

* <code><font style="color:rgb(17, 17, 51);background-color:rgba(175, 184, 193, 0.2);">cluster.conf</font></code><font style="color:rgb(17, 17, 51);"> </font><font style="color:rgb(17, 17, 51);">或 peer-finder 能正确发现 3 个节点</font>
* <font style="color:rgb(17, 17, 51);">网络互通（端口 7848, 8848, 9848, 9849）</font>

<font style="color:rgb(17, 17, 51);">这是最稳定的方式。</font>

***

### <font style="color:rgb(17, 17, 51);">✅</font><font style="color:rgb(17, 17, 51);"> 方案二：</font>**<font style="color:rgb(17, 17, 51);">强制单节点以 standalone 模式运行</font>**<font style="color:rgb(17, 17, 51);">（测试/开发环境）</font>

<font style="color:rgb(17, 17, 51);">虽然你设置了 </font><code><font style="color:rgb(17, 17, 51);background-color:rgba(175, 184, 193, 0.2);">cluster mode</font></code><font style="color:rgb(17, 17, 51);">，但如果只起 1 个 Pod，</font>**<font style="color:rgb(17, 17, 51);">应该用 standalone 模式</font>**<font style="color:rgb(17, 17, 51);">。</font>


> 更新: 2025-12-03 17:40:29  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/subcilqpn6u088v1>
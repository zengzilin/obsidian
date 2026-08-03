# Nacos集群有个节点的配置时间不一致

<font style="color:rgb(6, 10, 38);background-color:rgb(235, 245, 255);">Nacos 集群有节点的配置同步时间，慢了20分钟。</font>

# <font style="color:rgb(6, 10, 38);background-color:rgb(235, 245, 255);">1.进入有问题的节点nacos-2</font>

<font style="color:rgb(6, 10, 38);background-color:rgb(235, 245, 255);">kubectl  -n uat-ksa2-middleware exec -it nacos-2 -- /bin/bash</font>

<font style="color:rgb(6, 10, 38);background-color:rgb(235, 245, 255);">cd /home/nacos/data nacos-2:/home/nacos/data# ls connection naming protocol tenant-config-data tps</font>

# **<font style="color:rgb(6, 10, 38);">2.备份数据（以防万一）</font>**

<font style="color:rgb(6, 10, 38);">虽然我们要删的是协议缓存，但养成备份好习惯。</font>

**<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">bash</font>**

<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">编辑</font>

```plain
mv protocol protocol.bak_$(date +%F_%H%M%S)
```

# **<font style="color:rgb(6, 10, 38);">3. 删除 protocol 目录</font>**

<font style="color:rgb(6, 10, 38);">这是核心步骤。删除后，Nacos 启动时会重新初始化 Raft 状态。</font>

**<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">bash</font>**

<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">编辑</font>

```plain
rm -rf protocol
```

**<font style="color:rgb(6, 10, 38);">解释</font>**<font style="color:rgba(6, 10, 38, 0.7) !important;">：</font>

* <code><font style="color:rgb(6, 10, 38);">protocol</font></code><font style="color:rgba(6, 10, 38, 0.7) !important;">：存放 Raft 共识算法的数据（日志、快照、元数据）。删除它不会删除具体的服务注册信息（那些主要在</font><font style="color:rgba(6, 10, 38, 0.7) !important;"> </font><code><font style="color:rgb(6, 10, 38);">naming</font></code><font style="color:rgba(6, 10, 38, 0.7) !important;"> </font><font style="color:rgba(6, 10, 38, 0.7) !important;">和</font><font style="color:rgba(6, 10, 38, 0.7) !important;"> </font><code><font style="color:rgb(6, 10, 38);">config-data</font></code><font style="color:rgba(6, 10, 38, 0.7) !important;"> </font><font style="color:rgba(6, 10, 38, 0.7) !important;">中，且最终一致性依赖于 Raft），但会清除该节点的“记忆”，迫使它重新从 Leader 同步。</font>
* **<font style="color:rgb(6, 10, 38);">不要删除</font>**<font style="color:rgba(6, 10, 38, 0.7) !important;"> </font><code><font style="color:rgb(6, 10, 38);">naming</font></code><font style="color:rgba(6, 10, 38, 0.7) !important;"> </font><font style="color:rgba(6, 10, 38, 0.7) !important;">或</font><font style="color:rgba(6, 10, 38, 0.7) !important;"> </font><code><font style="color:rgb(6, 10, 38);">tenant-config-data</font></code><font style="color:rgba(6, 10, 38, 0.7) !important;">，除非你确定要清空所有注册服务。</font>

# **<font style="color:rgb(6, 10, 38);">4. 重新启动 Nacos</font>**

**<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">bash</font>**

<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">编辑</font>

```plain
kubectl rollout restart sts nacos -n uat-ksa2-middleware
```

# **<font style="color:rgb(6, 10, 38);">5. 观察日志（关键验证）</font>**


> 更新: 2026-02-27 17:42:13  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/ke4pzrhrm97vvft6>
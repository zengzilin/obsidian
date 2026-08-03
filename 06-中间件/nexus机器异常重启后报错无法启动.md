# nexus 机器异常重启后报错无法启动

 <font style="color:#DF2A3F;">nexus  *SYSTEM com.orientechnologies.orient.core.storage.impl.local.paginated.wal.OLogSegmentV2 - $ANSI{green {db=config}} For the page '5' of WAL segment '        ' amount of free space '0' does not match the end of last record in page '46490' it wi </font> 



# <font style="color:rgb(51, 51, 51);">0.删除wal文件</font>
<font style="color:rgb(51, 51, 51);">/home/nexus/sonatype-work/nexus3/db/config</font>

<font style="color:rgb(51, 51, 51);">rm -rf *.wal</font>

# 1.进入console，并且连接数据库
:::info
java -jar /usr/local/nexus-3.41.1-01/lib/support/nexus-orient-console.jar

:::



```plain
connect plocal:/home/nexus/sonatype-work/nexus3/db/config <username> <password>
```



# 2.备份数据库，新建数据库并恢复
<font style="color:rgb(51, 51, 51);">orientdb> export database config-export</font>

<font style="color:rgb(51, 51, 51);">orientdb> drop database</font>

新建数据库并恢复

<font style="color:rgb(51, 51, 51);">orientdb> create database plocal:/home/nexus/sonatype-work/nexus3/db/config admin admin</font>

<font style="color:rgb(51, 51, 51);">orientdb> import database config-export.json.gz -preserveClusterIDs=true</font>

<font style="color:rgb(51, 51, 51);">orientdb> rebuild index *</font>

<font style="color:rgb(51, 51, 51);">orientdb> disconnect</font>

# <font style="color:rgb(51, 51, 51);">3.授权并启动nexus</font>
<font style="color:rgb(51, 51, 51);">还需要给db数据库更改权限，现在很多属主是root启动会有问题。</font>

<font style="color:rgb(51, 51, 51);">chmod 777 -R  /home/nexus/sonatype-work/nexus3/db</font>

启动命令

:::info
<font style="color:#DF2A3F;">/usr/local/nexus-3.41.1-01/bin/nexus run</font>

:::

  
 参考文档



[https://www.cnblogs.com/xiaoxiaomuyuyu/p/16004284.html](https://www.cnblogs.com/xiaoxiaomuyuyu/p/16004284.html)

1. _<font style="color:rgb(160, 161, 167);"># 修复</font>_
2. <font style="color:rgb(152, 104, 1);">REBUILD</font><font style="color:rgb(152, 104, 1);">INDEX</font><font style="color:rgb(56, 58, 66);"> *</font>
3. <font style="color:rgb(152, 104, 1);">REPAIR</font><font style="color:rgb(152, 104, 1);">DATABASE</font><font style="color:rgb(56, 58, 66);"> --fix-graph</font>
4. <font style="color:rgb(152, 104, 1);">REPAIR</font><font style="color:rgb(152, 104, 1);">DATABASE</font><font style="color:rgb(56, 58, 66);"> --fix-links</font>
5. <font style="color:rgb(152, 104, 1);">REPAIR</font><font style="color:rgb(152, 104, 1);">DATABASE</font><font style="color:rgb(56, 58, 66);"> --fix-ridbags</font>
6. <font style="color:rgb(152, 104, 1);">REPAIR</font><font style="color:rgb(152, 104, 1);">DATABASE</font><font style="color:rgb(56, 58, 66);"> --fix-bonsai</font>
7. <font style="color:rgb(152, 104, 1);">DISCONNECT</font>



> 更新: 2024-09-30 15:45:02  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/vt3595gg9gncufog>
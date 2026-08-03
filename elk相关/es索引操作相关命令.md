# es索引操作相关命令

**<font style="color:rgb(31, 35, 40);">删除旧索引</font>**<font style="color:rgb(31, 35, 40);">：</font>

```plain
curl -X DELETE "localhost:9200/your_old_index"
```

<font style="color:rgb(31, 35, 40);">  
</font>

查看索引

curl -u username:password -X GET "[http://localhost:9200/_cat/indices?v"](http://localhost:9200/_cat/indices?v")

**<font style="color:rgb(31, 35, 40);">关闭索引</font>**<font style="color:rgb(31, 35, 40);">： 在删除索引之前，您可以先关闭索引以释放资源：</font>

```plain
curl -X POST "localhost:9200/your_large_index/_close"
```

<font style="color:rgb(31, 35, 40);">  
</font>

查看索引的存储大小： 使用_cat/indices命令并添加h=store参数可以只查看索引的存储大小：  


```plain
curl -X GET "localhost:9200/_cat/indices?v&h=index,store.size"
```

<font style="color:rgb(31, 35, 40);">  
</font>**<font style="color:rgb(31, 35, 40);">查看索引的文档数量</font>**<font style="color:rgb(31, 35, 40);">： 使用</font><font style="color:rgb(31, 35, 40);">_cat/indices</font><font style="color:rgb(31, 35, 40);">命令并添加</font><font style="color:rgb(31, 35, 40);">h=docs.count</font><font style="color:rgb(31, 35, 40);">参数可以只查看索引的文档数量</font>

```plain
curl -X GET "localhost:9200/_cat/indices?v&h=index,docs.count"
```

<font style="color:rgb(31, 35, 40);">  
</font>

**查看索引的分片信息**： 使用_cat/shards命令可以查看索引的分片信息：

```plain
curl -X GET "localhost:9200/_cat/shards?v"
```

<font style="color:rgb(31, 35, 40);">  
</font>



> 更新: 2024-05-24 15:59:51  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/rph7r73ykfgy28zs>
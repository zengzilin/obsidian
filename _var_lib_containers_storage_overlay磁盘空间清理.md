# /var/lib/containers/storage/overlay 磁盘空间清理

1.清理Exited状态的容器

crictl ps -a | grep -Ev "Running|CONTAINER"|awk '{print $1}'|xargs crictl rm

2.清理无用镜像

```shell
crictl rmi $(crictl images | grep -E -- '<none>' | awk '{print $3}')
```



> 更新: 2024-09-27 09:04:24  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/bwdopxzg6ygr2ogk>
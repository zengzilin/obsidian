# 清理cri-o或containerd的磁盘目录文件

<font style="color:rgb(6, 6, 7);">清理 </font>`containerd`<font style="color:rgb(6, 6, 7);"> 的 </font>`/var/lib/containers/storage/overlay`<font style="color:rgb(6, 6, 7);"> 目录通常涉及到清理不再使用的容器、镜像、以及卷等。以下是一些常用的清理步骤：</font>

1. **<font style="color:rgb(6, 6, 7);">清理悬空镜像</font>**<font style="color:rgb(6, 6, 7);">：</font>

```plain
bash

crictl images | awk 'NR>1 {print $3}' | xargs crictl rmi
```

<font style="color:rgb(6, 6, 7);">这个命令会删除所有未被引用的镜像</font><font style="color:rgb(6, 6, 7);">。</font>

2. **<font style="color:rgb(6, 6, 7);">清理停止的容器</font>**<font style="color:rgb(6, 6, 7);">：</font>

```plain
bash

crictl ps -a | grep -v Running | awk '{print $1}' | xargs sudo crictl rm
```

<font style="color:rgb(6, 6, 7);">这个命令会停止并删除所有非运行中的容器</font><font style="color:rgb(6, 6, 7);">。</font>

3. **<font style="color:rgb(6, 6, 7);">清理未使用的卷</font>**<font style="color:rgb(6, 6, 7);">：</font>

```plain
bash

crictl volumes ls -qf dangling=true | xargs crictl volume rm
```

<font style="color:rgb(6, 6, 7);">这个命令会删除所有未被引用的卷。</font>

4. **<font style="color:rgb(6, 6, 7);">清理未使用的网络</font>**<font style="color:rgb(6, 6, 7);">：</font>

```plain
bash

crictl networks ls | grep -v "default" | awk '{print $1}' | xargs crictl network rm
```

<font style="color:rgb(6, 6, 7);">这个命令会删除所有非默认的网络。</font>

5. **<font style="color:rgb(6, 6, 7);">清理containerd的容器日志</font>**<font style="color:rgb(6, 6, 7);">： 有时候容器的日志文件可能会占用大量空间，可以清空容器的日志文件来释放空间：</font>

```plain
bash

find /var/lib/containers/storage/overlay -name '*-json.log' -exec cat /dev/null > {} \;
```

<font style="color:rgb(6, 6, 7);">这个命令会清空所有的容器日志文件。</font>

6. **<font style="color:rgb(6, 6, 7);">手动清理overlay目录</font>**<font style="color:rgb(6, 6, 7);">： 如果上述自动化清理方法没有释放足够的空间，可能需要手动检查 </font>`/var/lib/containers/storage/overlay`<font style="color:rgb(6, 6, 7);"> 目录，并删除不再需要的层。</font>
7. **<font style="color:rgb(6, 6, 7);">调整containerd配置</font>**<font style="color:rgb(6, 6, 7);">： 可以在 </font>`/etc/containerd/config.toml`<font style="color:rgb(6, 6, 7);"> 中设置 </font>`discard_unpacked_layers`<font style="color:rgb(6, 6, 7);"> 为 </font>`true`<font style="color:rgb(6, 6, 7);">，这样在解压镜像层后，原始的镜像层可以被垃圾回收清理掉</font><font style="color:rgb(6, 6, 7);">。</font>
8. **<font style="color:rgb(6, 6, 7);">重启containerd服务</font>**<font style="color:rgb(6, 6, 7);">： 清理完成后，重启containerd服务以确保所有更改生效：</font>

```plain
bash

systemctl restart containerd
```


> 更新: 2024-09-25 11:11:45  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/cscicrye657lnvlx>
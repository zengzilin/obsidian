# OCI oracle linux系统扩容根分区

![1753964912882-7b57d60a-c426-404c-aac3-69d6d16d6b94.png](./img/1BqGQhbOqxt763Ce/1753964912882-7b57d60a-c426-404c-aac3-69d6d16d6b94-189885.png)

运维已经在平台扩容根分区到200G，但是没有实际生效。

# 重新scan一下根分区(可选，先执行oci-growfs试试)
<font style="color:#DF2A3F;">/dev/sdx以实际为准</font>

```plain
 sudo dd iflag=direct if=/dev/sda of=/dev/null count=1
echo "1" | sudo tee /sys/class/block/sda/device/rescan  
```

# 执行oci-growfs命令动态扩容
```plain
  /usr/libexec/oci-growfs  -y
```

<font style="color:#DF2A3F;">tips 只有oracle linux有这个命令</font>



> 更新: 2025-07-31 21:07:56  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/rh76mkhqxrs5nwhi>
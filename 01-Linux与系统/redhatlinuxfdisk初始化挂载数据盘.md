# redhat linux fdisk初始化挂载数据盘

### 1.1使用 `fdisk` 对 `sdx` 分区,比如sda（磁盘小于2T）

```plain
fdisk /dev/sda
```

```plain
Command (m for help): n   ← 创建新分区
Partition type
   p   primary (0 primary, 0 extended, 4 free)
   e   extended
Select (default p): p     ← 主分区
Partition number (1-4, default 1): 1  ← 默认就可以
First sector (2048-..., default 2048):  ← 回车
Last sector, +sectors or +size{K,M,G,T,P} (2048-..., default ...):  ← 回车（使用整块磁盘）
```

### 1.2使用 `fdisk` 对 `sdx` 分区,比如sda（磁盘大于2T）

```plain
fdisk /dev/sda
```

```plain
g # 创建GPT分区表（会清除现有分区表）
```

```plain
Command (m for help): n   ← 创建新分区
Partition type
   p   primary (0 primary, 0 extended, 4 free)
   e   extended
Select (default p): p     ← 主分区
Partition number (1-4, default 1): 1  ← 默认就可以
First sector (2048-..., default 2048):  ← 回车
Last sector, +sectors or +size{K,M,G,T,P} (2048-..., default ...):  ← 回车（使用整块磁盘）
```

### 2.格式化分区，格式化为 XFS 的命令如下：

```plain
mkfs.xfs /dev/sda1
```

### 3. 创建挂载点：

```plain
mkdir -p /data
```

### 4. 挂载：

```plain
mount /dev/sda1 /data
```

### 5. 验证：

```plain
df -Th | grep /data
```

你应该能看到类似：

```plain

/dev/sda1     xfs   1.0T   33M  1.0T   1% /data
```

***

### 6. 写入 `/etc/fstab`（XFS 也可以自动挂载）

查看 UUID：

```plain
blkid /dev/sda1
```

添加到 `/etc/fstab`：

```plain
echo 'UUID=你的UUID /data xfs defaults 0 0' >> /etc/fstab
```


> 更新: 2025-09-18 17:22:01  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/mw2goasvgf9amgq9>
# Redhat linux 扩容根磁盘

![1753966567368-6e06acc4-d5a8-44cb-8e0c-d2f350d501ba.png](./img/iK1wGYGoJcgBKpJJ/1753966567368-6e06acc4-d5a8-44cb-8e0c-d2f350d501ba-895678.png)

运维已经将磁盘在线扩容到200G，当前的磁盘为 `sda`，已经扩容到 **200G**，但用于 LVM 的分区 `/dev/sda4` 仍然只有 **27G**，也就是说：

**磁盘虽然扩容了，但用于 LVM 的分区 **<code>**sda4**</code>** 还没扩容，LVM 也无法使用多出的空间。**

:::danger
从第二步开始，两个操作系统的命令都一样

:::

***

## 1.1 扩展 `/dev/sda4` 分区容量（OCI redhat8.10）

由于你使用的是 `MBR` 或 `GPT` 分区（目前 `sda4` 是主分区），我们可以使用 `growpart` 安全扩容。

### 扩展 `sda4` 分区

```plain
bash
安装growpart命令
dnf install cloud-utils-growpart  -y

sudo growpart /dev/sda 4

CHANGED: partition=2 start=411648 old: size=419016800 end=419428447 new: size=4294555615 end=4294967262

```

这一步将 `/dev/sda4` 扩展到磁盘剩余空间（应变为接近 200G）。

***

# 1.2  扩展 `/dev/sda4` 分区容量（redhat 9.6）

redhat 9.6没有growpart命令

可以用<font style="color:#DF2A3F;">parted</font>命令

## 1.2.1 <font style="color:rgba(0, 0, 0, 0.85);">运行</font><code><font style="color:rgba(0, 0, 0, 0.85) !important;">parted</font></code><font style="color:rgba(0, 0, 0, 0.85);">工具操作磁盘：</font>

```plain
parted /dev/sda
```

## <font style="color:rgba(0, 0, 0, 0.85);">1.2.2查看当前分区表并确认</font><code><font style="color:rgba(0, 0, 0, 0.85);">sda4</font></code><font style="color:rgba(0, 0, 0, 0.85);">的分区号：</font>

```plain
(parted) print
```

<font style="color:rgba(0, 0, 0, 0.85) !important;">（确认</font><code><font style="color:rgba(0, 0, 0, 0.85) !important;">sda4</font></code><font style="color:rgba(0, 0, 0, 0.85) !important;">的</font><code><font style="color:rgba(0, 0, 0, 0.85) !important;">Number</font></code><font style="color:rgba(0, 0, 0, 0.85) !important;">为 4，且分区类型为</font><code><font style="color:rgba(0, 0, 0, 0.85) !important;">lvm</font></code><font style="color:rgba(0, 0, 0, 0.85) !important;">）</font>

## <font style="color:rgba(0, 0, 0, 0.85);">1.2.3 出现warning,需要执行fix,才能识别出sda磁盘的真实大小</font>

**<font style="color:#DF2A3F;">Using /dev/sda</font>**

**<font style="color:#DF2A3F;">Welcome to GNU Parted! Type 'help' to view a list of commands.</font>**

**<font style="color:#DF2A3F;">(parted) print</font>**

**<font style="color:#DF2A3F;">Warning: Not all of the space available to /dev/sda appears to be used, you can fix the GPT to use all of the space (an extra 150571008 blocks) or continue with the current setting?</font>**

**<font style="color:#DF2A3F;">Fix/Ignore? Fix</font>**

<font style="color:rgba(0, 0, 0, 0.85) !important;">Model: Google PersistentDisk (scsi)</font>

<font style="color:#DF2A3F;">Disk /dev/sda: 107GB</font>

<font style="color:rgba(0, 0, 0, 0.85) !important;">Sector size (logical/physical): 512B/4096B</font>

<font style="color:rgba(0, 0, 0, 0.85) !important;">Partition Table: gpt</font>

<font style="color:rgba(0, 0, 0, 0.85) !important;"></font>

## <font style="color:rgba(0, 0, 0, 0.85);">1.2.4调整</font><code><font style="color:rgba(0, 0, 0, 0.85);">sda4</font></code><font style="color:rgba(0, 0, 0, 0.85);">分区大小（扩展到最大可用空间）：</font>

```plain
(parted) resizepart 4  # 选择第4个分区
(parted) 100%          # 将分区扩展到磁盘末尾（或指定具体大小，如150G）
(parted) quit          # 退出parted
```

## <font style="color:rgba(0, 0, 0, 0.85);">1.2.5刷新分区表使系统识别变更：</font>

```plain
partprobe /dev/sda
```

# 🔍 第 2 步：确认分区扩展成功

```plain
lsblk
```

你应看到 `sda4` 的 `SIZE` 从 27G ➜ 接近 200G。

***

# 如果是xfs系统，不是lvm不支持用pvsize命令

![1761185107760-ba953733-bdf1-4b52-ad49-4c44555a334e.png](./img/iK1wGYGoJcgBKpJJ/1761185107760-ba953733-bdf1-4b52-ad49-4c44555a334e-548275.png)

## **扩展 XFS 文件系统**

sudo xfs\_growfs /

/ 是你的根挂载点，也可以写成 /dev/sda2，但推荐直接用挂载点。

扩展成功输出信息如下

![1761185269403-c9ee6202-3c60-4cc6-990d-e84a4d71ced4.png](./img/iK1wGYGoJcgBKpJJ/1761185269403-c9ee6202-3c60-4cc6-990d-e84a4d71ced4-992587.png)

![1761185330280-5bbdccb4-f872-43e3-b74f-4131d642ab46.png](./img/iK1wGYGoJcgBKpJJ/1761185330280-5bbdccb4-f872-43e3-b74f-4131d642ab46-063304.png)

# 如果是lvm系统，请执行如下步骤

## 🧱 第 1 步：扩展物理卷 PV

```plain
#安装 pvresize命令
dnf install lvm2 -y

#有可能是sdb，需要看清楚 (growpart执行成功之后可以不执行pvsize)
sudo pvresize /dev/sda4
```

这一步会把新扩展的空间注入到 `rootvg` 卷组。

***

## 💡 第 2步：确认卷组 VG 和可用空间

```plain
sudo vgs
```

输出示例：

```plain
VG     #PV #LV #SN Attr   VSize   VFree
rootvg   1   7   0 wz--n- <200.00g <173.00g
```

***

## ➕ 第 3 步：扩展某个逻辑卷（例如 `/`）

假如你想把所有空间都给 `/`（根目录）：

```plain
sudo lvextend -l +100%FREE /dev/mapper/rootvg-rootlv
```

***

## 📦 第 4步：扩展 XFS 文件系统（上一步的 `/`分区）

```plain
sudo xfs_growfs /
```

***

## ✅ 第 5 步：验证

```plain
df -Th
```

你应能看到 `/` 容量由 10G 变为接近 200G。

## ⛳ 如果想按比例分配空间给 `/home``/var``/tmp` 等目录：

先查看每个 LV 名称：

```plain
sudo lvs
```

然后可以选择性扩展某个 LV：

```plain
sudo lvextend -L +5G /dev/mapper/rootvg-homelv
sudo xfs_growfs /home
```


> 更新: 2026-01-28 16:30:18  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/ynmnv6rrd7cr14f7>
# Failed to mount /sysroot

![1745849933952-3e3ad5f8-40e7-4179-a28f-386e0aa5ccc9.png](./img/0_X9U3WFI2hz-3Yp/1745849933952-3e3ad5f8-40e7-4179-a28f-386e0aa5ccc9-051737.png)

<font style="color:rgba(0, 0, 0, 0.85) !important;">这是系统启动时出现错误的提示信息，主要问题是 </font><code><font style="color:rgba(0, 0, 0, 0.85) !important;">Failed to mount /sysroot</font></code><font style="color:rgba(0, 0, 0, 0.85) !important;">（挂载 </font><code><font style="color:rgba(0, 0, 0, 0.85) !important;">/sysroot</font></code><font style="color:rgba(0, 0, 0, 0.85) !important;"> 失败 ）。以下是可能的原因及解决办法：</font>

### <font style="color:rgb(0, 0, 0);">原因</font>

1. **<font style="color:rgb(0, 0, 0) !important;">文件系统损坏</font>**<font style="color:rgba(0, 0, 0, 0.85) !important;">：磁盘故障、突然断电等可能导致</font><font style="color:rgba(0, 0, 0, 0.85) !important;"> </font><code><font style="color:rgb(0, 0, 0);">/sysroot</font></code><font style="color:rgba(0, 0, 0, 0.85) !important;"> </font><font style="color:rgba(0, 0, 0, 0.85) !important;">对应的文件系统（如根分区）出现元数据损坏、文件系统结构错误等问题，使得系统无法正常挂载。</font>
2. **<font style="color:rgb(0, 0, 0) !important;">配置错误</font>**<font style="color:rgba(0, 0, 0, 0.85) !important;">：</font><code><font style="color:rgb(0, 0, 0);">/etc/fstab</font></code><font style="color:rgba(0, 0, 0, 0.85) !important;"> </font><font style="color:rgba(0, 0, 0, 0.85) !important;">等挂载配置文件中关于</font><font style="color:rgba(0, 0, 0, 0.85) !important;"> </font><code><font style="color:rgb(0, 0, 0);">/sysroot</font></code><font style="color:rgba(0, 0, 0, 0.85) !important;"> </font><font style="color:rgba(0, 0, 0, 0.85) !important;">挂载点的参数设置错误，比如指定的 UUID、设备名与实际不符，或者挂载选项有误，会导致挂载失败。</font>
3. **<font style="color:rgb(0, 0, 0) !important;">驱动问题</font>**<font style="color:rgba(0, 0, 0, 0.85) !important;">：如果根文件系统所在磁盘的驱动程序缺失、损坏或版本不兼容，可能无法正确识别和挂载磁盘，进而导致</font><font style="color:rgba(0, 0, 0, 0.85) !important;"> </font><code><font style="color:rgb(0, 0, 0);">/sysroot</font></code><font style="color:rgba(0, 0, 0, 0.85) !important;"> </font><font style="color:rgba(0, 0, 0, 0.85) !important;">挂载失败。</font>
4. **<font style="color:rgb(0, 0, 0) !important;">硬件故障</font>**<font style="color:rgba(0, 0, 0, 0.85) !important;">：磁盘本身出现物理故障，如坏道、接口松动等，会影响文件系统的正常挂载。</font>

### <font style="color:rgb(0, 0, 0);">解决办法</font>

1. **<font style="color:rgb(0, 0, 0) !important;">检查文件系统</font>**<font style="color:rgba(0, 0, 0, 0.85) !important;">：在当前进入的紧急 shell 环境下，使用文件系统检查工具。对于常见的 XFS 文件系统，可用 </font><code><font style="color:rgb(0, 0, 0);">xfs_repair</font></code><font style="color:rgba(0, 0, 0, 0.85) !important;"> 命令（如 </font><code><font style="color:rgb(0, 0, 0);">xfs_repair /dev/sdaX</font></code><font style="color:rgba(0, 0, 0, 0.85) !important;">，</font><code><font style="color:rgb(0, 0, 0);">sdaX</font></code><font style="color:rgba(0, 0, 0, 0.85) !important;"> 需替换为实际根分区设备名，可通过 </font><code><font style="color:rgb(0, 0, 0);">fdisk -l</font></code><font style="color:rgba(0, 0, 0, 0.85) !important;"> 等命令查看 ）；对于 ext4 文件系统，使用 </font><code><font style="color:rgb(0, 0, 0);">fsck.ext4 /dev/sdaX</font></code><font style="color:rgba(0, 0, 0, 0.85) !important;"> 尝试修复。</font>

比如 上图 使用 xfs\_repair /dev/sda2 解决

进入救援模式

```plain
systemd.unit=emergency.target rd.break 
```

# <font style="color:rgb(0, 0, 0);">“xfs\_repair: cannot open /dev/sda2: Device or resource busy”</font>

* **<font style="color:rgb(0, 0, 0) !important;">解决办法</font>**<font style="color:rgba(0, 0, 0, 0.85) !important;">：</font>
  * <font style="color:rgba(0, 0, 0, 0.85) !important;">使用</font><font style="color:rgba(0, 0, 0, 0.85) !important;"> </font><code><font style="color:rgb(0, 0, 0);">lsof /dev/sda2</font></code><font style="color:rgba(0, 0, 0, 0.85) !important;"> </font><font style="color:rgba(0, 0, 0, 0.85) !important;">查看哪些进程在使用该分区，然后使用</font><font style="color:rgba(0, 0, 0, 0.85) !important;"> </font><code><font style="color:rgb(0, 0, 0);">kill -9 <进程ID></font></code><font style="color:rgba(0, 0, 0, 0.85) !important;"> </font><font style="color:rgba(0, 0, 0, 0.85) !important;">杀掉相关进程（注意谨慎操作，避免影响重要业务 ）。</font>
  * <font style="color:rgba(0, 0, 0, 0.85) !important;">确保分区已正确卸载，可使用 </font><code><font style="color:rgb(0, 0, 0);">umount /dev/sda2</font></code><font style="color:rgba(0, 0, 0, 0.85) !important;"> 命令尝试卸载，若提示无法卸载，按上述方法排查占用进程。</font>
  * <font style="color:rgba(0, 0, 0, 0.85) !important;">本次解决方式</font>
  * <font style="color:rgba(0, 0, 0, 0.85) !important;"></font>

<font style="color:rgb(0, 0, 0);">umount /dev/sda2</font>

xfs\_repair /dev/sda2 解决


> 更新: 2025-04-28 22:35:14  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/cuuwma19qh13hvrw>
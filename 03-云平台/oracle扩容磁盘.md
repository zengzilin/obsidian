# oracle扩容磁盘

# 1.需求.磁盘有300G /分区只分配了35G ，将剩余空间都分配到根分区
命令

:::info
<font style="color:rgb(0, 0, 0);">usr/libexec/oci-growfs</font>

:::

<font style="color:rgb(0, 0, 0);"></font>

<font style="color:rgb(0, 0, 0);"></font>

# <font style="color:#DF2A3F;">2.需求：磁盘原有5T，扩容到了10T，但是lsblk看不到，需要先把磁盘扫出来</font>
# 1.oracle云磁盘重新识别磁盘文件
oracle云磁盘根目录扩容命令

sudo dd iflag=direct if=/dev/sdb1 of=/dev/null count=1

sudo  echo "1" | sudo tee /sys/class/block/sdb/device/rescan

# 2.oracle云磁盘扩容
超过2T 磁盘分区表格式需要用gpt，此处已修改，可以直接扩容

growpart /dev/sdb 1





# 3.扩容文件系统
磁盘扩容之后

xfs扩容命令：

<font style="color:rgb(199, 37, 78);background-color:rgb(249, 242, 244);">xfs_growfs /dev/vdb1 </font>

<font style="color:rgb(199, 37, 78);background-color:rgb(249, 242, 244);">ext扩容命令</font>

<font style="color:rgb(199, 37, 78);background-color:rgb(249, 242, 244);">resize2fs /dev/vdb1</font>

<font style="color:rgb(199, 37, 78);background-color:rgb(249, 242, 244);"></font>

<font style="color:rgb(199, 37, 78);background-color:rgb(249, 242, 244);">参考文档</font>

[https://docs.oracle.com/en-us/iaas/Content/Block/Tasks/rescanningdisk.htm](https://docs.oracle.com/en-us/iaas/Content/Block/Tasks/rescanningdisk.htm)



[https://docs.oracle.com/en-us/iaas/Content/Block/Tasks/extendingblockpartition.htm](https://docs.oracle.com/en-us/iaas/Content/Block/Tasks/extendingblockpartition.htm)



[https://blog.csdn.net/weixin_43863487/article/details/119576461](https://blog.csdn.net/weixin_43863487/article/details/119576461)



> 更新: 2024-11-07 23:23:41  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/sxwd34syx49qmmqm>
# Linux 系统硬盘MBR转换为GPT格式并扩容

### 问题描述
之前创建了一台ubuntu16的服务器虚机，挂载了一块2T的云数据盘，当时文件系统做的是MBR（dos）格式，最近因为存量数据增加，数据盘空间不足就在云平台将2T的数据盘扩容成了4T，结果进入虚机扩容的时候报错MBR格式的硬盘最大支持2T，剩余的空间将不会用到。

需要将硬盘转化为GPT分区格式，来支持2T以上空间的使用才行，但是转化硬盘格式又怕数据丢失，于是又找了一台虚机用来测试。



### <font style="color:rgb(79, 79, 79);">解决方案</font>
<font style="color:rgb(77, 77, 77);">fdisk工具支持MBR分区格式的硬盘操作，查看当前硬盘的信息：  
</font>![1718178083852-485626f5-f0ec-43ee-8c10-048f37af422c.png](./img/kj3hd5QxWFSaUA-X/1718178083852-485626f5-f0ec-43ee-8c10-048f37af422c-080985.png)<font style="color:rgb(77, 77, 77);">  
</font><font style="color:rgb(77, 77, 77);">可以看到硬盘大小是4T，但是分区里最大只能用2T。</font>

<font style="color:rgb(77, 77, 77);"></font>

**<font style="color:rgb(77, 77, 77);">操作对数据做好备份或快照，防止操作失败数据丢失。</font>**

#### <font style="color:rgb(79, 79, 79);">将MBR转化为GPT分区格式</font>
<font style="color:rgb(77, 77, 77);">使用gdisk工具，将分区表改为gpt格式</font>

![1718178180370-371bee1d-01b8-4d97-a596-b303b00bbbfc.png](./img/kj3hd5QxWFSaUA-X/1718178180370-371bee1d-01b8-4d97-a596-b303b00bbbfc-780110.png)



使用gdisk 硬盘盘符 命令进入程序后，直接 输入w保存并退出，然后输入y确认。gdisk就会将硬盘改为gpt格式分区。

注意：gdisk命令后面跟的是硬盘设备路径/dev/vdb，不是分区路径/dev/vdb1，如果指定错了会变更失败丢失数据



这个方法在大部分场景下都是可以转mbr为gpt的，只有磁盘开头前33个扇区，或最后34个扇区被分区占用的场景不支持。（如，原来的硬盘已经使用MBR分区占用了全部的空间，即后34个扇区被占用了，那么操作会失败）但是对于扩容的场景，后34个扇区尚未被占用，一般不会出问题。



<font style="color:rgb(77, 77, 77);">现在查看硬盘分区信息，就会显示其格式为gpt格式：</font>

![1718178253400-d3eee191-bc60-49f1-861f-126a565cf545.png](./img/kj3hd5QxWFSaUA-X/1718178253400-d3eee191-bc60-49f1-861f-126a565cf545-186576.png)

  
 

#### <font style="color:rgb(79, 79, 79);">扩容数据盘及文件系统</font>
<font style="color:rgb(77, 77, 77);">扩容数据盘：</font>  
 ![1718178290668-70811fc0-ac54-4724-bf34-4e74f69ec77f.png](./img/kj3hd5QxWFSaUA-X/1718178290668-70811fc0-ac54-4724-bf34-4e74f69ec77f-414085.png)



<font style="color:rgb(77, 77, 77);">扩容文件系统：</font>

![1718178368404-57d8e283-981a-4d3b-9c29-21974b2277f4.png](./img/kj3hd5QxWFSaUA-X/1718178368404-57d8e283-981a-4d3b-9c29-21974b2277f4-178077.png)



<font style="color:rgb(77, 77, 77);">扩容后，数据盘大小变为4T。  
</font><font style="color:rgb(77, 77, 77);">对于xfs文件系统格式，需要使用</font><font style="color:rgb(199, 37, 78);background-color:rgb(249, 242, 244);">xfs_growfs</font><font style="color:rgb(77, 77, 77);">命令进行扩容文件系统操作。</font>

<font style="color:rgb(77, 77, 77);">现在通过gdisk命令来查看数据盘的信息：</font>

![1718178414897-59f91071-73e7-4567-8f83-72abc95aed5a.png](./img/kj3hd5QxWFSaUA-X/1718178414897-59f91071-73e7-4567-8f83-72abc95aed5a-697627.png)

从图中可以看到，数据盘的分区表信息是由两部分组成的，一部分是MBR: protective，另一部分是GPT: present，这种分区格式成为Hybrid MBR，可以将MBR分区表和GPT分区表混合使用。



将文件系统重新挂在后，查看目录下的文件，没有出现数据丢失的情况。

还可以umount卸载挂载的设备，然后使用e2fsck命令检查文件系统有没有错误。





> 更新: 2024-06-12 15:47:25  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/qkotz5yoy7ssbucs>
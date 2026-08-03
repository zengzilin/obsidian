# crontab添加用户

<font style="color:rgba(0, 0, 0, 0.85);background-color:rgba(0, 0, 0, 0.04);">\[cloud-user@jed-prod-vm-wallyt-jump-01 backup]$ crontab -l You (cloud-user) are not allowed to use this program (crontab) See crontab(1) for more information</font>

<font style="color:rgba(0, 0, 0, 0.85) !important;">当你运行</font><font style="color:rgba(0, 0, 0, 0.85) !important;"> </font><code><font style="color:rgba(0, 0, 0, 0.85) !important;">crontab -l</font></code><font style="color:rgba(0, 0, 0, 0.85) !important;"> </font><font style="color:rgba(0, 0, 0, 0.85) !important;">时出现 "You (cloud-user) are not allowed to use this program (crontab)" 错误，这表明当前用户（cloud-user）没有权限使用 crontab 命令。</font>

<font style="color:rgb(0, 0, 0);">  
</font>

<font style="color:rgba(0, 0, 0, 0.85) !important;">这种限制通常是由系统管理员通过以下方式设置的：</font>

<font style="color:rgb(0, 0, 0);">  
</font>

1. **<font style="color:rgb(0, 0, 0) !important;">/etc/cron.allow 文件</font>**<font style="color:rgba(0, 0, 0, 0.85) !important;">：如果存在这个文件，只有文件中列出的用户才能使用 crontab</font>
2. **<font style="color:rgb(0, 0, 0) !important;">/etc/cron.deny 文件</font>**<font style="color:rgba(0, 0, 0, 0.85) !important;">：如果存在这个文件，文件中列出的用户被禁止使用 crontab</font>


> 更新: 2025-07-31 11:57:35  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/vswtcuoqkwwkzydq>
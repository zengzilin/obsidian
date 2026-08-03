# rclone同步数据

# <font style="color:rgb(28, 31, 35);"> 将灾备数据同步到生产环境</font>

<font style="color:rgb(28, 31, 35);"> rclone sync disaster: production: --exclude-from "/etc/rclone\_excludes.txt" --transfers 32 --checkers 32 </font>

# <font style="color:rgb(28, 31, 35);">反向同步确保一致性（可根据实际情况选择是否执行） </font>

<font style="color:rgb(28, 31, 35);">rclone sync production: disaster: --exclude-from "/etc/rclone\_excludes.txt" --transfers 32 --checkers 32 --update</font>

<font style="color:rgb(28, 31, 35);"></font>

# <font style="color:rgb(28, 31, 35);">同步前检查操作 rclone check</font>

## <font style="color:rgba(0, 0, 0, 0.85);">如果只需要快速查看差异结果，可添加</font><code><font style="color:rgba(0, 0, 0, 0.85);">--differ</font></code><font style="color:rgba(0, 0, 0, 0.85);">参数（仅列出不一致的文件）</font>

<font style="color:rgb(28, 31, 35);">rclone check production: disaster  --differ </font>

## <font style="color:rgba(0, 0, 0, 0.85);">若数据量较大（如 TB 级），可添加</font><code><font style="color:rgba(0, 0, 0, 0.85);">--stats</font></code><font style="color:rgba(0, 0, 0, 0.85);">参数定期输出进度统计</font>

<font style="color:rgb(28, 31, 35);">rclone check production: disaster: \ --stats 10s \ # 每10秒输出一次统计（已检查文件数、差异数等） --exclude-from /etc/rclone\_excludes.txt\ </font><font style="color:rgb(28, 31, 35);"> </font>

# <font style="color:rgb(28, 31, 35);">rclone查看桶实际存储大小</font>

<font style="color:rgb(28, 31, 35);">rclone size  gcp:bkt-tiq-damm-p-logs --human-readable</font>


> 更新: 2026-03-27 22:15:24  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/vkaeeb1ga5gq2m6r>
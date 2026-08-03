# rsync同步生产和灾备的数据

# 同步前：识别灾备环境新增的几十 GB 数据

<font style="color:rgba(0, 0, 0, 0.85);">使用 rsync 的</font><code><font style="color:rgba(0, 0, 0, 0.85);">--dry-run</font></code><font style="color:rgba(0, 0, 0, 0.85);">模式结合输出解析，生成灾备环境新增文件列表：</font>\
\#!/bin/bash

:::info

# 定义路径和日志文件

PROD="/nfs/production"

DR="/nfs/disaster\_recovery"

LOG="/var/log/nfs\_sync\_changes\_$(date +%Y%m%d).log"

NEW\_FILES="/var/log/nfs\_new\_files\_$(date +%Y%m%d).txt"

# 生成差异报告（仅显示灾备环境新增的文件）

rsync -anv --delete --exclude-from="/etc/rsync\_excludes.txt" $PROD/ $DR/ | grep '^>f' | awk '{print $NF}' > $NEW\_FILES

# 统计新增文件大小

echo "灾备环境新增文件列表：" > $LOG

cat $NEW\_FILES >> $LOG

echo -e "\n新增文件总大小：" >> $LOG

du -shc $(cat $NEW\_FILES) >> $LOG 2>/dev/null

echo "差异分析完成，结果保存在 $LOG 和 $NEW\_FILES"

:::

# <font style="color:rgb(0, 0, 0);">2. </font>**<font style="color:rgb(0, 0, 0) !important;">执行双向同步（重点保护生产环境新数据）</font>**

<font style="color:rgba(0, 0, 0, 0.85);">使用两次 rsync 操作实现双向同步：</font>

:::info

\#!/bin/bash

# 定义路径

PROD="/nfs/production"

DR="/nfs/disaster\_recovery"

EXCLUDES="/etc/rsync\_excludes.txt"

LOG="/var/log/nfs\_bidirectional\_sync\_$(date +%Y%m%d).log"

# 1. 将灾备环境新增数据同步到生产环境（保护生产环境已有文件）

echo "开始同步灾备环境新增数据到生产环境..." | tee -a $LOG

rsync -avz --update --exclude-from=$EXCLUDES --log-file=$LOG $DR/ $PROD/

# 2. 将生产环境新增数据同步到灾备环境（确保完全一致）

echo "开始同步生产环境新增数据到灾备环境..." | tee -a $LOG

rsync -avz --delete --exclude-from=$EXCLUDES --log-file=$LOG $PROD/ $DR/

echo "双向同步完成！" | tee -a $LOG

:::

# **<font style="color:rgb(0, 0, 0) !important;">3.完整工作流</font>**

1. **<font style="color:rgb(0, 0, 0) !important;">灾备切换前</font>**<font style="color:rgba(0, 0, 0, 0.85) !important;">：</font>
   * <font style="color:rgba(0, 0, 0, 0.85) !important;">定期执行单向同步（生产→灾备）：\ </font><code><font style="color:rgb(0, 0, 0);">rsync -avz --delete --exclude-from=$EXCLUDES $PROD/ $DR/</font></code>
2. **<font style="color:rgb(0, 0, 0) !important;">灾备环境运行期间</font>**<font style="color:rgba(0, 0, 0, 0.85) !important;">：</font>
   * <font style="color:rgba(0, 0, 0, 0.85) !important;">灾备环境产生新数据（几十 GB），但你不知道具体新增了哪些文件。</font>
3. **<font style="color:rgb(0, 0, 0) !important;">切回生产前</font>**<font style="color:rgba(0, 0, 0, 0.85) !important;">：</font>
   * <font style="color:rgba(0, 0, 0, 0.85) !important;">执行上述 “差异识别脚本”，生成灾备环境新增文件列表。</font>
   * <font style="color:rgba(0, 0, 0, 0.85) !important;">人工审核新增文件列表（</font><code><font style="color:rgb(0, 0, 0);">$NEW_FILES</font></code><font style="color:rgba(0, 0, 0, 0.85) !important;">），确认是否需要同步回生产环境。</font>
4. **<font style="color:rgb(0, 0, 0) !important;">执行双向同步</font>**<font style="color:rgba(0, 0, 0, 0.85) !important;">：</font>
   * <font style="color:rgba(0, 0, 0, 0.85) !important;">运行 “双向同步脚本”，先将灾备新增数据安全同步到生产，再确保生产与灾备完全一致。</font>


> 更新: 2025-07-13 22:33:21  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/aotkrshh88bwbngt>
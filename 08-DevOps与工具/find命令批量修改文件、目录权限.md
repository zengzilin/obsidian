# find命令批量修改文件、目录权限

# 修改文件权限
find /mnt/sftp/data/sftp/wallet/ -type f -exec chmod 644 {} +

# 修改目录权限
find /mnt/sftp/data/sftp/wallet/ -type f -exec chmod 755 {} +





> 更新: 2025-07-14 06:27:13  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/mkxb97r6buezoy0g>
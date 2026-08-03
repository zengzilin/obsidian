# 东八区时区配置方案（适用于AlmaLinux/CentOS/RHEL）

# 1. 查看当前时区状态
timedatectl status 

# 2. 设置东八区标准时区（推荐上海时区）
sudo timedatectl set-timezone Asia/Shanghai 

# 3. 强制同步硬件时钟（BIOS时间）
sudo hwclock --systohc



> 更新: 2025-04-25 09:30:15  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/xh2kiisql07pz31o>
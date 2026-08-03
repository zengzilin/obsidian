# windows server放通特定端口 允许外部访问



已管理员权限打开powershell



New-NetFirewallRule -DisplayName "开放8089端口" -Direction Inbound -Protocol TCP -LocalPort 8089 -Action Allow



> 更新: 2025-06-19 10:48:48  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/em3wfn74r15akwrx>
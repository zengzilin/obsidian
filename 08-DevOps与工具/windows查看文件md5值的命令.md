# windows查看文件md5值的命令

在powershell执行如下命令

文件名有特殊符号，需要用双引号引起来

```bash
PS D:\Users\Downloads> Get-FileHash -Path .\"【历峰】【基础平台】【SpayServer】渠道、商户审核通过邮件功能&注销场景版本sql4BCFF0DC59E62F5438118011249B4191.zip"  -Algorithm MD5
```



> 更新: 2025-10-14 07:31:49  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/zk4scl6a2tzwoda7>
# oci 对象存储解压缩对象命令

# 恢复archive对象命令 
```plain
oci os object restore-status   --namespace axfofpte3reg   --bucket-name jed-prod-bkt-k8s-share   --name "market/outPutPath/42d0207fc1b1c48e6c4825d15bd7c5ea/Expat June 1 - B2.xlsx"
```

（默认恢复保持时间是24小时，可以用--hours 指定恢复时长）



# 查看对象恢复状态
```plain
oci os object restore-status   --namespace axfofpte3reg   --bucket-name jed-prod-bkt-k8s-share   --name "market/outPutPath/42d0207fc1b1c48e6c4825d15bd7c5ea/Expat June 1 - B2.xlsx"
```

Restoring, this object is being restored and will be available for download in about 1 hour from the time you issued the restore command.





> 更新: 2025-08-13 16:28:01  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/end0r822yhsukokp>
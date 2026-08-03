# rabbitmq操作命令

#  查看rabbitmq状态
 kubectl <font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">exec-it</font> rabbitmq-cluster-msg-0 <font style="color:rgb(0, 0, 0);background-color:rgba(0, 0, 0, 0);">-n</font> middleware -- rabbitmqctl status  

# 部署生产mq,从别的地方导入的数据，账号密码跟生产的设置不一致，需要手动修改密码 
```plain
kubectl -n middleware exec -it rabbitmq-0 -- /bin/bash
```

```plain
I have no name!@rabbitmq-0:/$ rabbitmqctl list_users
Listing users ...
user    tags
admin   [administrator]
user    [administrator]
guest   [administrator]
（rabbitmq有三个内置用户）
```



```plain
rabbitmqctl change_password admin tS9bS2yX4pU2aH8jS9iC
Changing password for user "admin"
```



> 更新: 2026-02-14 14:55:16  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/nubcbu52ctoc8cp4>
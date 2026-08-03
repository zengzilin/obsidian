# GCP在线扩容pvc命令

kubectl patch pvc rabbitmq-cluster-0 -n middleware -p '{"spec":{"resources":{"requests":{"storage":"10Gi"}}}}'



> 更新: 2026-02-14 23:08:48  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/bydmqnx9r0qmoaf7>
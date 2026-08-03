# k8s部署redis cluster一直不通

在oracle云上redis集群突然挂了



一直重装都不成功

跨节点网络不通。

但是没有设置firewall规则，



根因：

oracle k8s集群网络有问题，但是是DNS有问题

最后解决方法：

重启coredns和flannel、kubeproxy 服务pod，重启完之后网络通信正常，



k8s网络相关的，不要忘了查coredns



> 更新: 2024-10-15 16:15:58  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/auasgqloyzxuiigl>
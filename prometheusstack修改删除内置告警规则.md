# prometheus stack修改 删除内置告警规则

# 使用 prometheus stack安装监控后，默认会生成一些集群内部的 prometheus rule
## 如果要删除 InfoInhibitor 和 Watchdog   的告警
就要删除prometheus-kube-prometheus-general.rules

这条规则配置的对应alert规则



## 如果要删除KubeVersionMismatch这个告警
就要删除prometheus-kube-prometheus-kubernetes-system这条规则配置的对应alert规则



> 更新: 2024-07-09 18:24:32  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/xvimipg31vzwh6zr>
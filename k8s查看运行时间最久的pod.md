# k8s查看运行时间最久的pod

kubectl get pods --all-namespaces -o wide | sort -k5 | awk 'NR==1{print $1,$2,$6}'



tips: RN==1表示选取排序后的第一个pod



> 更新: 2024-08-30 15:06:58  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/gw75hw6wz2nwzlnk>
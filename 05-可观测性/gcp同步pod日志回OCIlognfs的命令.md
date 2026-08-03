# gcp同步pod日志回OCI log nfs的命令

# 第一步mgr绑定的gcp nfs


**kubectl apply -f pvc.yaml**

**helm install dockermanagement ./deploy/ -f ./deploy/values.yaml  -n mgr**

# 第二步手动同步回gcp nfs
 for pod in $(kubectl get po -n mgr -o name | cut -d'/' -f2); do   echo "Executing command in pod: $pod";   kubectl exec -n mgr $pod --  sh  /dockermanagement/root/shell/dockerRsync.sh; done



# 第三步
 执行同步rclone脚本



# 


> 更新: 2025-11-18 11:58:55  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/uwdma1qy82cur0tr>
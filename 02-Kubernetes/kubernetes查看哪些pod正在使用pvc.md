# kubernetes 查看哪些 pod 正在使用 pvc

 kubectl get pods -n monitoring -o=json | jq -c '.items[] | {name: .metadata.name, namespace: .metadata.namespace, claimName:.spec.volumes[] | select( has ("persistentVolumeClaim") ).persistentVolumeClaim.claimName }'





> 更新: 2025-07-31 12:53:57  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/tmhhsv3a6l8kup61>
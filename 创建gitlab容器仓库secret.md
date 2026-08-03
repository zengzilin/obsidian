# 创建gitlab 容器仓库secret

kubectl -n $1 create secret docker-registry gitlab-registry \

  --docker-server=[http://kw-prod-git.tiqmopaymentkuwait.com:5050](http://kw-prod-git.tiqmopaymentkuwait.com:5050) \

  --docker-username=k8simage \

  --docker-password='uX6uD5zU5t!!' \

  --docker-email=example@example.com



 k8simage/yfw7BQzkqn





> 更新: 2025-07-25 17:34:17  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/pdvy9nnraw4bgah7>
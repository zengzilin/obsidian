# envoy gateway部署和配置

helm pull oci://docker.io/envoyproxy/gateway-helm --version v1.6.1 

helm upgrade --install eg ./gateway-helm   -n envoy-gateway-system   --create-namespace   -f values.yaml



> 更新: 2025-12-16 23:51:57  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/gixggqv7r6nrh1zk>
# GKE gateway controller迁移到envoy gateway



GKE已经提前部署了 gateway api crd

所以要跳过envoy 自带的crd

helm pull oci://docker.io/envoyproxy/gateway-helm --version v1.6.1 --untar

cd gateway-helm/

helm upgrade --install eg .   -n envoy-gateway-system   --create-namespace   --skip-crds



> 更新: 2025-12-12 11:36:14  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/mgefc1a47dgxizbx>
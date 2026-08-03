# 清理redis 容器数据

for i in {0..5}; do kubectl exec -n test-ksa-middleware redis-cluster-new-$i -- redis-cli FLUSHALL;  done 



> 更新: 2025-06-06 20:27:10  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/xgmnv83wi20np0ac>
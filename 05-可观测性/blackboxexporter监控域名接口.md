# blackbox exporter监控域名接口



# blackbox安装
helm repo add prometheus-community [https://prometheus-community.github.io/helm-charts](https://prometheus-community.github.io/helm-charts)

helm install my-prometheus-blackbox-exporter prometheus-community/prometheus-blackbox-exporter --version 11.4.1

# prometheus配置
```plain
 - job_name: blackbox-exporter
      metrics_path: /probe  # Blackbox 暴露指标的路径
      params:
        module: [http_2xx]  # 关联 Blackbox 中的 http_2xx 模块
      static_configs:
      - targets:
          - https://kw-preprod-wallet-api.tiqmopaymentkuwait.com/sw/app/3032
      relabel_configs:
        - source_labels: [__address__]
          target_label: __param_target  # 将目标域名传给 Blackbox 的 target 参数
        - source_labels: [__param_target]
          target_label: instance  # 在指标中显示目标域名
        - target_label: __address__
          replacement: prometheus-blackbox-exporter.monitoring:9115
```





> 更新: 2025-10-27 21:08:54  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/kfr8fhix0w6u6ybc>
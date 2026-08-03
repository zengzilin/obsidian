# click to deploy 启用mtls

:::info
apiVersion: apps/v1

kind: StatefulSet

metadata:

  name: rabbitmq-1-rabbitmq

spec:

  template:

    spec:

      # 挂载 secret 作为 volume

      volumes:

        - name: rabbitmq-tls

          secret:

            secretName: rabbitmq-tls



      containers:

        - name: rabbitmq

          volumeMounts:

            - name: rabbitmq-tls

              mountPath: /etc/rabbitmq/certs

              readOnly: true

        # 如果 init 容器也需要访问证书 (根据你的 initContainer 脚本是否用到)

        - name: copy-rabbitmq-config

          volumeMounts:

            - name: rabbitmq-tls

              mountPath: /etc/rabbitmq/certs

              readOnly: true

:::





> 更新: 2025-11-20 16:18:23  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/hlfvwtn33ybz9gpe>
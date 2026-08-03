# nacos更新配置报错

[wftapp@kubespray nacos-2.5-extra-config-new]$ helm upgrade nacos ./ -f values-dev.yaml -n middleware-new

Error: UPGRADE FAILED: Unable to continue with update: ConfigMap "nacos-application-properties" in namespace "middleware-new" exists and cannot be imported into the current release: invalid ownership metadata; label validation error: missing key "app.kubernetes.io/managed-by": must be set to "Helm"; annotation validation error: missing key "meta.helm.sh/release-name": must be set to "nacos"; annotation validation error: missing key "meta.helm.sh/release-namespace": must be set to "middleware-new"

[wftapp@kubespray nacos-2.5-extra-config-new]$ helm upgrade nacos ./ -f values-dev.yaml -n middleware-new^C



### <font style="color:rgb(0, 0, 0);">方法一：删除现有 ConfigMap（不推荐，可能导致数据丢失）</font>
<font style="color:rgb(28, 31, 35);">kubectl delete configmap nacos-application-properties -n middleware-new</font>

<font style="color:rgb(28, 31, 35);">helm upgrade nacos ./ -f values-dev.yaml -n middleware-new</font>

<font style="color:rgb(28, 31, 35);"></font>

### <font style="color:rgb(0, 0, 0);">方法二：为现有 ConfigMap 添加 Helm 标签和注解（推荐）</font>
<font style="color:rgb(28, 31, 35);">  
</font><font style="color:rgb(28, 31, 35);"> kubectl patch configmap nacos-application-properties -n middleware-new --patch ' metadata: labels: app.kubernetes.io/managed-by: "Helm" annotations: meta.helm.sh/release-name: "nacos" meta.helm.sh/release-namespace: "middleware-new" '</font>

<font style="color:rgb(28, 31, 35);"></font>

<font style="color:rgb(28, 31, 35);">helm upgrade nacos ./ -f values-dev.yaml -n middleware-new</font>

<font style="color:rgb(28, 31, 35);"></font>

<font style="color:rgb(28, 31, 35);"></font>

**<font style="color:#DF2A3F;">注意 配置更新之后，需要重启nacos pods，才能真正生效</font>**



> 更新: 2025-05-26 17:12:09  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/vnwmn4kcaomgre9d>
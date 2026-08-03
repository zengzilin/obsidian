# k8s集群接入spinnaker报错

<font style="color:rgba(0, 0, 0, 0.85);background-color:rgba(0, 0, 0, 0.04);">Resource: "spinnaker.io/v1alpha2, Resource=spinnakerservices", GroupVersionKind: "spinnaker.io/v1alpha2, Kind=SpinnakerService" Name: "spinnaker", Namespace: "spinnaker" for: "STDIN": error when patching "STDIN": admission webhook "webhook-spinnakerservices-v1alpha2.spinnaker.io" denied the request: SpinnakerService validation failed: Validator for account 'finance-uat' detected an error: error building rest config from kubeconfigFile: context "kubernetes-admin@kubernetes" does not exist</font>

<font style="color:rgba(0, 0, 0, 0.85);background-color:rgba(0, 0, 0, 0.04);"></font>

### <font style="color:rgb(0, 0, 0);">一、核心报错分析</font>

<font style="color:rgba(0, 0, 0, 0.85) !important;">当前 Spinnaker 部署失败的</font>**<font style="color:rgb(0, 0, 0) !important;">直接原因</font>**<font style="color:rgba(0, 0, 0, 0.85) !important;">是：</font><code><font style="color:rgba(0, 0, 0, 0.85) !important;">admission webhook</font></code><font style="color:rgba(0, 0, 0, 0.85) !important;">拒绝了请求，因为</font><code><font style="color:rgba(0, 0, 0, 0.85) !important;">finance-uat</font></code><font style="color:rgba(0, 0, 0, 0.85) !important;">账号的验证器检测到</font><code><font style="color:rgba(0, 0, 0, 0.85) !important;">kubeconfig</font></code><font style="color:rgba(0, 0, 0, 0.85) !important;">配置错误 ——</font>**<font style="color:rgb(0, 0, 0) !important;">无法找到名为 “kubernetes-admin@kubernetes” 的 context</font>**<font style="color:rgba(0, 0, 0, 0.85) !important;">。</font>

### <font style="color:rgb(0, 0, 0);">二、错误根源定位</font>

<font style="color:rgba(0, 0, 0, 0.85) !important;">报错关联的是</font><code><font style="color:rgba(0, 0, 0, 0.85) !important;">spec.spinnakerConfig.files</font></code><font style="color:rgba(0, 0, 0, 0.85) !important;">中的</font><code><font style="color:rgba(0, 0, 0, 0.85) !important;">kubeconfig-finance-uat</font></code><font style="color:rgba(0, 0, 0, 0.85) !important;">文件（因报错明确指向 “finance-uat” 账号），该文件的关键配置与期望的</font><code><font style="color:rgba(0, 0, 0, 0.85) !important;">context</font></code><font style="color:rgba(0, 0, 0, 0.85) !important;">不匹配：</font>

<font style="color:rgba(0, 0, 0, 0.85);background-color:rgba(0, 0, 0, 0.04);">  
</font>

| **<font style="color:rgb(0, 0, 0) !important;">配置项</font>** | <code>**<font style="color:rgb(0, 0, 0);">kubeconfig-finance-uat</font>**</code><br/>**<font style="color:rgb(0, 0, 0) !important;">实际内容</font>** | **<font style="color:rgb(0, 0, 0) !important;">报错期望内容</font>** | **<font style="color:rgb(0, 0, 0) !important;">不匹配点</font>** |
| :--- | :--- | :--- | :--- |
| <code><font style="color:rgb(0, 0, 0);">contexts[0].name</font></code> | <code><font style="color:rgb(0, 0, 0);">internal</font></code> | <code><font style="color:rgb(0, 0, 0);">kubernetes-admin@kubernetes</font></code> | <font style="color:rgba(0, 0, 0, 0.85) !important;">context 名称不一致</font> |
| <code><font style="color:rgb(0, 0, 0);">current-context</font></code> | <code><font style="color:rgb(0, 0, 0);">internal</font></code> | <code><font style="color:rgb(0, 0, 0);">kubernetes-admin@kubernetes</font></code> | <font style="color:rgba(0, 0, 0, 0.85) !important;">当前激活的 context 不一致</font> |
| <code><font style="color:rgb(0, 0, 0);">clusters[0].name</font></code> | <code><font style="color:rgb(0, 0, 0);">internalCluster</font></code> | <font style="color:rgba(0, 0, 0, 0.85) !important;">未明确要求，但需与 context 关联</font> | <font style="color:rgba(0, 0, 0, 0.85) !important;">集群名称与期望 context 无关联</font> |

### <font style="color:rgb(0, 0, 0);">三、解决方案</font>

<font style="color:rgba(0, 0, 0, 0.85) !important;">需修改</font><code><font style="color:rgba(0, 0, 0, 0.85) !important;">kubeconfig-finance-uat</font></code><font style="color:rgba(0, 0, 0, 0.85) !important;">文件，确保</font><code><font style="color:rgba(0, 0, 0, 0.85) !important;">context</font></code><font style="color:rgba(0, 0, 0, 0.85) !important;">配置与 Spinnaker 期望的 “kubernetes-admin@kubernetes” 匹配，步骤如下：</font>

<font style="color:rgba(0, 0, 0, 0.85);background-color:rgba(0, 0, 0, 0.04);">  
</font>

1. **<font style="color:rgb(0, 0, 0) !important;">调整</font>**<code>**<font style="color:rgb(0, 0, 0);">kubeconfig-finance-uat</font>**</code>**<font style="color:rgb(0, 0, 0) !important;">的 context 配置</font>**<font style="color:rgba(0, 0, 0, 0.85) !important;">：\ </font><font style="color:rgba(0, 0, 0, 0.85) !important;">将文件中的</font><code><font style="color:rgb(0, 0, 0);">contexts</font></code><font style="color:rgba(0, 0, 0, 0.85) !important;">和</font><code><font style="color:rgb(0, 0, 0);">current-context</font></code><font style="color:rgba(0, 0, 0, 0.85) !important;">修改为报错期望的名称，示例如下：</font>**<font style="color:rgba(0, 0, 0, 0.85);">yaml</font>**

```yaml
contexts:
- context:
    cluster: internalCluster  # 保持与已有cluster名称一致（或改为"kubernetes"，需确保cluster配置存在）
    user: user                # 保持与已有user名称一致
  name: kubernetes-admin@kubernetes  # 改为报错期望的context名称
current-context: kubernetes-admin@kubernetes  # 激活上述context
```


> 更新: 2025-08-21 20:35:49  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/if8qc8xzysffswnn>
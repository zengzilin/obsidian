# GKE集群升级到1.32版本之后,ingress controller报错



# ingress controller报错没有资源权限
![1749694769532-95e7589e-5c57-4cf4-8d7a-b24abaff7045.png](./img/mU6vMZc05kBIVMER/1749694769532-95e7589e-5c57-4cf4-8d7a-b24abaff7045-250763.png)



权限检测命令

kubectl get clusterrolebinding -o yaml | grep -A5 ingress-nginx

kubectl auth can-i list secrets --as=system:serviceaccount:ingress-nginx:ingress-nginx

![1749695145242-0bc9e1f9-b1b3-4b59-9aa9-fc189b336fcf.png](./img/mU6vMZc05kBIVMER/1749695145242-0bc9e1f9-b1b3-4b59-9aa9-fc189b336fcf-251526.png)

没有自动创建clusterrolebinding  ingress-nginx，serviceaccount报没权限， 可能是版本不兼容，Gemini AI建议升级ingress

# 重用配置升级controller
helm upgrade ingress-nginx ingress-nginx/ingress-nginx -n ingress-nginx --reuse-values



**<font style="color:#DF2A3F;">升级后恢复正常</font>**



> 更新: 2025-06-12 14:48:52  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/ok4dg5e0b13vt1tk>
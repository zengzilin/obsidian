# 修改配置重装calico

#  kubespray部署的1.31版本老是报DNS解析超时,redisk8s域名解析失败
https://github.com/kubernetes/kubernetes/issues/131396 "it was confirmed that the issue was caused by the checksum offload feature in Calico 3.28. After disabling this feature, normal communication was restored. ",然后我更新了calico，新增参数calico_checksum_offload: false，**<font style="color:#DF2A3F;">但是我没发现配置有更新！！</font>**

**<font style="color:#DF2A3F;">因为kubspray 2.27版本不支持从变量修改</font>**

**所以直接修改calico jinja2部署模板，手动新增**

FELIX_CHECKSUMOFFLOADBROKEN 变量，据说是等价于 calico_checksum_offload: false

```plain
vim roles/network_plugin/calico/templates/calico-node.yml.j2
 env:
            # 新增 FELIX_CHECKSUMOFFLOADBROKEN 环境变量
            # 在 FelixConfiguration 中设置 checksumOffloadDisabled: true
            - name: FELIX_CHECKSUMOFFLOADBROKEN
              value: "true"
```





# 重新部署 calico
ansible-playbook \

  -i inventory/tiqmo-dev/inventory.ini \

  cluster.yml \

  --tags calico \

  --limit kube_node,kube_control_plane



 ansible-playbook -i inventory/tiqmo-dev/inventory.ini  cluster.yml  --tags calico -b --limit kube_node,kube_control_plane



[https://kubespray.io/#/docs/ansible/ansible?id=ansible-tags](https://kubespray.io/#/docs/ansible/ansible?id=ansible-tags)



> 更新: 2026-02-07 12:30:05  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/lvegqyedoik9b3du>
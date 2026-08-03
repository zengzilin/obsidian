# 深圳与tiqmo互通的网络方案

# 原方案

深圳IDC(192.168.0.0/16)--德国阿里云VPN->阿里云深圳(10.69.0.0/16)--云企业网->阿里云德国法兰克福(10.77.0.0/16)-阿里云VPN-->客户比利时 gitlab(10.42.103.136/32)

深圳IDC(192.168.0.0/16)--沙特利雅得阿里云VPN->阿里云深圳(10.69.0.0/16)--云企业网->阿里云沙特利雅得(10.75.0.0/16)-阿里云VPN-->客户沙特gitlab(10.10.1.197/32)

![1764316754288-ac2ace9c-bd3e-45a2-8b9d-fe3565bde973.png](./img/uRjzxDPwe8lrxjDU/1764316754288-ac2ace9c-bd3e-45a2-8b9d-fe3565bde973-588668.png)

# 新方案

深圳IDC-深圳云上VPN(VPC)-TR链接-tiqmo CEN->-跨境带宽包-德国阿里云ipsec VPN-德国VPC-德国Tiqmo gitlab

深圳IDC-深圳云上VPN(VPC)-TR链接-tiqmo CEN->-跨境带宽包-沙特阿里云ipsec VPN-沙特VPC-沙特Tiqmo gitlab

## 在Tiqmo CEN创建转发路由

![1764325957077-69e46b49-54d5-4f94-9271-b037557deb67.png](./img/uRjzxDPwe8lrxjDU/1764325957077-69e46b49-54d5-4f94-9271-b037557deb67-163322.png)

创建地域内连接

![1764324732158-8c3368e7-3c73-4aa8-a97d-f04c4bf74499.png](./img/uRjzxDPwe8lrxjDU/1764324732158-8c3368e7-3c73-4aa8-a97d-f04c4bf74499-130348.png)

![1764325888389-279d576c-6bdc-4477-b52b-9a87215058a8.png](./img/uRjzxDPwe8lrxjDU/1764325888389-279d576c-6bdc-4477-b52b-9a87215058a8-352712.png)

关闭自动路由学习

将深圳的VPC加入到原来Tiqmo的CEN

![1764324234508-1c5678a1-6cb0-457f-aa20-7fcadd81afcb.png](./img/uRjzxDPwe8lrxjDU/1764324234508-1c5678a1-6cb0-457f-aa20-7fcadd81afcb-569330.png)

## 在深圳CEN转发路由表添加静态路由

![1764326089742-dd572eef-2a0c-42f9-b4d2-44eab0e9e4a6.png](./img/uRjzxDPwe8lrxjDU/1764326089742-dd572eef-2a0c-42f9-b4d2-44eab0e9e4a6-387800.png)

**添加的是静态路由！！**

目标网段<font style="color:rgb(51, 51, 51);background-color:rgb(250, 250, 250);">192.168.4.48/32</font>

**下次还想跟别的网段通信，比如4.135,需要在同一个地方再添加一个静态路由：**

![1764559458291-e816de2e-0784-4615-9ba4-a3ebdecfb959.png](./img/uRjzxDPwe8lrxjDU/1764559458291-e816de2e-0784-4615-9ba4-a3ebdecfb959-948110.png)

**添加之后，在tiqmo  CEN的转发路由表就会自动学习到**

![1764559654180-5c262797-f24f-4a6a-8b15-689bbb7f7b64.png](./img/uRjzxDPwe8lrxjDU/1764559654180-5c262797-f24f-4a6a-8b15-689bbb7f7b64-105463.png)

## 深圳vpn创建路由

在深圳VPN创建策略路由

目的是跟ipsec打通

![1764560461821-67030352-918f-4652-9a91-5e9f8e11db4e.png](./img/uRjzxDPwe8lrxjDU/1764560461821-67030352-918f-4652-9a91-5e9f8e11db4e-400527.png)

<font style="color:#DF2A3F;">添加策略路由后不要发布！！会导致公司oa访问不了外网！！</font>

德国有两个地址，所以用/24

```plain
（源网段）10.77.0.0/24>192.168.0.0/16 （目标）不要发布！
```

沙特只有一个环境地址，所以用/32

| `plain （源网段）10.75.0.169/32-->192.168.0.0/16 （目标网段）不要发布！ `  | |
| --- | --- |

创建目的路由

机房到vpn

![1764326918034-569699e5-589c-4832-b36d-43aace5b33d2.png](./img/uRjzxDPwe8lrxjDU/1764326918034-569699e5-589c-4832-b36d-43aace5b33d2-729695.png)

## 深圳vpc的路由表创建自定义路由

进入vpc

![1764327031462-90d82415-b174-4e1d-97af-28b58a1018cb.png](./img/uRjzxDPwe8lrxjDU/1764327031462-90d82415-b174-4e1d-97af-28b58a1018cb-260728.png)

打开资源管理的路由表

![1764327084990-1e0ae369-502a-47f8-8ee5-b14013131284.png](./img/uRjzxDPwe8lrxjDU/1764327084990-1e0ae369-502a-47f8-8ee5-b14013131284-916087.png)

点进去

![1764328283621-239d9b8f-f4c4-464c-9c02-e2d4aae86b1b.png](./img/uRjzxDPwe8lrxjDU/1764328283621-239d9b8f-f4c4-464c-9c02-e2d4aae86b1b-643912.png)

转到自定义路由条目

![1764328562947-66a0e746-ceb0-4d78-8254-2ecc704ba091.png](./img/uRjzxDPwe8lrxjDU/1764328562947-66a0e746-ceb0-4d78-8254-2ecc704ba091-286007.png)

```



创建深圳vpn到沙特vpc的自定义路由

![1764561080200-57e39aa1-7bf8-455c-b52c-6659598d42d8.png](./img/uRjzxDPwe8lrxjDU/1764561080200-57e39aa1-7bf8-455c-b52c-6659598d42d8-138804.png)

创建深圳vpn到德国vpc的自定义路由

![1764561116654-a9728dd4-3d1f-4f36-8732-d67e1cb6079c.png](./img/uRjzxDPwe8lrxjDU/1764561116654-a9728dd4-3d1f-4f36-8732-d67e1cb6079c-340990.png)

<font style="color:#000000;">路由器类型选择: </font><font style="color:#DF2A3F;">转发路由器，目标网段选vpc网段!!</font>

![1764328505700-3d21938d-fc41-4afe-8f35-40ad1e331d1a.png](./img/uRjzxDPwe8lrxjDU/1764328505700-3d21938d-fc41-4afe-8f35-40ad1e331d1a-563344.png)

沙特同理

![1764328779912-2be1ecec-e9c8-402b-b577-a5498fc8b369.png](./img/uRjzxDPwe8lrxjDU/1764328779912-2be1ecec-e9c8-402b-b577-a5498fc8b369-203158.png)



## 在深圳VPN下分别创建沙特和德国的Ipsec连接


![1764327289216-949881b6-29bd-41bd-a472-15fd7671743c.png](./img/uRjzxDPwe8lrxjDU/1764327289216-949881b6-29bd-41bd-a472-15fd7671743c-726657.png)

深圳到德国VPC

<font style="color:#000000;">本端网段和目标网段不要搞反：</font>

<font style="color:#DF2A3F;">本端网段填vpc网段，目标网段填机房网段！！！</font>

![1764327437359-4d1cb609-5f5c-4d00-8596-b976efc1ad8e.png](./img/uRjzxDPwe8lrxjDU/1764327437359-4d1cb609-5f5c-4d00-8596-b976efc1ad8e-253406.png)



共享密钥、认证算法、加密算法配置要跟公司的交换机设备保持一致！！

![1764327546991-605feb08-9c3a-4d6a-a965-862684ba05c5.png](./img/uRjzxDPwe8lrxjDU/1764327546991-605feb08-9c3a-4d6a-a965-862684ba05c5-414128.png)

![1764327629364-770f82f1-e547-43ec-a0d2-2a62567ea0cb.png](./img/uRjzxDPwe8lrxjDU/1764327629364-770f82f1-e547-43ec-a0d2-2a62567ea0cb-316347.png)

![1764327815707-6560dc3f-3ad7-483c-8af5-869feffa7bc6.png](./img/uRjzxDPwe8lrxjDU/1764327815707-6560dc3f-3ad7-483c-8af5-869feffa7bc6-828087.png)

<font style="color:#DF2A3F;">要把localId 120.78.65.230 地址和预共享密钥给到企业IT！</font>

remoteId地址是公司的公网地址

![1764327919345-e0362700-8455-44c5-b793-c3cb9d01df6a.png](./img/uRjzxDPwe8lrxjDU/1764327919345-e0362700-8455-44c5-b793-c3cb9d01df6a-909498.png)

沙特同理

![1764327668584-4d72e6bd-04ee-466c-9e1d-54ecc258a14a.png](./img/uRjzxDPwe8lrxjDU/1764327668584-4d72e6bd-04ee-466c-9e1d-54ecc258a14a-420675.png)

![1764327712143-282c9c24-9812-4520-86d0-9c42a858db94.png](./img/uRjzxDPwe8lrxjDU/1764327712143-282c9c24-9812-4520-86d0-9c42a858db94-994768.png)





# 在云上与客户的vpn下创建ipsec
![1768994919300-9eba905e-c9bd-4e59-b5a4-0414c738bf94.png](./img/uRjzxDPwe8lrxjDU/1768994919300-9eba905e-c9bd-4e59-b5a4-0414c738bf94-500088.png)

<font style="color:#DF2A3F;">如果客户换了ip也要记得改这里 不要忘记！！1</font>

<font style="color:#DF2A3F;"></font>

# 在云上与客户的vpn下创建用户网关


# 在云上与客户的vpn下创建自定义路由


  


```
# 新增深圳harbor新地址
## 在tiqmo企业网深圳tr添加回程路由地址


![[Pasted image 20260512103238.png|697]]

![[Pasted image 20260512103346.png|697]]
但是添加之后从192.168.4.239去访问沙特gitlab可以通
去访问德国gitlab却不通。
原因：沙特的vpc已经自动添加路由地址192.168.4.239
![[Pasted image 20260512104604.png]]
德国的vpc路由需要添加自定义路由地址192.168.4.239
![[Pasted image 20260512103848.png]]
![[Pasted image 20260512104031.png]]

![[Pasted image 20260512104325.png]]
更新: 2026-01-21 19:30:28  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/ksha4gv0f9p5g34z>
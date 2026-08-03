# logstash报错

![1750939540551-d557c0d5-210d-41b5-8112-29f2c3db8453.png](./img/ulf66YlReMbCaQD2/1750939540551-d557c0d5-210d-41b5-8112-29f2c3db8453-554009.png)

<font style="color:#DF2A3F;">关键错误信息 wallet index 文档数超大，超大</font>

# <font style="color:#DF2A3F;">解决方案</font>
1.设置文档数阈值，到达10亿文档数之后滚动创建一个新的index

:::info
PUT _ilm/policy/logs-svrlog-wallet-policy

{

  "policy": {

    "phases": {

      "hot": {

        "actions": {

          "rollover": {

            "max_docs": 1000000000  // 文档数达到10亿时滚动

          }

        }

      }

    }

  }

}

:::



2.上一步设置完之后，旧的索引还是很大，所以手动触发滚动

```json
# 手动触发当前索引滚动（创建新索引）
POST .ds-logs-svrlog-wallet-*/_rollover
```





> 更新: 2025-06-26 20:11:57  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/oxs4xp598gc67i4g>
# kubespray 扩容报错

TASK \[kubernetes/preinstall : Check /usr readonly] \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

ok: \[node9]

Sunday 27 April 2025 09:52:13 +0800 (0:00:00.160) 0:00:17.382 \*\*\*\*\*\*\*\*\*\*

Sunday 27 April 2025 09:52:13 +0800 (0:00:00.010) 0:00:17.393 \*\*\*\*\*\*\*\*\*\*

ansible-playbook -i inventory/tiqmo-dev/inventory.ini scale.yml -b -l node9

TASK \[kubernetes/preinstall : Stop if any host not in '--limit' does not have a fact cache] \*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*\*

fatal: \[node9]: FAILED! => {

"assertion": "uncached\_hosts | intersect(excluded\_hosts) == \[]",

"changed": false,

"evaluated\_to": false,

"msg": "Kubespray does not support '--limit' without a populated facts cache for the excluded hosts.\nPlease run the facts.yml playbook first without '--limit'.\nThe following excluded hosts are not cached: \['node2', 'node6', 'node3', 'node8', 'node7', 'node5', 'node1', 'node4']\n"

}

ansible-playbook -i inventory/tiqmo-dev/inventory.ini  scale.yml  -b -l node9

### <font style="color:rgba(0, 0, 0, 0.9);">问题分析与解决方案</font>

#### <font style="color:rgba(0, 0, 0, 0.9);">1.</font><font style="color:rgba(0, 0, 0, 0.9);"> </font>**<font style="color:rgba(0, 0, 0, 0.9);">错误根源</font>**

<font style="color:rgba(0, 0, 0, 0.9);">您在运行</font><font style="color:rgba(0, 0, 0, 0.9);"> </font><code><font style="color:rgba(0, 0, 0, 0.9);">scale.yml</font></code><font style="color:rgba(0, 0, 0, 0.9);"> </font><font style="color:rgba(0, 0, 0, 0.9);">时使用了</font><font style="color:rgba(0, 0, 0, 0.9);"> </font><code><font style="color:rgba(0, 0, 0, 0.9);">--limit node9</font></code><font style="color:rgba(0, 0, 0, 0.9);">，但其他节点（</font><code><font style="color:rgba(0, 0, 0, 0.9);">node1</font></code><font style="color:rgba(0, 0, 0, 0.9);"> </font><font style="color:rgba(0, 0, 0, 0.9);">到</font><font style="color:rgba(0, 0, 0, 0.9);"> </font><code><font style="color:rgba(0, 0, 0, 0.9);">node8</font></code><font style="color:rgba(0, 0, 0, 0.9);">）的 Ansible 事实缓存未生成。\ </font><font style="color:rgba(0, 0, 0, 0.9);">Kubespray 要求在使用</font><font style="color:rgba(0, 0, 0, 0.9);"> </font><code><font style="color:rgba(0, 0, 0, 0.9);">--limit</font></code><font style="color:rgba(0, 0, 0, 0.9);"> </font><font style="color:rgba(0, 0, 0, 0.9);">限制执行节点时，</font>**<font style="color:rgba(0, 0, 0, 0.9);">所有未被包含的节点</font>**<font style="color:rgba(0, 0, 0, 0.9);">（即排除的节点）必须已存在事实缓存（通过</font><font style="color:rgba(0, 0, 0, 0.9);"> </font><code><font style="color:rgba(0, 0, 0, 0.9);">facts.yml</font></code><font style="color:rgba(0, 0, 0, 0.9);"> </font><font style="color:rgba(0, 0, 0, 0.9);">生成），否则会触发此断言错误。</font>

***

#### <font style="color:rgba(0, 0, 0, 0.9);">2.</font><font style="color:rgba(0, 0, 0, 0.9);"> </font>**<font style="color:rgba(0, 0, 0, 0.9);">直接解决方案</font>**

<font style="color:rgba(0, 0, 0, 0.9);">根据错误提示，需先运行 </font><code><font style="color:rgba(0, 0, 0, 0.9);">facts.yml</font></code><font style="color:rgba(0, 0, 0, 0.9);"> </font>**<font style="color:rgba(0, 0, 0, 0.9);">完整收集所有节点的事实缓存</font>**<font style="color:rgba(0, 0, 0, 0.9);">，再执行 </font><code><font style="color:rgba(0, 0, 0, 0.9);">scale.yml</font></code><font style="color:rgba(0, 0, 0, 0.9);"> ：</font>

ansible-playbook -i inventory/tiqmo-dev/inventory.ini  playbooks/facts.yml -b


> 更新: 2025-04-27 09:59:16  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/xt0hh2vhrq5gsn0z>
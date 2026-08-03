# 以非root用户运行容器无法创建并运行定时任务

### **<font style="color:rgb(6, 10, 38);">真相：是谁在跑你的定时任务？</font>**

<font style="color:rgb(6, 10, 38);">当你以普通用户执行</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">crontab -l</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">看到任务时，</font>**<font style="color:rgb(6, 10, 38);">真正在后台每分钟唤醒并执行你脚本的，依然是那个由 Root 用户启动的系统级</font>\*\*\*\*<font style="color:rgb(6, 10, 38);"> </font>**<code>**<font style="color:rgb(6, 10, 38);">crond</font>**</code>**<font style="color:rgb(6, 10, 38);"> </font>\*\*\*\*<font style="color:rgb(6, 10, 38);">服务！</font>**

#### **<font style="color:rgb(6, 10, 38);">1. 架构解析</font>**

<font style="color:rgb(6, 10, 38);">Linux 的 Cron 架构是</font><font style="color:rgb(6, 10, 38);"> </font>**<font style="color:rgb(6, 10, 38);">C/S (客户端/服务器)</font>**<font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">模式：</font>

* **<font style="color:rgb(6, 10, 38);">服务端 (Server)</font>**<font style="color:rgb(6, 10, 38);">:</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">/usr/sbin/crond</font></code><font style="color:rgb(6, 10, 38);">。</font>
  * **<font style="color:rgb(6, 10, 38);">必须由 Root 启动</font>**<font style="color:rgb(6, 10, 38);">。</font>
  * <font style="color:rgb(6, 10, 38);">它一直驻留在内存中（PID 1 或类似）。</font>
  * <font style="color:rgb(6, 10, 38);">它负责读取</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">/var/spool/cron/用户名</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">目录下的所有用户配置文件。</font>
  * <font style="color:rgb(6, 10, 38);">它拥有 Root 权限，所以它能读取任何用户的 crontab 文件。</font>
* **<font style="color:rgb(6, 10, 38);">客户端 (Client)</font>**<font style="color:rgb(6, 10, 38);">:</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">crontab</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">命令。</font>
  * <font style="color:rgb(6, 10, 38);">普通用户可以运行。</font>
  * <font style="color:rgb(6, 10, 38);">它的作用只是</font>**<font style="color:rgb(6, 10, 38);">编辑</font>**<font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">(</font><code><font style="color:rgb(6, 10, 38);">-e</font></code><font style="color:rgb(6, 10, 38);">)、</font>**<font style="color:rgb(6, 10, 38);">列出</font>**<font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">(</font><code><font style="color:rgb(6, 10, 38);">-l</font></code><font style="color:rgb(6, 10, 38);">) 或</font><font style="color:rgb(6, 10, 38);"> </font>**<font style="color:rgb(6, 10, 38);">删除</font>**<font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">(</font><code><font style="color:rgb(6, 10, 38);">-r</font></code><font style="color:rgb(6, 10, 38);">) 存储在</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">/var/spool/cron/用户名</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">里的</font>**<font style="color:rgb(6, 10, 38);">文本文件</font>**<font style="color:rgb(6, 10, 38);">。</font>
  * <font style="color:rgb(6, 10, 38);">它</font>**<font style="color:rgb(6, 10, 38);">不负责调度</font>**<font style="color:rgb(6, 10, 38);">，它只是个“记事本”。</font>

#### **<font style="color:rgb(6, 10, 38);">2. 流程还原</font>**

1. **<font style="color:rgb(6, 10, 38);">你 (普通用户)</font>**<font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">运行</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">crontab -e</font></code><font style="color:rgb(6, 10, 38);">。</font>
   * <code><font style="color:rgb(6, 10, 38);">crontab</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">程序把你的配置保存到了</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">/var/spool/cron/user</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">文件中。</font>
2. **<font style="color:rgb(6, 10, 38);">系统 (Root 用户)</font>**<font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">运行的</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">/usr/sbin/crond</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">守护进程。</font>
   * <font style="color:rgb(6, 10, 38);">它每分钟醒来一次。</font>
   * <font style="color:rgb(6, 10, 38);">它扫描</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">/var/spool/cron/</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">目录。</font>
   * <font style="color:rgb(6, 10, 38);">它发现了</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">user</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">这个文件。</font>
   * <font style="color:rgb(6, 10, 38);">它读取内容：</font><code><font style="color:rgb(6, 10, 38);">* * * * * sh test.sh</font></code><font style="color:rgb(6, 10, 38);">。</font>
   * <font style="color:rgb(6, 10, 38);">它调用</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">fork()</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">+</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">setuid(user)</font></code><font style="color:rgb(6, 10, 38);">，</font>**<font style="color:rgb(6, 10, 38);">切换成你的身份</font>**<font style="color:rgb(6, 10, 38);">去执行</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">sh test.sh</font></code><font style="color:rgb(6, 10, 38);">。</font>

**<font style="color:rgb(6, 10, 38);">结论：</font>**<font style="color:rgb(6, 10, 38);">\ </font><font style="color:rgb(6, 10, 38);">你能跑通定时任务，是因为</font>**<font style="color:rgb(6, 10, 38);">你的操作系统里已经有一个 Root 用户在运行</font>\*\*\*\*<font style="color:rgb(6, 10, 38);"> </font>**<code>**<font style="color:rgb(6, 10, 38);">crond</font>**</code>**<font style="color:rgb(6, 10, 38);"> </font>\*\*\*\*<font style="color:rgb(6, 10, 38);">服务了</font>**<font style="color:rgb(6, 10, 38);">（通常是系统开机自启的）。</font><font style="color:rgb(6, 10, 38);">\ </font>**<font style="color:rgb(6, 10, 38);">并不是</font>**<font style="color:rgb(6, 10, 38);">因为你以普通用户身份启动了</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">crond</font></code><font style="color:rgb(6, 10, 38);">。</font>

***

### **<font style="color:rgb(6, 10, 38);">🚫</font>\*\*\*\*<font style="color:rgb(6, 10, 38);"> 为什么在 Kubernetes Pod 里这招行不通？</font>**

<font style="color:rgb(6, 10, 38);">这就是问题的关键所在！</font>

#### **<font style="color:rgb(6, 10, 38);">场景 A：你的物理机/虚拟机 (RHEL 8)</font>**

* <font style="color:rgb(6, 10, 38);">系统启动时，</font><code><font style="color:rgb(6, 10, 38);">systemd</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">以</font><font style="color:rgb(6, 10, 38);"> </font>**<font style="color:rgb(6, 10, 38);">Root</font>**<font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">身份启动了</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">/usr/sbin/crond</font></code><font style="color:rgb(6, 10, 38);">。</font>
* <font style="color:rgb(6, 10, 38);">所以，即使你登录的是普通用户，后台也有个 Root 版的</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">crond</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">在伺候你。</font>
* **<font style="color:rgb(6, 10, 38);">结果</font>**<font style="color:rgb(6, 10, 38);">：</font><code><font style="color:rgb(6, 10, 38);">crontab -l</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">有效，任务能跑。</font>

#### **<font style="color:rgb(6, 10, 38);">场景 B：Kubernetes Pod (默认情况)</font>**

* <font style="color:rgb(6, 10, 38);">容器启动时，</font>**<font style="color:rgb(6, 10, 38);">只运行你指定的 CMD</font>**<font style="color:rgb(6, 10, 38);">。</font>
* <font style="color:rgb(6, 10, 38);">如果你设置</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">runAsUser: 1001</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">(普通用户)，且 CMD 只是</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">sh test.sh</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">或者</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">while...</font></code><font style="color:rgb(6, 10, 38);">。</font>
* **<font style="color:rgb(6, 10, 38);">此时容器内没有任何其他进程</font>**<font style="color:rgb(6, 10, 38);">。</font>
* **<font style="color:rgb(6, 10, 38);">没有 Root 进程</font>**<font style="color:rgb(6, 10, 38);">在运行</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">/usr/sbin/crond</font></code><font style="color:rgb(6, 10, 38);">。</font>
* <font style="color:rgb(6, 10, 38);">虽然你可以运行</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">crontab -e</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">写入文件到</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">/var/spool/cron/user</font></code><font style="color:rgb(6, 10, 38);">。</font>
* **<font style="color:rgb(6, 10, 38);">但是！</font>**<font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">没有人去读取这个文件！没有守护进程在每分钟检查它！</font>
* **<font style="color:rgb(6, 10, 38);">结果</font>**<font style="color:rgb(6, 10, 38);">：</font><code><font style="color:rgb(6, 10, 38);">crontab -l</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">能看到内容（因为只是读文件），但</font>**<font style="color:rgb(6, 10, 38);">任务永远不会执行</font>**<font style="color:rgb(6, 10, 38);">。</font>

#### **<font style="color:rgb(6, 10, 38);">场景 C：你想在 Pod 里复现物理机的行为</font>**

<font style="color:rgb(6, 10, 38);">你想在 Pod 里也实现“普通用户写 crontab，任务自动跑”。</font>

* <font style="color:rgb(6, 10, 38);">你必须在 Pod 里启动一个</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">/usr/sbin/crond</font></code><font style="color:rgb(6, 10, 38);">。</font>
* <font style="color:rgb(6, 10, 38);">但如前所述，</font><code><font style="color:rgb(6, 10, 38);">/usr/sbin/crond</font></code><font style="color:rgb(6, 10, 38);"> </font>**<font style="color:rgb(6, 10, 38);">拒绝</font>**<font style="color:rgb(6, 10, 38);">由普通用户启动。</font>
* <font style="color:rgb(6, 10, 38);">如果 Pod 强制</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">runAsNonRoot: true</font></code><font style="color:rgb(6, 10, 38);">，K8s 会阻止你以 Root 启动这个进程。</font>
* **<font style="color:rgb(6, 10, 38);">死锁</font>**<font style="color:rgb(6, 10, 38);">：</font>
  * <font style="color:rgb(6, 10, 38);">没 Root -></font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">crond</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">起不来 -> 没人读 crontab -> 任务不跑。</font>
  * <font style="color:rgb(6, 10, 38);">有 Root -> 违反</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">runAsNonRoot</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">策略 (除非你接受 Root 启动进程，但业务降权)。</font>

***

### **<font style="color:rgb(6, 10, 38);">💡</font>\*\*\*\*<font style="color:rgb(6, 10, 38);"> 验证实验 (在 K8s Pod 中)</font>**

<font style="color:rgb(6, 10, 38);">你可以做一个实验来证明我的观点：</font>

1. <font style="color:rgb(6, 10, 38);">部署一个 Pod，</font><code><font style="color:rgb(6, 10, 38);">securityContext.runAsUser: 1001</font></code><font style="color:rgb(6, 10, 38);">。</font>
2. <font style="color:rgb(6, 10, 38);">CMD 设置为</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">tail -f /dev/null</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">(让容器挂着)。</font>
3. <font style="color:rgb(6, 10, 38);">进入容器：</font><code><font style="color:rgb(6, 10, 38);">kubectl exec -it <pod> -- bash</font></code><font style="color:rgb(6, 10, 38);">。</font>
4. <font style="color:rgb(6, 10, 38);">写入任务：</font>**<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">bash</font>**<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">编辑</font>

```plain
echo "* * * * * echo hello >> /tmp/test.log" | crontab -
crontab -l  # 能看到任务
```

5. <font style="color:rgb(6, 10, 38);">等待 2 分钟。</font>
6. <font style="color:rgb(6, 10, 38);">查看日志：</font>**<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">bash</font>**<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">编辑</font>

```plain
cat /tmp/test.log
```

7. **<font style="color:rgb(6, 10, 38);">结果</font>**<font style="color:rgb(6, 10, 38);">：文件</font>**<font style="color:rgb(6, 10, 38);">不存在</font>**<font style="color:rgb(6, 10, 38);">或为空。因为容器里没有</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">crond</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">进程在跑。</font>

<font style="color:rgb(6, 10, 38);">再检查一下进程：</font>

**<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">bash</font>**

<font style="color:rgba(17, 17, 51, 0.7);background-color:rgb(240, 240, 242);">编辑</font>

```plain
ps -ef | grep cron
# 输出：只有 grep 自己，没有 crond 进程。
```

### **<font style="color:rgb(6, 10, 38);">✅</font>\*\*\*\*<font style="color:rgb(6, 10, 38);"> 总结</font>**

1. <code>**<font style="color:rgb(6, 10, 38);">crontab -l</font>**</code>**<font style="color:rgb(6, 10, 38);"> </font>\*\*\*\*<font style="color:rgb(6, 10, 38);">能显示</font>**<font style="color:rgb(6, 10, 38);">：这只是因为它在读写文本文件，普通用户有权做这件事。</font>
2. **<font style="color:rgb(6, 10, 38);">任务能跑 (在物理机)</font>**<font style="color:rgb(6, 10, 38);">：是因为物理机后台有一个</font><font style="color:rgb(6, 10, 38);"> </font>**<font style="color:rgb(6, 10, 38);">Root 用户</font>**<font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">运行的</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">crond</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">服务在帮你干活。</font>
3. **<font style="color:rgb(6, 10, 38);">任务不能跑 (在 K8s 普通用户 Pod)</font>**<font style="color:rgb(6, 10, 38);">：因为容器里默认没有那个 Root 版的</font><font style="color:rgb(6, 10, 38);"> </font><code><font style="color:rgb(6, 10, 38);">crond</font></code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">服务，而你又不允许启动它。</font>

**<font style="color:rgb(6, 10, 38);">所以，回到你的需求：</font>**<font style="color:rgb(6, 10, 38);">\ </font><font style="color:rgb(6, 10, 38);">如果你要在 K8s 里以</font>**<font style="color:rgb(6, 10, 38);">普通用户</font>**<font style="color:rgb(6, 10, 38);">运行 Pod 且</font>**<font style="color:rgb(6, 10, 38);">必须有定时任务</font>**<font style="color:rgb(6, 10, 38);">，你只有三条路：</font>

1. **<font style="color:rgb(6, 10, 38);">方案 A (推荐)</font>**<font style="color:rgb(6, 10, 38);">：使用</font><font style="color:rgb(6, 10, 38);"> </font><code>**<font style="color:rgb(6, 10, 38);">superCronic</font>**</code><font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">(它不需要 Root，自己就是调度器)。</font>
2. **<font style="color:rgb(6, 10, 38);">方案 B (简单)</font>**<font style="color:rgb(6, 10, 38);">：自己写</font><font style="color:rgb(6, 10, 38);"> </font><code>**<font style="color:rgb(6, 10, 38);">while</font>**</code>**<font style="color:rgb(6, 10, 38);"> </font>\*\*\*\*<font style="color:rgb(6, 10, 38);">循环</font>**<font style="color:rgb(6, 10, 38);"> </font><font style="color:rgb(6, 10, 38);">脚本 (你自己充当调度器)。</font>
3. **<font style="color:rgb(6, 10, 38);">方案 C (妥协)</font>**<font style="color:rgb(6, 10, 38);">：允许 Pod </font>**<font style="color:rgb(6, 10, 38);">以 Root 启动进程</font>**<font style="color:rgb(6, 10, 38);"> (运行 </font><code><font style="color:rgb(6, 10, 38);">crond</font></code><font style="color:rgb(6, 10, 38);">)，但让 </font><code><font style="color:rgb(6, 10, 38);">crond</font></code><font style="color:rgb(6, 10, 38);"> 内部降权执行任务 (这是最接近物理机体验的，但需要调整 K8s 安全策略)。</font>

## <font style="color:rgb(6, 10, 38);">我最终选了方案B</font>


> 更新: 2026-03-07 04:22:18  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/wbq7q1824gfhu0x7>
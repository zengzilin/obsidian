# rocky linux sudo su 异常变慢

                                                                                                                                                                                                                                                                                                                            ● 这里已经有一个明显问题了：机器主机名就是 localhost，/etc/hosts 里也只有 localhost 映射，没有独立主机名。



  这类配置很容易让 pam_systemd / sudo / ssh 在创建 session 时出现异常或超时。

                                                                                                                                                                                                                                                                                                                               先检查主机名

                                                                                                                                                                                                                                                                                                                               执行：



  hostname

  hostnamectl

  hostname -f



  如果 hostname -f 卡很久或报错，基本就坐实了。



  ---

  建议修复



  把主机名改成一个真实名字，比如：



  hostnamectl set-hostname rocky-app01



  然后改 /etc/hosts，至少变成这样：



  127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4

  127.0.1.1   rocky-app01

  ::1         localhost localhost.localdomain localhost6 localhost6.localdomain6



  如果你机器有固定内网 IP，更推荐这样：



  127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4

  192.168.x.x rocky-app01

  ::1         localhost localhost.localdomain localhost6 localhost6.localdomain6



  ---

  改完后执行



  systemctl restart dbus

  systemctl restart systemd-logind

  time sudo su -



  ---

  另外一个隐患



  你的 DNS 配的是公网：



  8.8.8.8

  1.2.4.8



  如果这台机器在内网、且公网 DNS 不稳定，也会放大超时问题。

  如果你们有内网 DNS，优先换成内网 DNS。



  ---

  现在我的判断



  当前最可疑的是：



  1. hostname 配成 localhost

  2. hosts 没有本机独立主机名映射

  3. DNS 可达性一般，导致 pam_systemd 会话创建更慢



  ---

  如果你不想直接改，我给你一个最小验证法：



  临时验证



  先只改 hostname，不重启系统：



  hostnamectl set-hostname rocky-app01

  printf '127.0.1.1 rocky-app01\n' >> /etc/hosts

  systemctl restart dbus

  systemctl restart systemd-logind

  time sudo su -



  如果马上恢复，就确定了。



> 更新: 2026-04-07 21:54:10  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/lfgbrdksg9wtowtr>
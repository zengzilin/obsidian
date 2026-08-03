# mysql exporter

prometheus target配置

* <code>**<font style="color:rgb(32, 33, 36);background-color:rgb(243, 246, 252);">mysqld_exporter</font>**</code><font style="color:rgb(32, 33, 36);background-color:rgb(243, 246, 252);"> </font><font style="color:rgb(32, 33, 36);background-color:rgb(243, 246, 252);">reads this</font><font style="color:rgb(32, 33, 36);background-color:rgb(243, 246, 252);"> </font><code><font style="color:rgb(32, 33, 36);background-color:rgb(243, 246, 252);">my.conf</font></code><font style="color:rgb(32, 33, 36);background-color:rgb(243, 246, 252);"> </font><font style="color:rgb(32, 33, 36);background-color:rgb(243, 246, 252);">file (typically located at</font><font style="color:rgb(32, 33, 36);background-color:rgb(243, 246, 252);"> </font><code><font style="color:rgb(32, 33, 36);background-color:rgb(243, 246, 252);">/etc/mysql/my.cnf</font></code><font style="color:rgb(32, 33, 36);background-color:rgb(243, 246, 252);">,</font><font style="color:rgb(32, 33, 36);background-color:rgb(243, 246, 252);"> </font><code><font style="color:rgb(32, 33, 36);background-color:rgb(243, 246, 252);">~/.my.cnf</font></code><font style="color:rgb(32, 33, 36);background-color:rgb(243, 246, 252);">, or specified via</font><font style="color:rgb(32, 33, 36);background-color:rgb(243, 246, 252);"> </font><code><font style="color:rgb(32, 33, 36);background-color:rgb(243, 246, 252);">--config.mycnf</font></code><font style="color:rgb(32, 33, 36);background-color:rgb(243, 246, 252);"> </font><font style="color:rgb(32, 33, 36);background-color:rgb(243, 246, 252);">flag).</font>
* <font style="color:rgb(32, 33, 36);background-color:rgb(243, 246, 252);">When Prometheus scrapes</font><font style="color:rgb(32, 33, 36);background-color:rgb(243, 246, 252);"> </font><code><font style="color:rgb(32, 33, 36);background-color:rgb(243, 246, 252);">mysqld_exporter</font></code><font style="color:rgb(32, 33, 36);background-color:rgb(243, 246, 252);">, you'll usually pass a</font><font style="color:rgb(32, 33, 36);background-color:rgb(243, 246, 252);"> </font><code><font style="color:rgb(32, 33, 36);background-color:rgb(243, 246, 252);">target</font></code><font style="color:rgb(32, 33, 36);background-color:rgb(243, 246, 252);"> </font><font style="color:rgb(32, 33, 36);background-color:rgb(243, 246, 252);">parameter in your scrape configuration, like:</font>

```yaml
- job_name: 'mysql_exporter_multi_target'
  static_configs:
    - targets:
        - dev-mysql          # The 'name' from your YAML
        - test-mysql         # The 'name' from your YAML
  relabel_configs:
    - source_labels: [__address__]
      target_label: __param_target
    - source_labels: [__param_target]
      target_label: instance
    - target_label: __address__
      replacement: localhost:9104 # Or whatever host:port your export
```


> 更新: 2025-05-26 15:09:00  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/vcpoptiup82dl9ul>
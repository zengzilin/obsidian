# etcd查看集群信息

ETCDCTL_API=3 /usr/local/bin/etcdctl   --endpoints=[https://127.0.0.1:2379](https://127.0.0.1:2379)   --cacert=/etc/ssl/etcd/ssl/ca.pem    --cert=/etc/ssl/etcd/ssl/admin-node1.pem    --key=/etc/ssl/etcd/ssl/admin-node1-key.pem member list --write-out=table

+------------------+---------+-------+----------------------------+----------------------------+------------+

|        ID        | STATUS  | NAME  |         PEER ADDRS         |        CLIENT ADDRS        | IS LEARNER |

+------------------+---------+-------+----------------------------+----------------------------+------------+

| 317ed2741997ed2c | started | etcd3 | [https://192.168.4.107:2380](https://192.168.4.107:2380) | [https://192.168.4.107:2379](https://192.168.4.107:2379) |      false |

| c522ed18c3d33016 | started | etcd2 | [https://192.168.4.106:2380](https://192.168.4.106:2380) | [https://192.168.4.106:2379](https://192.168.4.106:2379) |      false |

| ff09dc64515f3ea9 | started | etcd1 | [https://192.168.4.105:2380](https://192.168.4.105:2380) | [https://192.168.4.105:2379](https://192.168.4.105:2379) |      false |

+------------------+---------+-------+----------------------------+----------------------------+------------+





恢复备份

./etcdctl snapshot restore /tmp/snapshot.db --name etcd2 --initial-cluster etcd2=[https://192.168.4.106:2380](https://192.168.4.106:2380) --initial-cluster-token k8s_etcd --initial-advertise-peer-urls [https://192.168.4.106:2380](https://192.168.4.106:2380) --data-dir ./backup/



> 更新: 2025-04-22 09:23:04  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/rzdexw8aewimz1as>
# 多域名蓝绿部署操作手册

## 适用范围

这份文档用于当前这套不依赖 OpenKruise 的蓝绿部署方案，基于：

- Kubernetes `Deployment`
- 多个 Kubernetes `Namespace`
- Gateway API `HTTPRoute`
- Nacos `Namespace`

适用域名包括：

- `gw-preprod-wallet-api.tiqmopayment.com`
- `gw-preprod-wallet-portal.tiqmopayment.com`
- `gw-preprod-account-portal.tiqmopayment.com`
- `gw-preprod-acquiring-portal.tiqmopayment.com`
- `gw-preprod-loyalty-portal.tiqmopayment.com`

## 目标

建立两套固定槽位环境，而不是把资源名字直接命名成 blue / green。

这里约定：

- `slot-a`
- `slot-b`

蓝绿只是发布过程中的“角色”，不是资源名称。

任意时刻：

- 一个槽位承担当前生产流量
- 另一个槽位承担下一次发布验证

这样切换后不会出现“green 已经变成生产，但资源名字还叫 green”的误导。

## 一、核心设计原则

## 1. Kubernetes Namespace 不体现 blue / green

业务 Namespace 使用固定槽位命名。

建议命名如下：

- `wallet-a`
- `wallet-b`
- `account-a`
- `account-b`
- `acquiring-a`
- `acquiring-b`
- `frontend-a`
- `frontend-b`
- `edge-routing`

说明：

- `*-a` 和 `*-b` 是固定槽位
- `edge-routing` 只放统一入口路由

## 2. Nacos Namespace 也不体现 blue / green

Nacos 也使用固定槽位命名。

建议：

- `slot-a`
- `slot-b`

说明：

- 所有 `*-a` 的 Kubernetes Namespace 对应 `slot-a`
- 所有 `*-b` 的 Kubernetes Namespace 对应 `slot-b`

这样关系清晰：

- `wallet-a / account-a / acquiring-a / frontend-a` 全部注册到 `slot-a`
- `wallet-b / account-b / acquiring-b / frontend-b` 全部注册到 `slot-b`

## 3. 用独立状态标识判断当前谁是生产槽位

不要通过 Namespace 名称判断当前谁是 blue / green。

应通过一个独立状态标识来判断：

- 当前生产槽位是谁
- 当前发布目标槽位是谁

推荐做法：

在 Kubernetes 中维护一个固定的 `ConfigMap`，作为发布状态标识。

建议名称：

- `release-slot-state`

建议放在：

- `edge-routing`

示例：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: release-slot-state
  namespace: edge-routing
data:
  activeSlot: "a"
  standbySlot: "b"
  activeNacosNamespaceId: "slot-a-id"
  standbyNacosNamespaceId: "slot-b-id"
  currentRelease: "2026.06.24.01"
```

语义说明：

- `activeSlot`
  - 当前承载生产流量的槽位
  - 在发布语义上，可以理解为当前 blue
- `standbySlot`
  - 下一次部署目标槽位
  - 在发布语义上，可以理解为下一次 green

切换完成且旧槽位确认下线后，更新这个标识：

- `activeSlot: b`
- `standbySlot: a`

这样下次发布时，流程就能自动判断新版本该部署到哪套槽位。

## 4. 路由文件建议按域名拆分

建议从“按业务系统文件拆分”改成“按域名拆分”。

这是因为你当前同一个 host 可能分散在多个文件里，容易出现：

- 同一域名的 path 规则分散
- 切换时漏改一部分 path
- 同 host 多文件 review 不直观

所以推荐：

- 一个公网域名对应一个路由文件

建议文件组织：

```text
common/
  gatewayapi/
    domains/
      wallet-api.yaml
      wallet-portal.yaml
      account-portal.yaml
      acquiring-portal.yaml
      loyalty-portal.yaml
    referencegrants/
      wallet-a.yaml
      wallet-b.yaml
      account-a.yaml
      account-b.yaml
      acquiring-a.yaml
      acquiring-b.yaml
      frontend-a.yaml
      frontend-b.yaml
  release/
    slot-state.yaml
```

这样更直观：

- 管理按域名收口
- 切换更自由
- review 更容易
- 不同人维护时更不容易漏改

## 二、当前域名现状说明

当前仓库中相关域名主要分布在：

- `gatewayapi/wallet.yaml`
- `gatewayapi/account.yaml`
- `gatewayapi/acquiring.yaml`
- `gatewayapi/frontend.yaml`

当前问题是：

- 同一个 hostname 的 path 规则不一定在同一个文件
- 前端和后端路由存在交叉

因此正式改造时，建议把下面这些域名都收口成“一个域名一个文件”：

- `wallet-api`
- `wallet-portal`
- `account-portal`
- `acquiring-portal`
- `loyalty-portal`

## 三、资源命名与映射规则

## 1. Kubernetes Namespace 规则

建议固定如下：

| 模块 | 槽位 A | 槽位 B |
|---|---|---|
| wallet | `wallet-a` | `wallet-b` |
| account | `account-a` | `account-b` |
| acquiring | `acquiring-a` | `acquiring-b` |
| frontend | `frontend-a` | `frontend-b` |

## 2. Nacos Namespace 规则

建议固定如下：

| 槽位 | Nacos Namespace 名称 |
|---|---|
| A | `slot-a` |
| B | `slot-b` |

注意：

- 应用中配置的是 Nacos Namespace ID
- 不是显示名称

## 3. 槽位映射规则

| 发布角色 | 由谁决定 | 示例 |
|---|---|---|
| 当前生产槽位 | `release-slot-state.data.activeSlot` | `a` |
| 下一次部署槽位 | `release-slot-state.data.standbySlot` | `b` |
| 当前生产 Nacos 命名空间 | `activeNacosNamespaceId` | `slot-a-id` |
| 下一次部署 Nacos 命名空间 | `standbyNacosNamespaceId` | `slot-b-id` |

## 四、实施步骤

## 第 1 步：创建固定槽位 Namespace

执行：

```bash
kubectl create ns wallet-a
kubectl create ns wallet-b
kubectl create ns account-a
kubectl create ns account-b
kubectl create ns acquiring-a
kubectl create ns acquiring-b
kubectl create ns frontend-a
kubectl create ns frontend-b
kubectl create ns edge-routing
```

## 第 2 步：在 Nacos 中创建固定槽位 Namespace

在 Nacos 控制台中创建：

- `slot-a`
- `slot-b`

创建后记录各自 Namespace ID。

## 第 3 步：创建发布状态标识

在 `edge-routing` 中创建状态 `ConfigMap`。

示例：

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: release-slot-state
  namespace: edge-routing
data:
  activeSlot: "a"
  standbySlot: "b"
  activeNacosNamespaceId: "slot-a-id"
  standbyNacosNamespaceId: "slot-b-id"
  currentRelease: "2026.06.24.01"
```

第一次部署时约定：

- 生产在 A
- 待发布在 B

则：

- `activeSlot = a`
- `standbySlot = b`

## 第 4 步：部署两套固定槽位业务

每个模块都要有两套相同结构：

- `wallet-a` / `wallet-b`
- `account-a` / `account-b`
- `acquiring-a` / `acquiring-b`
- `frontend-a` / `frontend-b`

建议保持：

- Service 名一致
- 端口一致
- 健康检查一致

示例：

- `wallet-a/wallyt-intf-web`
- `wallet-b/wallyt-intf-web`

这样切流时只变更 Namespace，不变更 Service 名。

## 第 5 步：应用通过槽位绑定 Nacos Namespace

应用配置建议如下：

```yaml
spring:
  config:
    import:
      - optional:nacos:${spring.application.name}.yaml
  cloud:
    nacos:
      config:
        server-addr: nacos-cs.middleware.svc.cluster.local:8848
        namespace: ${NACOS_CONFIG_NAMESPACE}
        group: DEFAULT_GROUP
      discovery:
        server-addr: nacos-cs.middleware.svc.cluster.local:8848
        namespace: ${NACOS_DISCOVERY_NAMESPACE}
        group: DEFAULT_GROUP
```

如果当前发布目标是 `slot-b`，那部署到 `wallet-b / account-b / acquiring-b / frontend-b` 时，环境变量应统一使用 `slot-b-id`。

示例：

```yaml
env:
- name: NACOS_CONFIG_NAMESPACE
  value: slot-b-id
- name: NACOS_DISCOVERY_NAMESPACE
  value: slot-b-id
```

如果当前生产在 `slot-a`，则 `*-a` 仍然维持：

```yaml
env:
- name: NACOS_CONFIG_NAMESPACE
  value: slot-a-id
- name: NACOS_DISCOVERY_NAMESPACE
  value: slot-a-id
```

## 第 6 步：在每个槽位 Namespace 中创建 ReferenceGrant

因为路由统一放在 `edge-routing`，而 Service 在各业务 Namespace 中，所以要授权跨 Namespace 引用。

示例：`wallet-a`

```yaml
apiVersion: gateway.networking.k8s.io/v1beta1
kind: ReferenceGrant
metadata:
  name: allow-edge-routing
  namespace: wallet-a
spec:
  from:
  - group: gateway.networking.k8s.io
    kind: HTTPRoute
    namespace: edge-routing
  to:
  - group: ""
    kind: Service
```

下面这些 Namespace 都需要一份：

- `wallet-a`
- `wallet-b`
- `account-a`
- `account-b`
- `acquiring-a`
- `acquiring-b`
- `frontend-a`
- `frontend-b`

## 第 7 步：建立按域名拆分的路由文件

建议每个域名一个 YAML 文件。

推荐文件：

- `gatewayapi/domains/wallet-api.yaml`
- `gatewayapi/domains/wallet-portal.yaml`
- `gatewayapi/domains/account-portal.yaml`
- `gatewayapi/domains/acquiring-portal.yaml`
- `gatewayapi/domains/loyalty-portal.yaml`

每个文件建议同时包含：

- 生产路由
- 预览路由

这样一个文件就能完整表达该域名的切换逻辑。

## 第 8 步：预览路由固定指向 standbySlot

预览域名建议为独立 host，例如：

- `gw-preprod-wallet-api-preview.tiqmopayment.com`
- `gw-preprod-wallet-portal-preview.tiqmopayment.com`
- `gw-preprod-account-portal-preview.tiqmopayment.com`
- `gw-preprod-acquiring-portal-preview.tiqmopayment.com`
- `gw-preprod-loyalty-portal-preview.tiqmopayment.com`

说明：

- 不建议把 preview host 命名成 `*-green`
- 因为槽位角色会轮换
- preview 永远指向 `standbySlot`

例如当前：

- `activeSlot = a`
- `standbySlot = b`

那么所有 preview route 都应指向 `*-b`

## 第 9 步：生产路由固定指向 activeSlot

生产域名始终只保留一套对外路由。

例如 `wallet-api`：

```yaml
apiVersion: gateway.networking.k8s.io/v1
kind: HTTPRoute
metadata:
  name: wallet-api-prod
  namespace: edge-routing
spec:
  parentRefs:
  - name: internal-gateway
    namespace: default
    sectionName: https
  hostnames:
  - gw-preprod-wallet-api.tiqmopayment.com
  rules:
  - matches:
    - path:
        type: PathPrefix
        value: /
    backendRefs:
    - name: wallyt-intf-web
      namespace: wallet-a
      port: 9092
  - matches:
    - path:
        type: PathPrefix
        value: /api
    backendRefs:
    - name: wallyt-cardpaymt-web
      namespace: wallet-a
      port: 9093
```

如果当前生产槽位切到 `b`，则只把 backend namespace 从 `wallet-a` 改成 `wallet-b`。

## 第 10 步：同一个域名的全部 path 规则必须一起切

这是关键要求。

例如：

- `wallet-portal`
- `wallet-api`
- `account-portal`
- `acquiring-portal`

这些域名当前存在 path 分散在多个文件的情况。

改造时必须做到：

- 同一个 hostname 的所有 path 统一收口到一个域名文件
- 切换时整组切换

不要出现：

- `/` 还在 A
- `/api` 已经切到 B

这不属于蓝绿，而会变成混流。

## 第 11 步：发布时的标准流程

假设当前状态：

- `activeSlot = a`
- `standbySlot = b`

则本次发布流程如下：

1. 读取 `release-slot-state`
2. 判断当前生产在 A，下一次部署到 B
3. 将新版本部署到：
   - `wallet-b`
   - `account-b`
   - `acquiring-b`
   - `frontend-b`
4. 所有新版本应用注册到 Nacos `slot-b`
5. 所有 preview 域名都指向 B
6. 用 preview 域名完成验证
7. 更新生产 `HTTPRoute`，把所有生产域名从 `*-a` 切到 `*-b`
8. 观察生产稳定
9. 确认 A 已下线或不再承载生产流量
10. 更新 `release-slot-state`

更新后的状态：

- `activeSlot = b`
- `standbySlot = a`
- `activeNacosNamespaceId = slot-b-id`
- `standbyNacosNamespaceId = slot-a-id`

下次发布就自动基于 A 再做一次。

## 第 12 步：回滚流程

如果切换后出现问题：

1. 读取当前 `release-slot-state`
2. 将生产 `HTTPRoute` 从当前新槽位切回旧槽位
3. 验证生产流量恢复
4. 保留新槽位环境用于排查
5. 不要急着更新 `release-slot-state`

只有当新槽位稳定成为生产后，才更新状态标识。

## 五、推荐的域名级路由拆分方式

## 1. wallet-api.yaml

管理：

- `gw-preprod-wallet-api.tiqmopayment.com`
- `gw-preprod-wallet-api-preview.tiqmopayment.com`

包含：

- `/`
- `/api`

## 2. wallet-portal.yaml

管理：

- `gw-preprod-wallet-portal.tiqmopayment.com`
- `gw-preprod-wallet-portal-preview.tiqmopayment.com`

建议把这些 path 一并收口：

- `/swallet-oms`
- `/agreement/`
- `/h5/`
- `/`

## 3. account-portal.yaml

管理：

- `gw-preprod-account-portal.tiqmopayment.com`
- `gw-preprod-account-portal-preview.tiqmopayment.com`

同一个域名下所有 path 一起放在同一文件。

## 4. acquiring-portal.yaml

管理：

- `gw-preprod-acquiring-portal.tiqmopayment.com`
- `gw-preprod-acquiring-portal-preview.tiqmopayment.com`

同样要求整域名收口。

## 5. loyalty-portal.yaml

管理：

- `gw-preprod-loyalty-portal.tiqmopayment.com`
- `gw-preprod-loyalty-portal-preview.tiqmopayment.com`

这组通常最简单。

## 六、操作检查清单

发布前：

- [ ] `wallet-a / wallet-b / account-a / account-b / acquiring-a / acquiring-b / frontend-a / frontend-b` 已创建
- [ ] `slot-a / slot-b` 已在 Nacos 中创建
- [ ] `release-slot-state` 已创建
- [ ] 所有 `ReferenceGrant` 已创建
- [ ] 所有域名文件已按 hostname 收口
- [ ] 所有 preview 路由已建立

本次发布前：

- [ ] 已读取 `release-slot-state`
- [ ] 已确认当前 `activeSlot`
- [ ] 已确认本次 `standbySlot`
- [ ] 新版本只部署到 `standbySlot`
- [ ] 新版本只注册到 `standbySlot` 对应的 Nacos Namespace

切换前：

- [ ] standbySlot 的所有 Pod Ready
- [ ] standbySlot 的所有 Service 健康检查通过
- [ ] preview 域名验证通过
- [ ] standbySlot 内部调用正常
- [ ] 数据库兼容性确认通过

切换后：

- [ ] 生产域名访问正常
- [ ] 日志正常
- [ ] 监控正常
- [ ] 告警正常
- [ ] 旧槽位确认已退出生产
- [ ] `release-slot-state` 已更新

## 七、注意事项

## 1. blue / green 只是角色，不是资源名

文档中如果提到 blue / green，只表示发布角色：

- 当前生产角色
- 当前待发布角色

不应该出现在 Namespace 或文件命名里。

## 2. 同一域名不要半切换

这是蓝绿，不是金丝雀。

同一个 hostname 的所有 path 最好整组切换。

## 3. Service 名尽量在 A/B 中保持一致

这样切换只需要改 Namespace。

## 4. readiness 检查保持一致

你当前 `gatewayapi/wallet.yaml` 已经使用 readiness 风格健康检查，A/B 两套都应保持一致。

## 5. 数据库变更必须向后兼容

蓝绿方案只能解决路由与服务发现切换，不能解决不兼容表结构问题。

## 6. Spring Cloud Alibaba 新版本建议

如果使用的是 `2025.1.x` 及以后版本，建议使用：

- `application.yml`
- `spring.config.import`

尽量不要依赖旧的 `bootstrap.yml` 方式。

## 八、建议的仓库落地顺序

建议按如下顺序推进：

1. 先确定 A/B 命名方案
2. 再创建 `release-slot-state`
3. 再创建 `slot-a / slot-b` 的 Nacos Namespace
4. 再把 Gateway 路由按域名收口
5. 再补 `ReferenceGrant`
6. 再建立 preview 路由
7. 在 preprod 完整演练一次 A/B 切换

## 文档位置

英文版：

- `common/BLUE_GREEN_DEPLOYMENT_GUIDE.md`

中文版：

- `common/BLUE_GREEN_DEPLOYMENT_GUIDE_CN.md`

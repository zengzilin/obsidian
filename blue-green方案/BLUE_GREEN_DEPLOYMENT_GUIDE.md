# Multi-Domain Blue-Green Deployment Guide

## Scope

This guide describes a blue-green deployment approach without OpenKruise, based on:

- Kubernetes `Deployment`
- multiple Kubernetes `Namespace`s
- Gateway API `HTTPRoute`
- Nacos `Namespace`

It applies to the current domains in this repo:

- `gw-preprod-wallet-api.tiqmopayment.com`
- `gw-preprod-wallet-portal.tiqmopayment.com`
- `gw-preprod-account-portal.tiqmopayment.com`
- `gw-preprod-acquiring-portal.tiqmopayment.com`
- `gw-preprod-loyalty-portal.tiqmopayment.com`

## Goal

Use two fixed environment slots instead of naming resources directly as blue and green.

In this guide:

- `slot-a`
- `slot-b`

Blue and green are deployment roles, not resource names.

At any time:

- one slot serves production traffic
- the other slot serves the next deployment validation

This avoids misleading names after a switch, such as a production environment still being named `green`.

## Core Principles

## 1. Kubernetes Namespaces should not contain blue / green

Use fixed slot names for business namespaces.

Recommended names:

- `wallet-a`
- `wallet-b`
- `account-a`
- `account-b`
- `acquiring-a`
- `acquiring-b`
- `frontend-a`
- `frontend-b`
- `edge-routing`

Meaning:

- `*-a` and `*-b` are fixed slots
- `edge-routing` stores the unified external routes

## 2. Nacos Namespaces should not contain blue / green either

Use fixed slot names in Nacos as well.

Recommended:

- `slot-a`
- `slot-b`

Meaning:

- all `*-a` Kubernetes namespaces map to `slot-a`
- all `*-b` Kubernetes namespaces map to `slot-b`

This creates a clear one-to-one mapping:

- `wallet-a / account-a / acquiring-a / frontend-a` register to `slot-a`
- `wallet-b / account-b / acquiring-b / frontend-b` register to `slot-b`

## 3. Use an independent state marker to identify the current production slot

Do not infer blue / green from namespace names.

Use one independent state marker to identify:

- which slot is currently production
- which slot is the next deployment target

Recommended approach:

Maintain a fixed `ConfigMap` in Kubernetes as the release slot state.

Suggested name:

- `release-slot-state`

Suggested location:

- `edge-routing`

Example:

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

Meaning:

- `activeSlot`
  - the slot currently serving production traffic
  - in deployment language, this is the current blue
- `standbySlot`
  - the slot used for the next deployment
  - in deployment language, this is the next green

After the switch is complete and the old slot is fully retired, update the state:

- `activeSlot: b`
- `standbySlot: a`

This allows the next deployment to automatically know where to place the new version.

## 4. Route files should be organized by domain

It is recommended to move from system-based route files to domain-based route files.

Reason:

- the same hostname may currently be split across multiple files
- some path rules may be missed during switching
- review is less intuitive when one hostname is spread across multiple files

Recommended rule:

- one public domain per route file

Suggested file layout:

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

Benefits:

- domain-level ownership is clearer
- switching is more flexible
- review is easier
- maintainers are less likely to miss related path rules

## Current Domain Situation

Relevant routes are currently spread across:

- `gatewayapi/wallet.yaml`
- `gatewayapi/account.yaml`
- `gatewayapi/acquiring.yaml`
- `gatewayapi/frontend.yaml`

Current issues:

- the same hostname may be split across different files by path
- frontend and backend routes may overlap

Recommended target:

Consolidate these domains into one file per hostname:

- `wallet-api`
- `wallet-portal`
- `account-portal`
- `acquiring-portal`
- `loyalty-portal`

## Naming and Mapping Rules

## 1. Kubernetes Namespace rules

Recommended fixed naming:

| Module | Slot A | Slot B |
|---|---|---|
| wallet | `wallet-a` | `wallet-b` |
| account | `account-a` | `account-b` |
| acquiring | `acquiring-a` | `acquiring-b` |
| frontend | `frontend-a` | `frontend-b` |

## 2. Nacos Namespace rules

Recommended fixed naming:

| Slot | Nacos Namespace name |
|---|---|
| A | `slot-a` |
| B | `slot-b` |

Important:

- applications should use the Nacos namespace ID
- not the display name

## 3. Slot mapping rules

| Role | Source of truth | Example |
|---|---|---|
| current production slot | `release-slot-state.data.activeSlot` | `a` |
| next deployment slot | `release-slot-state.data.standbySlot` | `b` |
| current production Nacos namespace | `activeNacosNamespaceId` | `slot-a-id` |
| next deployment Nacos namespace | `standbyNacosNamespaceId` | `slot-b-id` |

## Implementation Steps

## Step 1. Create fixed slot namespaces

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

## Step 2. Create fixed slot namespaces in Nacos

Create these two Nacos namespaces:

- `slot-a`
- `slot-b`

Record their namespace IDs.

## Step 3. Create the release state marker

Create the state `ConfigMap` in `edge-routing`.

Example:

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

Initial convention:

- production runs in A
- the next deployment target is B

So:

- `activeSlot = a`
- `standbySlot = b`

## Step 4. Deploy both slot environments

Each module must have two equivalent environments:

- `wallet-a` / `wallet-b`
- `account-a` / `account-b`
- `acquiring-a` / `acquiring-b`
- `frontend-a` / `frontend-b`

Recommended consistency:

- same Service name
- same ports
- same health checks

Example:

- `wallet-a/wallyt-intf-web`
- `wallet-b/wallyt-intf-web`

This keeps traffic switching simple because only the namespace changes.

## Step 5. Bind applications to the slot-specific Nacos namespace

Recommended application config:

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

If the current deployment target is `slot-b`, then workloads deployed to `wallet-b / account-b / acquiring-b / frontend-b` should all use `slot-b-id`.

Example:

```yaml
env:
- name: NACOS_CONFIG_NAMESPACE
  value: slot-b-id
- name: NACOS_DISCOVERY_NAMESPACE
  value: slot-b-id
```

If current production is still in `slot-a`, the `*-a` workloads keep using:

```yaml
env:
- name: NACOS_CONFIG_NAMESPACE
  value: slot-a-id
- name: NACOS_DISCOVERY_NAMESPACE
  value: slot-a-id
```

## Step 6. Create `ReferenceGrant` in every slot namespace

Because routes are centralized in `edge-routing` while Services live in business namespaces, cross-namespace references must be explicitly allowed.

Example for `wallet-a`:

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

Create equivalent resources in:

- `wallet-a`
- `wallet-b`
- `account-a`
- `account-b`
- `acquiring-a`
- `acquiring-b`
- `frontend-a`
- `frontend-b`

## Step 7. Split route files by domain

Recommended files:

- `gatewayapi/domains/wallet-api.yaml`
- `gatewayapi/domains/wallet-portal.yaml`
- `gatewayapi/domains/account-portal.yaml`
- `gatewayapi/domains/acquiring-portal.yaml`
- `gatewayapi/domains/loyalty-portal.yaml`

Each file should contain:

- the production route
- the preview route

This makes one file the complete source of truth for one public domain.

## Step 8. Preview routes should always point to `standbySlot`

Recommended preview hostnames:

- `gw-preprod-wallet-api-preview.tiqmopayment.com`
- `gw-preprod-wallet-portal-preview.tiqmopayment.com`
- `gw-preprod-account-portal-preview.tiqmopayment.com`
- `gw-preprod-acquiring-portal-preview.tiqmopayment.com`
- `gw-preprod-loyalty-portal-preview.tiqmopayment.com`

Important:

- do not name preview hosts as `*-green`
- slot roles rotate over time
- preview should always point to `standbySlot`

Example:

If:

- `activeSlot = a`
- `standbySlot = b`

then all preview routes should point to `*-b`.

## Step 9. Production routes should always point to `activeSlot`

Each production domain should expose only one active public route.

Example `wallet-api`:

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

If production moves to slot B, only the backend namespace changes from `wallet-a` to `wallet-b`.

## Step 10. All path rules of the same hostname must switch together

This is a key rule.

Examples:

- `wallet-portal`
- `wallet-api`
- `account-portal`
- `acquiring-portal`

These domains currently have path rules spread across multiple files.

The target model must ensure:

- all paths for one hostname are consolidated into one domain file
- switching happens for the whole hostname as one unit

Do not allow cases like:

- `/` still points to slot A
- `/api` already points to slot B

That becomes mixed routing, not blue-green deployment.

## Step 11. Standard deployment flow

Assume the current state is:

- `activeSlot = a`
- `standbySlot = b`

Then the release flow is:

1. read `release-slot-state`
2. determine that production is in A and the next deployment goes to B
3. deploy the new version to:
   - `wallet-b`
   - `account-b`
   - `acquiring-b`
   - `frontend-b`
4. register all new workloads to Nacos `slot-b`
5. point all preview domains to slot B
6. validate the preview domains
7. update the production `HTTPRoute`s and switch all production domains from `*-a` to `*-b`
8. observe production stability
9. confirm the A slot is retired or no longer serving production traffic
10. update `release-slot-state`

New state:

- `activeSlot = b`
- `standbySlot = a`
- `activeNacosNamespaceId = slot-b-id`
- `standbyNacosNamespaceId = slot-a-id`

The next deployment will then naturally target slot A.

## Step 12. Rollback flow

If issues appear after the switch:

1. read the current `release-slot-state`
2. switch the production `HTTPRoute`s back from the new slot to the old slot
3. verify production traffic recovery
4. keep the new slot environment for debugging
5. do not update `release-slot-state` yet

Only update the state marker after the new slot has become the confirmed production slot.

## Recommended Domain-Level Route Split

## 1. wallet-api.yaml

Manages:

- `gw-preprod-wallet-api.tiqmopayment.com`
- `gw-preprod-wallet-api-preview.tiqmopayment.com`

Includes:

- `/`
- `/api`

## 2. wallet-portal.yaml

Manages:

- `gw-preprod-wallet-portal.tiqmopayment.com`
- `gw-preprod-wallet-portal-preview.tiqmopayment.com`

Recommended path consolidation:

- `/swallet-oms`
- `/agreement/`
- `/h5/`
- `/`

## 3. account-portal.yaml

Manages:

- `gw-preprod-account-portal.tiqmopayment.com`
- `gw-preprod-account-portal-preview.tiqmopayment.com`

All paths for the same domain should stay in this file.

## 4. acquiring-portal.yaml

Manages:

- `gw-preprod-acquiring-portal.tiqmopayment.com`
- `gw-preprod-acquiring-portal-preview.tiqmopayment.com`

The same full-domain consolidation rule applies.

## 5. loyalty-portal.yaml

Manages:

- `gw-preprod-loyalty-portal.tiqmopayment.com`
- `gw-preprod-loyalty-portal-preview.tiqmopayment.com`

This is usually the simplest one.

## Operational Checklist

Before rollout design:

- [ ] `wallet-a / wallet-b / account-a / account-b / acquiring-a / acquiring-b / frontend-a / frontend-b` are created
- [ ] `slot-a / slot-b` exist in Nacos
- [ ] `release-slot-state` exists
- [ ] all `ReferenceGrant` resources exist
- [ ] all routes are consolidated by hostname
- [ ] all preview routes exist

Before a deployment:

- [ ] `release-slot-state` has been read
- [ ] current `activeSlot` is confirmed
- [ ] current `standbySlot` is confirmed
- [ ] the new version is deployed only to `standbySlot`
- [ ] the new version is registered only to the `standbySlot` Nacos namespace

Before switching production:

- [ ] all Pods in `standbySlot` are Ready
- [ ] all Services in `standbySlot` pass health checks
- [ ] preview domains are validated
- [ ] internal calls inside `standbySlot` work correctly
- [ ] database compatibility is confirmed

After switching production:

- [ ] production domains are healthy
- [ ] logs are normal
- [ ] metrics are normal
- [ ] alerts are normal
- [ ] the old slot is confirmed out of production
- [ ] `release-slot-state` is updated

## Notes

## 1. Blue / green are roles, not names

If this guide mentions blue or green, it refers only to release roles:

- current production role
- current next-release role

They should not appear in namespace names or file names.

## 2. Do not partially switch one hostname

This is blue-green, not canary.

All paths of one hostname should ideally switch together.

## 3. Keep Service names consistent across slots

This keeps switching simple because only the namespace changes.

## 4. Keep readiness checks consistent

Your current `gatewayapi/wallet.yaml` already follows a readiness-style health check model. Both slots should keep the same behavior.

## 5. Database changes must remain backward compatible

Blue-green routing solves traffic and service discovery switching. It does not solve incompatible schema changes.

## 6. Spring Cloud Alibaba version note

If you are using `2025.1.x` or later, prefer:

- `application.yml`
- `spring.config.import`

Avoid relying on the old `bootstrap.yml` pattern unless your current version still requires it.

## Suggested Rollout Order in This Repo

Recommended order:

1. define the A/B naming convention
2. create `release-slot-state`
3. create `slot-a / slot-b` in Nacos
4. consolidate Gateway routes by domain
5. add all `ReferenceGrant` resources
6. create preview routes
7. rehearse one full A/B switch in preprod

## Document Locations

Chinese version:

- `common/BLUE_GREEN_DEPLOYMENT_GUIDE_CN.md`

English version:

- `common/BLUE_GREEN_DEPLOYMENT_GUIDE.md`

# Elasticsearch / Logstash Hotfix Runbook

## Scope

This runbook records the emergency handling steps for Logstash `429` / `_bulk` timeout issues caused by Elasticsearch write hotspots on log data streams.

Relevant data streams:

- `logs-svrlog-wallet`
- `logs-ingress-nginx-ingress-nginx`

Relevant Elasticsearch nodes:

- `elasticsearch01` / `10.21.104.13`
- `elasticsearch02` / `10.21.104.14`
- `elasticsearch03` / `10.21.104.15`

## Symptoms

Typical Logstash errors:

```text
es_rejected_execution_exception
Manticore::SocketTimeout Read timed out
Marking url as dead
Attempted to send a bulk request but Elasticsearch appears to be unreachable or down
```

Typical Elasticsearch signs:

- `indexing_pressure` rejections concentrated on `elasticsearch01`
- `write` thread pool queue concentrated on `elasticsearch01`
- current write index using only `1` primary shard

## Root Cause

The high-traffic data streams were using the default `logs` template with a single primary shard.

This caused:

- `logs-svrlog-wallet` current write index primary shard to land on `elasticsearch01`
- `logs-ingress-nginx-ingress-nginx` current write index primary shard to land on a single node as well
- write traffic to concentrate on one node instead of spreading across the cluster
- `429` and `_bulk` timeouts under sustained Logstash ingestion

## Immediate Logstash Mitigation

Use conservative settings on each Logstash instance:

```text
consumer_threads = 1
pipeline workers = 1
pipeline batch size = 100
pipeline batch delay = 50
queue.type = persisted
queue.max_bytes = 8GB to 20GB depending on pipeline importance
queue.checkpoint.writes = 1024
```

Temporary guidance:

- keep non-critical pipelines throttled or paused
- if needed, temporarily remove `10.21.104.13:9200` from Logstash `hosts` to reduce coordinating pressure on `elasticsearch01`

## Hotfix for `logs-svrlog-wallet`

### 1. Reduce pressure on the current write index

Current write index at time of incident:

```text
.ds-logs-svrlog-wallet-2026.05.21-001642
```

Run:

```http
PUT .ds-logs-svrlog-wallet-2026.05.21-001642/_settings
{
  "index": {
    "number_of_replicas": 0,
    "refresh_interval": "30s"
  }
}
```

### 2. Create a dedicated high-priority index template

Run:

```http
DELETE _index_template/logs-svrlog-wallet-hotfix

PUT _index_template/logs-svrlog-wallet
{
  "index_patterns": ["logs-svrlog-wallet*"],
  "data_stream": {},
  "priority": 500,
  "template": {
    "settings": {
      "index.number_of_shards": 3,
      "index.number_of_replicas": 1,
      "index.refresh_interval": "5s"
    }
  }
}
```

If `logs-svrlog-wallet-hotfix` still exists, delete it first. Elasticsearch does not support renaming an index template in place, so creating `logs-svrlog-wallet` with the same pattern and priority will fail until the old template is removed.

### 3. Force rollover

Run:

```http
POST logs-svrlog-wallet/_rollover
```

### 4. Validate

Run:

```http
GET _data_stream/logs-svrlog-wallet
GET _cat/shards/.ds-logs-svrlog-wallet-*?v
GET _cat/thread_pool/write?v&h=node_name,active,queue,rejected,completed
```

Expected result:

- the newest backing index has shards `0 p`, `1 p`, `2 p`
- primary shards are spread across `elasticsearch01/02/03`
- `elasticsearch01` write queue starts dropping

## Hotfix for `logs-ingress-nginx-ingress-nginx`

### 1. Reduce pressure on the current write index

Current write index at time of incident:

```text
.ds-logs-ingress-nginx-ingress-nginx-2026.05.16-000045
```

Run:

```http
PUT .ds-logs-ingress-nginx-ingress-nginx-2026.05.16-000045/_settings
{
  "index": {
    "number_of_replicas": 0,
    "refresh_interval": "30s"
  }
}
```

### 2. Create a dedicated high-priority index template

Run:

```http
DELETE _index_template/logs-ingress-nginx-hotfix

PUT _index_template/logs-ingress-nginx-ingress-nginx
{
  "index_patterns": ["logs-ingress-nginx-ingress-nginx*"],
  "data_stream": {},
  "priority": 500,
  "template": {
    "settings": {
      "index.number_of_shards": 3,
      "index.number_of_replicas": 1,
      "index.refresh_interval": "5s"
    }
  }
}
```

If `logs-ingress-nginx-hotfix` still exists, delete it first. Elasticsearch does not support renaming an index template in place, so creating `logs-ingress-nginx-ingress-nginx` with the same pattern and priority will fail until the old template is removed.

### 3. Force rollover

Run:

```http
POST logs-ingress-nginx-ingress-nginx/_rollover
```

### 4. Validate

Run:

```http
GET _data_stream/logs-ingress-nginx-ingress-nginx
GET _cat/shards/.ds-logs-ingress-nginx-ingress-nginx-*?v
GET _cat/thread_pool/write?v&h=node_name,active,queue,rejected,completed
```

Expected result:

- the newest backing index has shards `0 p`, `1 p`, `2 p`
- primary shards are spread across `elasticsearch01/02/03`
- ES write queue becomes more balanced

## General Verification

Use these checks during and after mitigation:

```http
GET _cluster/health?pretty
GET _cat/nodes?v&h=name,heap.percent,cpu,load_1m,disk.used_percent
GET _cat/thread_pool/write?v&h=node_name,active,queue,rejected,completed
GET _nodes/stats/indexing_pressure?pretty
```

Good signs:

- Logstash `429` becomes rare or disappears
- `_bulk` timeout frequency drops
- `elasticsearch01` queue keeps decreasing
- `elasticsearch02` and `elasticsearch03` start handling more writes

## Recovery Rollback Plan

Use this section after the cluster is stable again.

Recommended preconditions:

- no sustained `429`
- no recurring `_bulk` timeout bursts
- write queue is stable and low
- new backing indices are using `3` primary shards as expected

### Rollback target

Restore:

- `number_of_replicas` from `0` back to `1`
- `refresh_interval` from `30s` back to `5s` or your normal value

Do not roll back `index.number_of_shards` to `1` for new high-traffic backing indices.

### 1. Restore the template for `logs-svrlog-wallet`

Run:

```http
PUT _index_template/logs-svrlog-wallet
{
  "index_patterns": ["logs-svrlog-wallet*"],
  "data_stream": {},
  "priority": 500,
  "template": {
    "settings": {
      "index.number_of_shards": 3,
      "index.number_of_replicas": 1,
      "index.refresh_interval": "5s"
    }
  }
}
```

### 2. Restore the current write index settings for `logs-svrlog-wallet`

First find the newest backing index:

```http
GET _data_stream/logs-svrlog-wallet
```

Then apply:

```http
PUT <latest-backing-index>/_settings
{
  "index": {
    "number_of_replicas": 1,
    "refresh_interval": "5s"
  }
}
```

### 3. Restore the template for `logs-ingress-nginx-ingress-nginx`

Run:

```http
PUT _index_template/logs-ingress-nginx-ingress-nginx
{
  "index_patterns": ["logs-ingress-nginx-ingress-nginx*"],
  "data_stream": {},
  "priority": 500,
  "template": {
    "settings": {
      "index.number_of_shards": 3,
      "index.number_of_replicas": 1,
      "index.refresh_interval": "5s"
    }
  }
}
```

### 4. Restore the current write index settings for `logs-ingress-nginx-ingress-nginx`

First find the newest backing index:

```http
GET _data_stream/logs-ingress-nginx-ingress-nginx
```

Then apply:

```http
PUT <latest-backing-index>/_settings
{
  "index": {
    "number_of_replicas": 1,
    "refresh_interval": "5s"
  }
}
```

## Optional Full Rollback

Only do this if you intentionally want to remove the dedicated hotfix templates.

Warning:

- removing the templates can cause future rollover indices to fall back to the default `logs` template
- this may reintroduce the single-primary-shard hotspot problem

Commands:

```http
DELETE _index_template/logs-svrlog-wallet
DELETE _index_template/logs-ingress-nginx-ingress-nginx
```

This is usually not recommended for high-throughput log streams.

## Recommended Long-Term State

For high-ingestion log streams, keep:

- `index.number_of_shards = 3`
- `index.number_of_replicas = 1` after the incident
- a dedicated template instead of relying only on the default `logs` template

Consider also:

- increasing ES heap from `16GB` to `24GB` or `30GB` if workload remains high
- keeping Logstash pipeline concurrency conservative
- reviewing other high-volume data streams for the same single-shard pattern

## Capacity and Kafka Retention Guidance

Key capacity conclusion from this incident:

- moving from `1` primary shard to `3` primary shards does not triple storage by itself
- the main storage increase comes from restoring `number_of_replicas` from `0` back to `1`
- based on the incident data discussed here, the known large `0` replica indices were approximately:
  - `logs-svrlog-wallet` total: about `930GB`
  - `traces-apm-default` total: about `575GB`
  - combined additional cluster storage after restoring replicas: about `1.5TB`

Operational interpretation for the current environment:

- in a `3` node cluster, `1.5TB` of extra replica data is roughly `0.5TB` additional disk per node on average
- with `/data` around `9.8TB` total and about `5.8TB` used at the time of review, this still leaves meaningful headroom after replica recovery
- even using a conservative worst-case estimate, disk usage would still be materially below the ES high watermark

Kafka retention guidance:

- do not reduce Kafka log retention from `2 days` to `1 day` only because ES templates were changed to `3` shards and `1` replica
- keep Kafka at `2 days` while the cluster is stabilizing so replay capacity remains available if ES or Logstash falls behind again
- only reconsider reducing Kafka retention if ES node disk usage starts trending toward `80%` to `85%` after replica recovery and shard rebalancing

## Rollover Timing Guidance

After updating a template or lifecycle policy:

- if the current write index is already too large or still using old settings, run a manual rollover immediately instead of waiting for the age condition
- recommended steady-state rollover targets for these hot data streams are:
  - `max_primary_shard_size = 40GB` to `50GB`
  - `max_age = 1d`
- for `3` primary shards, this usually keeps the full backing index around `120GB` to `150GB` before rollover
- if ILM has lifecycle errors, fix the lifecycle problem first because automatic rollover may not happen as expected

## Emergency Stop Order

Use this section when the immediate goal is to reduce ES write pressure as fast as possible.

### Priority 1: Stop non-core Logstash pipelines

Temporarily stop or remove from subscription:

- `tiqmo-Einvoice-logs`
- `tiqmo-middleware`
- `tiqmo-ingress-nginx`

Keep only:

- `tiqmo-svc-logs`

Recommended `tiqmo-svc-logs` runtime settings:

```text
group_id = logstash-svrlog-k8s-20260522
auto_offset_reset = latest
consumer_threads = 1
workers = 1
batch_size = 50 or 100
```

Temporary ES output hosts for `tiqmo-svc-logs`:

```text
http://10.21.104.14:9200
http://10.21.104.15:9200
```

### Priority 2: Stop direct-to-ES APM ingestion if pressure remains high

If `elasticsearch01` remains the hotspot even after Logstash is reduced, stop APM direct ingestion first.

Typical Docker Compose command:

```bash
docker compose stop apm-server
```

If Compose service names are not available, stop the container directly:

```bash
docker stop docker-elk-sp-tiqmo-apm-server-1
```

### Priority 3: Stop metrics / fleet writers if needed

If ES pressure is still high after stopping APM:

```bash
docker compose stop metricbeat fleet-server
```

Or stop containers directly if needed.

### Priority 4: Pause all Logstash temporarily if ES still does not recover

If ES remains overloaded:

```bash
docker compose stop logstash
```

Then wait 10 to 20 minutes and observe:

```http
GET _cluster/health?pretty
GET _cat/thread_pool/write?v&h=node_name,active,queue,rejected,completed
GET _cat/recovery?v
GET _nodes/stats/indexing_pressure?pretty
```

### Priority 5: Remove test recovery noise

If `new-index-name` is only a test index created during split testing, delete it:

```http
DELETE new-index-name
```

This helps remove unnecessary shard allocation and recovery load.

## APM Traces Hotfix

Current incident findings showed that APM traces were still using a single-primary-shard write index and the primary was on `elasticsearch01`.

Example observed write index:

```text
.ds-traces-apm-default-2026.05.22-000999
```

### Fastest temporary action

Stop `apm-server` first if immediate recovery is more important than keeping APM traces real-time.

### If APM ingestion must stay on

#### 1. Reduce pressure on the current APM traces write index

```http
PUT .ds-traces-apm-default-2026.05.22-000999/_settings
{
  "index": {
    "number_of_replicas": 0,
    "refresh_interval": "30s"
  }
}
```

#### 2. Create a dedicated APM traces template

```http
DELETE _index_template/traces-apm-default-hotfix

PUT _index_template/traces-apm-default
{
  "index_patterns": ["traces-apm-default*"],
  "data_stream": {},
  "priority": 1000,
  "template": {
    "settings": {
      "index.number_of_shards": 3,
      "index.number_of_replicas": 1,
      "index.refresh_interval": "5s"
    }
  }
}
```

If `traces-apm-default-hotfix` still exists, delete it first. Elasticsearch does not support renaming an index template in place, so creating `traces-apm-default` with the same pattern and priority will fail until the old template is removed.

#### 3. Force rollover

```http
POST traces-apm-default/_rollover
```

#### 4. Validate

```http
GET _data_stream/traces-apm-default
GET _cat/shards/.ds-traces-apm-default-*?v
```

Expected result:

- newest APM traces backing index has `0 p`, `1 p`, `2 p`
- primaries are spread across `elasticsearch01/02/03`

### Steady-state target for APM traces

When the system is stable again, keep APM traces on `3` primary shards and `1` replica:

```http
PUT _index_template/traces-apm-default
{
  "index_patterns": ["traces-apm-default*"],
  "data_stream": {},
  "priority": 1000,
  "template": {
    "settings": {
      "index.number_of_shards": 3,
      "index.number_of_replicas": 1,
      "index.refresh_interval": "5s"
    }
  }
}
```

Then update the latest backing index if it is still using the temporary emergency settings:

```http
PUT <latest-apm-backing-index>/_settings
{
  "index": {
    "number_of_replicas": 1,
    "refresh_interval": "5s"
  }
}
```

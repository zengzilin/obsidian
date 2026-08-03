# ingress 和gateway api对应关系表

# ⭐ **1. CORE MAPPING TABLE (ALL CONTROLLERS)**

| Ingress Annotation | Meaning | Gateway API Replacement |
| --- | --- | --- |

| `kubernetes.io/ingress.class` | Select ingress controller | `Gateway.spec.gatewayClassName` |
| --- | --- | --- |

| `nginx.ingress.kubernetes.io/rewrite-target` | Path rewrite | `HTTPRoute → filters → URLRewrite` |
| --- | --- | --- |

| `nginx.ingress.kubernetes.io/add-base-url` | Add header | `HTTPRoute → ResponseHeaderModifier` |
| --- | --- | --- |

| `nginx.ingress.kubernetes.io/proxy-body-size` | Request size limit | `BackendPolicy`<br/> (if supported) or implementation-specific |
| --- | --- | --- |

| `nginx.ingress.kubernetes.io/enable-cors` | CORS | `HTTPRoute → ResponseHeaderModifier`<br/> (manual headers) |
| --- | --- | --- |

| `nginx.ingress.kubernetes.io/configuration-snippet` | Custom NGINX config | ❌ No direct equivalent → Must use Gateway extension (Envoy/Tigera) |
| --- | --- | --- |

| `nginx.ingress.kubernetes.io/server-snippet` | Nginx server block injection | ❌ No direct equivalent → Use HeaderModifier or ExtensionRef |
| --- | --- | --- |

| `nginx.ingress.kubernetes.io/ssl-redirect` | Force HTTPS | `HTTPRoute → parentRef (HTTPS only)`<br/> or listener config |
| --- | --- | --- |

| `nginx.ingress.kubernetes.io/from-to-www-redirect` | URL redirect | `HTTPRoute → Redirect`<br/> filter |
| --- | --- | --- |

| `nginx.ingress.kubernetes.io/auth-*` | External auth | `HTTPRoute → ExtensionRef`<br/> (Envoy AuthPolicy) |
| --- | --- | --- |

| `nginx.ingress.kubernetes.io/limit-rps` | Rate limiting | `HTTPRoute → ExtensionRef (RateLimit)` |
| --- | --- | --- |

| `nginx.ingress.kubernetes.io/limit-connections` | Connection limiting | ExtensionRef (Envoy/Kong/etc.) |
| --- | --- | --- |

| `nginx.ingress.kubernetes.io/proxy-read-timeout` | Timeout | `backendRefs.timeout` |
| --- | --- | --- |

| `nginx.ingress.kubernetes.io/proxy-send-timeout` | Timeout | `backendRefs.timeout` |
| --- | --- | --- |

| `nginx.ingress.kubernetes.io/proxy-next-upstream` | Retry | `HTTPRoute.filters → RequestMirror`<br/> or `RetryPolicy`<br/> (Envoy extension) |
| --- | --- | --- |

| `nginx.ingress.kubernetes.io/whitelist-source-range` | IP allow/deny | `HTTPRoute → ExtensionRef (FirewallPolicy)` |
| --- | --- | --- |

| `nginx.ingress.kubernetes.io/upstream-hash-by` | Sticky session | `SessionPersistencePolicy`<br/> (Envoy extension |
| --- | --- | --- |

# ⭐ **2. TLS / CERTIFICATE**

| Ingress Field | Gateway API Equivalent |
| --- | --- |
| `.spec.tls[].secretName` | `Gateway.listeners.tls.certificateRefs.name` |
| `.spec.tls[].hosts` | `Gateway.listeners.hostname` |
| `nginx.ingress.kubernetes.io/ssl-passthrough` | `Gateway.listeners.tls.mode: Passthrough` |

# ⭐ **3. PATH & HOST MATCHING**

| Ingress | Gateway API |
| --- | --- |
| `pathType: Prefix` | `HTTPRoute.matches[].path.type: PathPrefix` |
| `pathType: Exact` | `HTTPRoute.matches[].path.type: Exact` |
| `pathType: ImplementationSpecific` | `HTTPRoute.matches[].path.type: RegularExpression` |
| `host: example.com` | `HTTPRoute.spec.hostnames[]` |
| Multiple paths | Multiple `rules` |

***

# ⭐ **4. HTTP HEADER MANIPULATION**

| Ingress Annotation | Gateway API |
| --- | --- |
| `nginx.ingress.kubernetes.io/add-header` | `ResponseHeaderModifier.add` |
| `nginx.ingress.kubernetes.io/remove-header` | `ResponseHeaderModifier.remove` |
| `nginx.ingress.kubernetes.io/proxy-set-headers` | `RequestHeaderModifier.add / set` |
| `server-snippet`<br/> (headers only) | Convert to header modifier |

# ⭐ \*\*5. REDIRECTS 	\*\*

| Ingress Annotation | Gateway API |
| --- | --- |
| `nginx.ingress.kubernetes.io/permanent-redirect` | `HTTPRoute → RequestRedirect filter` |
| `nginx.ingress.kubernetes.io/temporal-redirect` | `HTTPRoute → RequestRedirect filter (status=302)` |
| `nginx.ingress.kubernetes.io/from-to-www-redirect` | Same as above |

# ⭐ **6. LOAD BALANCING / SESSION**

| Ingress Annotation | Gateway API |
| --- | --- |
| `nginx.ingress.kubernetes.io/load-balance: ip_hash` | ExtensionRef (Envoy LBPolicy) |
| `nginx.ingress.kubernetes.io/load-balance: round_robin` | Default behavior |
| `nginx.ingress.kubernetes.io/upstream-hash-by` | ExtensionRef (session persistence) |
| `nginx.ingress.kubernetes.io/session-cookie-name` | PolicyAttachment (if supported) |

# ⭐ **7. RATE LIMITING / SECURITY**

| Ingress Annotation | Gateway API |
| --- | --- |
| `nginx.ingress.kubernetes.io/limit-rps` | ExtensionRef (Envoy RateLimit) |
| `nginx.ingress.kubernetes.io/limit-connections` | ExtensionRef |
| `nginx.ingress.kubernetes.io/modsecurity-*` | No native Gateway API support → extension |
| `nginx.ingress.kubernetes.io/server-snippet`<br/> (security rules) | Must migrate manually → |

# ⭐ **8. REQUEST SIZE / BODY LIMIT**

| Ingress Annotation | Gateway Equivalent |
| --- | --- |
| `nginx.ingress.kubernetes.io/proxy-body-size` | BackendPolicy (if implementation supports it) |

# ⭐ **9. TIMEOUTS**

| Ingress Annotation | Gateway API |
| --- | --- |
| `proxy-read-timeout` | `backendRefs.timeout` |
| `proxy-send-timeout` | `backendRefs.timeout` |
| `proxy-connect-timeout` | Gateway Listener timeout parameters (implementation-specific) |

# ⭐ **10. INGRESS BACKEND → HTTPROUTE BACKENDREF**

| Ingress | Gateway API |
| --- | --- |
| `backend.service.name` | `backendRefs.name` |
| `backend.service.port.number` | `backendRefs.port` |
| Weight (annotation) | `backendRefs.weight` |


> 更新: 2025-12-02 09:08:33  
> 原文: <https://www.yuque.com/zilin-hw8cn/po91to/muq55ucc59uug4cg>
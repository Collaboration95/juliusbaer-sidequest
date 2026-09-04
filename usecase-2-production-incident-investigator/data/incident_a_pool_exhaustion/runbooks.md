# Runbooks

## RB-014: Payment Gateway Timeout Spike

**Symptoms**: `ConnectionPoolTimeoutException` appearing in
`payment-gateway-adapter` logs; intermittent (not total) payment
failures; `payment-service` logging `GATEWAY_TIMEOUT`.

**Diagnostic steps**:
1. Check `payment-gateway-adapter` connection pool utilization metrics
   for saturation.
2. Check recent deployments touching `payment-gateway-adapter`
   (see deployment history) for pool size or timeout configuration changes.
3. Compare the current pool size configuration against the historical
   baseline (50 connections).

**Remediation**: revert the pool size to the prior baseline value, or
scale the pool size upward to match current traffic; redeploy
`payment-gateway-adapter`.

**Typical MTTR: 20 minutes.**

## RB-002: Elevated Notification Queue Depth

**Symptoms**: `notification-service` logging elevated queue depth
warnings.

**Diagnostic steps**: check consumer count and downstream email provider
latency.

**Remediation**: scale notification-service consumers.

**Typical MTTR: 15 minutes.**

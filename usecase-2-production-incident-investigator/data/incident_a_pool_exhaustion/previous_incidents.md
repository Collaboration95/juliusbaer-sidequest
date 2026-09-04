# Previous incidents

## INC-2031 (2026-03-14)

**Summary**: Intermittent payment failures, `payment-gateway-adapter`
logging `ConnectionPoolTimeoutException` under normal (not elevated)
traffic.

**Root cause**: connection pool size was set too low for peak traffic
during a configuration change made in that day's deploy.

**Resolution**: reverted the pool size to its prior value (50) and
redeployed.

**MTTR**: 22 minutes (from first error log to resolution deploy landing).

## INC-1987 (2026-01-09)

**Summary**: `order-service` returned elevated 500 rates for ~10 minutes
during a database failover. Unrelated to payment processing.

**Root cause**: database connection string not updated fast enough by
the failover automation.

**Resolution**: manual failover trigger.

**MTTR**: 11 minutes.

# Deployment history

| Version | Timestamp (UTC) | Component | Change |
|---|---|---|---|
| v2.3.8 | 2026-08-18 09:00 | order-service | Bug fix: duplicate order creation on retry |
| v2.4.0 | 2026-08-20 10:00 | payment-service | Added client-side retry logic for transient gateway errors |
| **v2.4.1** | **2026-09-02 14:30** | **payment-gateway-adapter** | **Reduced connection pool size from 50 to 10 (memory optimization for the upcoming cost-reduction initiative)** |
| v2.4.2 | 2026-09-02 16:10 | notification-service | Updated email template styling (unrelated) |

No other deployments touched `payment-gateway-adapter` in the two weeks
prior to v2.4.1.

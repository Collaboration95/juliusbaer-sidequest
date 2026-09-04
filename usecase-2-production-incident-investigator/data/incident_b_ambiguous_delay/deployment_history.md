# Deployment history

| Version | Timestamp (UTC) | Component | Change |
|---|---|---|---|
| v2.4.0 | 2026-08-20 10:00 | payment-service | Added client-side retry logic for transient gateway errors |
| v2.4.1 | 2026-09-02 14:30 | payment-gateway-adapter | Reduced connection pool size from 50 to 10 |

No deployment touched `notification-service` in the month before this
incident (2026-08-15). The two entries above both post-date this
incident and involve unrelated components — there is no deployment
correlated with the email delay pattern.

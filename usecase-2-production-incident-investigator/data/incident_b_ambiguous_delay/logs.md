# Application logs — 2026-08-15

```
2026-08-15 08:55:02 INFO  order-service            Order created order_id=ORD-55021
2026-08-15 08:55:03 INFO  payment-gateway-adapter  Charge succeeded order_id=ORD-55021
2026-08-15 08:55:03 INFO  notification-service     Email queued order_id=ORD-55021
2026-08-15 09:12:41 WARN  web-frontend             Checkout page render time 3900ms (elevated)
2026-08-15 09:41:38 INFO  notification-service     Email sent order_id=ORD-55021
2026-08-15 10:02:11 INFO  order-service            Order created order_id=ORD-55040
2026-08-15 10:02:12 INFO  payment-gateway-adapter  Charge succeeded order_id=ORD-55040
2026-08-15 10:02:12 INFO  notification-service     Email queued order_id=ORD-55040
2026-08-15 10:20:55 INFO  order-service            Duplicate order create attempt suppressed (idempotency key already used) order_id=ORD-55036
2026-08-15 10:44:38 INFO  notification-service     Email sent order_id=ORD-55040
2026-08-15 11:05:14 INFO  search-service           Reindex lag 6m10s behind catalog
2026-08-15 11:10:02 WARN  notification-service     Queue depth elevated: 340 messages
2026-08-15 11:15:19 INFO  order-service            Order created order_id=ORD-55071
2026-08-15 11:15:20 INFO  payment-gateway-adapter  Charge succeeded order_id=ORD-55071
2026-08-15 11:15:20 INFO  notification-service     Email queued order_id=ORD-55071
2026-08-15 11:48:03 INFO  notification-service     Email rendered using fallback template (webmail compatibility) order_id=ORD-55055
2026-08-15 12:30:44 INFO  notification-service     Email sent order_id=ORD-55071
2026-08-15 12:50:27 WARN  payment-gateway-adapter  Refund webhook delivery delayed 180s merchant_id=MCH-2209
2026-08-15 13:02:07 INFO  order-service            Order created order_id=ORD-55090
2026-08-15 13:02:08 INFO  payment-gateway-adapter  Charge succeeded order_id=ORD-55090
2026-08-15 13:02:08 INFO  notification-service     Email queued order_id=ORD-55090
2026-08-15 13:30:19 INFO  auth-service             Session expired after 600s inactivity user_id=USR-40188
2026-08-15 13:58:51 INFO  notification-service     Email sent order_id=ORD-55090
```

Delays are consistently 40–75 minutes between "Email queued" and
"Email sent". No `ERROR`-level entries anywhere in this window, no
exceptions, no failed sends — every email does eventually go out. Payment
and order creation both complete normally and quickly. The log also
carries a handful of entries from unrelated systems (checkout rendering,
duplicate-order suppression, search indexing, email templating, refund
webhooks, auth sessions) — background noise from other known issues, none
of which explain the delay pattern.

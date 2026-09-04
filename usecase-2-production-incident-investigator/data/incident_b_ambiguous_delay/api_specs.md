# API specification (excerpt)

`notification-service` has no public HTTP API — it is a queue consumer
only, triggered internally by events published from `order-service` and
`payment-service`. There is no documented SLA for email delivery latency
in the current API specification; this is itself a gap worth noting.

## `POST /api/payments/charge`

Owned by `payment-service`. Unrelated to this incident based on the
available logs (all charges in the log window succeeded within
milliseconds).

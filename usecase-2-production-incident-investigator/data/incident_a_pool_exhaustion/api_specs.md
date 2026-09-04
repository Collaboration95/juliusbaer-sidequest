# API specification (excerpt)

## `POST /api/payments/charge`

Owned by: `payment-service`, delegates to `payment-gateway-adapter`.

| Field | Type | Notes |
|---|---|---|
| `order_id` | string | required |
| `amount_cents` | integer | required |
| `currency` | string | ISO 4217 |

**Timeout**: the adapter waits up to 5000ms to acquire a pooled connection
to the Payment Provider before failing the request with
`GATEWAY_TIMEOUT`. There is no automatic retry at this layer — retries,
if any, are the caller's responsibility.

**Response codes**: `200 OK`, `402 PAYMENT_DECLINED`, `504 GATEWAY_TIMEOUT`.

## `POST /api/orders`

Owned by `order-service`. Independent of the payment path; does not call
`payment-gateway-adapter`.

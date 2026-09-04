# Architecture overview

```
Client
  -> API Gateway
       -> payment-service       (validates and orchestrates charge requests)
            -> payment-gateway-adapter   (maintains a connection pool to the
                                           external Payment Provider; handles
                                           request signing and retries)
                 -> Payment Provider (external, third-party)
       -> order-service          (creates and tracks orders)
       -> notification-service   (sends order/payment confirmation emails)
```

## Components

- **payment-service**: stateless, horizontally scaled, calls
  `payment-gateway-adapter` synchronously for every charge.
- **payment-gateway-adapter**: owns a bounded connection pool to the
  external Payment Provider's API. Pool size is a static configuration
  value, set at deploy time. When the pool is exhausted, new requests
  wait up to a fixed timeout and then fail with
  `ConnectionPoolTimeoutException`.
- **order-service**: independent of payment-service; creates orders
  before payment is attempted.
- **notification-service**: sends emails via a message queue; independent
  of the payment path.

`payment-service` and `payment-gateway-adapter` are the only components in
the direct path of a charge request.

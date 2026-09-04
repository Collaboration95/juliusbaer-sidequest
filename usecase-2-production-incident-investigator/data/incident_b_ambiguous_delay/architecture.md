# Architecture overview

```
Client
  -> API Gateway
       -> payment-service       (validates and orchestrates charge requests)
            -> payment-gateway-adapter   (connection pool to Payment Provider)
       -> order-service          (creates and tracks orders)
       -> notification-service   (consumes an internal message queue and
                                   sends order/payment confirmation emails
                                   via a third-party email provider)
```

## Components

- **notification-service**: subscribes to an internal message queue;
  each order/payment event is queued as a message, and a pool of
  consumer workers dequeues and sends the corresponding email. Consumer
  pool size and the third-party email provider's own latency are both
  outside this service's direct control and are not currently
  instrumented with per-stage timing.
- **payment-service** / **payment-gateway-adapter** / **order-service**:
  independent of the notification path; no evidence in this incident's
  logs of any failure or slowdown in these components.

# Runbooks

## RB-002: Elevated Notification Queue Depth

**Symptoms**: `notification-service` logging elevated queue depth
warnings.

**Diagnostic steps**: check consumer count and downstream email provider
latency. Neither is currently exposed as a metric — this runbook is
incomplete pending better instrumentation.

**Remediation**: scale notification-service consumers (unverified whether
this is actually the bottleneck).

**Typical MTTR: 15 minutes.** (Note: this MTTR figure is from a
different, unconfirmed prior occurrence and may not apply here.)

No other runbook in the current set addresses email delivery latency
specifically.

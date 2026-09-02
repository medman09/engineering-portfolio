# Failure modes

This document is intentionally updated as the demonstrator gains real PyLabRobot adapters.

| Failure | Classification | Initial behavior | Evidence to add |
| --- | --- | --- | --- |
| Temporary liquid-handler timeout | Retryable | bounded retry, then fail | unit + adapter integration test |
| Temporary plate-reader timeout | Retryable | bounded retry, then fail | unit + adapter integration test |
| Invalid workflow start state | Logic error | reject command | unit test |
| Permanent device/configuration error | Non-retryable | fail immediately | unit test |
| Exception during workflow | Unexpected | mark failed and cleanup | unit test |
| Exception during one device cleanup | Cleanup fault | continue cleanup of remaining devices and record error | unit test |
| Device unavailable after successful previous step | Recoverability case | preserve completed step; pause/recovery policy to be designed | M3 |
| Process crash / restart | Persistence case | not yet implemented | M3/M4 |

## Retry rule

Retries must be:

- bounded;
- applied only to errors classified as transient;
- observable in the event log;
- unable to create duplicate unsafe physical actions without explicit consideration.

The current fake-device tests validate the control structure. Before real hardware is ever connected, idempotency and device-specific recovery semantics must be reviewed for each operation.

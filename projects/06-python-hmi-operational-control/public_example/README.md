# Public Python example — background control for a hardware-facing HMI

This directory is a **fresh, device-agnostic public reconstruction** of one of the reliability patterns used in the private operational HMI project.

It is intentionally not a copy of the production repository. Vehicle-specific endpoints, tokens, command routes, UI code and deployment details are excluded. The purpose is to make the software-engineering approach inspectable without publishing professional/private implementation details.

## What it demonstrates

- dependency injection through a small `DeviceApi` protocol
- background device I/O without blocking the caller/UI thread
- one status poll in flight at a time
- coalescing of refresh requests instead of fixed-rate overlap
- request-generation based rejection of stale poll results
- background command execution
- callback handoff back to the caller/UI thread
- explicit error propagation
- worker tracking and clean shutdown
- deterministic tests with a fake device API

## Files

- [`background_controller.py`](background_controller.py) — the representative implementation
- [`test_background_controller.py`](test_background_controller.py) — focused behavioral tests

## Run the tests

From this directory:

```bash
python3 -m unittest -v
```

The example uses only the Python standard library.

## Validation

Before publishing this example I ran the test suite locally:

```text
5 tests passed
```

The tests cover nominal polling, prevention/coalescing of overlapping polls, stale-result rejection after a command, error reporting and shutdown behavior.

## Relationship to the real project

The private HMI contains a larger application with configuration validation, HTTP bridge integration, explicit application state, UI pages, connected/disconnected loopback validation and a broader regression suite. This public example focuses on one technically representative part: **making asynchronous communication with a physical-system backend predictable and testable**.

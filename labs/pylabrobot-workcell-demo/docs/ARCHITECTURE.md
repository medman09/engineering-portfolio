# Architecture

## Design goal

Keep the workcell workflow independent from a specific laboratory robot or instrument implementation.

```text
Workflow / state machine
        |
        v
Small Python device interfaces
        |
        v
PyLabRobot-specific adapters
        |
        v
PyLabRobot frontend/backend
        |
        v
Simulator or real device
```

## Why this boundary exists

The orchestrator should reason about engineering operations such as `transfer_sample()` and `read_plate()`, not about a vendor protocol, deck command, socket, USB endpoint, or simulator class.

Benefits:

- unit tests do not require PyLabRobot or physical hardware;
- device-specific changes remain localized;
- simulated and real backends can share workflow logic;
- failures can be classified consistently at the device boundary;
- the design can evolve from device-free simulation to physical equipment without rewriting the state machine.

## Current core

`WorkcellOrchestrator`
: owns workflow state, sequencing, retry policy and cleanup.

`LiquidHandlerPort`
: minimal contract needed by the workflow for liquid handling.

`PlateReaderPort`
: minimal contract needed by the workflow for measurement.

`FakeLiquidHandler` / `FakePlateReader`
: deterministic devices used to test nominal and failure paths.

## Planned PyLabRobot adapters

The liquid-handler adapter will use PyLabRobot's `LiquidHandler` with `LiquidHandlerChatterboxBackend` for device-free testing.

The plate-reader adapter will isolate the currently available simulated plate-reader API behind `PlateReaderPort`. Any use of a PyLabRobot `legacy` module must remain inside that adapter so the rest of the project does not depend on legacy package structure.

## Engineering principle

Framework types are implementation details at the adapter boundary. Workcell behavior, failure handling and acceptance tests should remain understandable without knowing a specific vendor SDK.

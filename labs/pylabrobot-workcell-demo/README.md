# Simulated Lab Workcell — PyLabRobot

Personal technical demonstrator for learning lab-automation patterns with PyLabRobot and transferring existing hardware/software integration experience into a laboratory context.

> **Scope:** device-free simulation only. No physical laboratory equipment is used or claimed.

## What this project is meant to demonstrate

- rapid adoption of an unfamiliar hardware-automation framework;
- clean separation between workflow/orchestration logic and device-specific drivers;
- Python software controlling simulated physical devices;
- explicit state management and interface contracts;
- timeout/retry/failure-recovery thinking;
- structured logging and testability;
- AI-native development with human engineering ownership.

## Target workcell

```text
                  WorkcellOrchestrator
                         |
              +----------+----------+
              |                     |
              v                     v
       LiquidHandlerPort       PlateReaderPort
              |                     |
              v                     v
       PyLabRobot adapter      PyLabRobot adapter
              |                     |
              v                     v
    simulated liquid handler  simulated plate reader
```

Nominal workflow:

```text
INITIALIZING
    |
    v
READY
    |
    v
PIPETTING
    |
    v
READING
    |
    v
COMPLETED
```

Failure states will include `RETRYING`, `PAUSED`, and `FAILED`.

## Engineering approach

The project deliberately keeps the orchestration layer independent from PyLabRobot-specific classes. Device integrations implement small Python interfaces and can later be replaced by real hardware adapters without rewriting the workflow logic.

This mirrors a pattern already used in other physical-systems projects: generic command/state logic -> device adapter -> protocol/backend -> physical system.

## Milestones

### M0 — Architecture and testable core

- define workcell states and interfaces;
- implement a minimal orchestrator;
- implement deterministic fake devices;
- test nominal operation and retry exhaustion;
- document architecture, failure modes, and AI-assisted workflow.

### M1 — PyLabRobot liquid-handler adapter

- integrate `LiquidHandler` with `LiquidHandlerChatterboxBackend`;
- create a simulated deck/resources setup;
- implement a simple transfer operation;
- validate setup/operation/stop lifecycle.

### M2 — Simulated plate-reader adapter

- integrate a device-free plate-reader backend where supported by the current PyLabRobot API;
- isolate any `legacy` API usage inside the adapter;
- return deterministic measurement data to the workflow.

### M3 — Reliability

- explicit timeout policy;
- bounded retries;
- invalid-state rejection;
- failure isolation;
- pause/recovery behavior;
- cleanup after exceptions.

### M4 — Observability and evidence

- structured event log;
- test matrix for nominal/error/boundary paths;
- architecture and sequence diagrams;
- capture of simulator/visualizer output where useful.

### M5 — Portfolio-ready case study

- summarize problem, architecture, engineering decisions, tests, limitations and transferable learning;
- document concrete examples of coding-agent mistakes and how they were detected/corrected;
- clearly distinguish simulated lab automation from real hardware experience.

## What I should be able to defend in an interview

At completion I should be able to explain, without relying on an AI assistant:

1. what a PyLabRobot frontend/backend is;
2. why orchestration is separated from device drivers;
3. the control and data flow through the workcell;
4. how timeout/retry/recovery behavior is defined;
5. why some errors are retryable and others are not;
6. how tests avoid depending on physical hardware;
7. how a simulated adapter would be replaced by a real hardware backend;
8. what coding agents implemented versus what engineering decisions I retained;
9. at least two cases where generated code or assumptions were incorrect;
10. current limitations and the next engineering step.

## Current status

**M0 in progress.** The first implementation focuses on a deterministic, testable orchestration core before connecting PyLabRobot-specific adapters.

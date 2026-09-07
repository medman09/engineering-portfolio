# Public C++ example — protocol validation and codec boundary

This directory is a **fresh public reconstruction** of the protocol/driver pattern used in the private vehicle-interface project.

It does **not** contain real vehicle CAN identifiers, scaling values, payload layouts, heartbeat behavior or safety-sensitive command details. All identifiers and protocol values in this example are synthetic.

The goal is to make the software-engineering approach inspectable without publishing proprietary or operational information.

## What it demonstrates

- a small C++17 protocol boundary independent of ROS 2
- explicit frame metadata and validation results
- rejection of unsupported identifiers, invalid DLC and invalid frame metadata
- byte-level signed measurement decoding
- command encoding with input validation and range checks
- deterministic tests around nominal and error paths
- a minimal CMake/CTest build that can run without vehicle hardware

## Files

- [`protocol_codec.hpp`](protocol_codec.hpp) — public interface and data types
- [`protocol_codec.cpp`](protocol_codec.cpp) — validation, decoding and encoding logic
- [`test_protocol_codec.cpp`](test_protocol_codec.cpp) — focused executable tests
- [`CMakeLists.txt`](CMakeLists.txt) — standalone C++17 build and CTest configuration

## Build and test

```bash
cmake -S . -B build
cmake --build build
ctest --test-dir build --output-on-failure
```

## Validation

Before publishing this example, I built it locally with warnings enabled and ran CTest successfully:

```text
100% tests passed, 0 tests failed
```

## Relationship to the real project

The private vehicle interface is substantially larger and includes real CAN transport, vehicle-specific command/status behavior, ROS 2 / Autoware integration, heartbeat/state handling and physical validation.

This public example isolates one transferable engineering pattern: **keep binary protocol handling behind a small testable boundary, reject malformed input before it can update system state, and verify conversion behavior independently from the robotics framework and the physical machine**.

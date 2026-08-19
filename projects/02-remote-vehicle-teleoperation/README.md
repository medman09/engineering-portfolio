# Remote Vehicle Teleoperation Platform

[← Back to portfolio](../../README.md)

## Overview

The objective was to support remote driving and tele-assisted operation of an automated shuttle over mobile networks.

The system combined:

- six onboard cameras
- an NVIDIA Jetson embedded computer
- low-latency video transport
- an operator station
- remote control commands
- vehicle feedback/status
- ROS 2 and CAN interfaces

The main engineering challenge was not one isolated software module; it was making **video, networking, operator interaction and vehicle control work together on a real platform**.

---

## System architecture

```mermaid
flowchart LR
    CAM[6 onboard cameras] --> JET[NVIDIA Jetson]
    JET --> VID[GStreamer / WebRTC video]
    VID --> NET[4G / 5G network]
    NET --> STA[Operator station]
    STA --> GUI[Qt-based GUI]
    STA --> CMD[Remote control input]
    CMD --> NET
    NET --> VC[Vehicle-side control interface]
    VC --> ROS[ROS 2]
    ROS --> CAN[CAN vehicle interface]
    CAN --> VEH[Shuttle]
    VEH --> FB[Vehicle feedback]
    FB --> STA
```

Internal IP addresses, VPN credentials and proprietary vehicle mappings are intentionally excluded.

---

## My contribution

My work focused on the end-to-end integration:

- camera and onboard-compute integration
- video-pipeline setup and testing
- operator-side GUI integration
- remote command path
- vehicle feedback/status path
- ROS 2 / CAN connection to the vehicle
- network testing over 4G/5G
- latency measurement
- real-vehicle test support and troubleshooting

Software components included Python, C++ and Qt code. Parts of implementation and refactoring were produced with AI-assisted development; my responsibility was the architecture, integration, adaptation, debugging and validation on the real system.

---

## Engineering challenges

### Low-latency video

Teleoperation requires a different design mindset from ordinary video streaming. The main trade-offs are:

- image quality
- bitrate
- frame rate
- latency
- packet loss sensitivity
- network variability

The system was tested over mobile networks and tuned for practical driving/supervision rather than maximum visual quality.

### Network behavior

A later dedicated prototype also reproduced an important WebRTC troubleshooting case over VPN: the signaling and ICE connection could be established while full video frames were not reconstructed reliably.

A reduced sender profile with approximately:

- 640 × 360 video
- 15 fps
- VP8 around 250 kbit/s
- RTP MTU around 1200 bytes

was validated as a practical workaround for the lab network conditions.

This is an example of the type of **system troubleshooting** I am comfortable with: separate signaling, transport, decoding and application behavior until the failure mechanism becomes clear.

### Vehicle-control safety

Remote driving is not only a networking problem. A usable design needs to consider:

- stale/lost commands
- operator intent
- vehicle feedback
- enabling/disabling control
- communication loss
- safe fallback behavior
- validation before real driving

---

## Results

- real remote-driving / tele-assisted experiments supported on the shuttle
- six-camera onboard setup
- NVIDIA Jetson-based video processing/streaming
- 4G/5G communication trials
- approximately **80 ms round-trip time** observed under favorable network conditions
- platform used to support applied research related to remote driving of automated vehicles

---

## Technologies

`ROS 2` · `CAN` · `NVIDIA Jetson` · `GStreamer` · `WebRTC` · `Qt` · `C++` · `Python` · `4G/5G` · `Linux`

---

## What I can defend technically

I can explain and defend:

- end-to-end teleoperation architecture
- why video latency matters for remote driving
- the data path from operator input to vehicle CAN
- the return path for vehicle state
- practical GStreamer/WebRTC integration
- network trade-offs and troubleshooting
- test strategy and real-system validation

I do not position myself as a WebRTC protocol-stack developer or advanced concurrent-C++ specialist.

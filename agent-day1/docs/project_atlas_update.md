# Project Atlas - Status Update & Technical Overview

**Project Name:** Project Atlas (AMR-500 Heavy Payload Autonomous Pallet Mover)  
**Project Owner / Technical Lead:** Marcus Chen (`marcus.c@acmerobotics.internal`)  
**Product Manager:** Sarah Jenkins  
**Last Updated:** September 10, 2026  
**Status:** In Progress / On Track for Phase 3  

---

## 1. Project Objective
Project Atlas is Acme Robotics' flagship heavy-duty autonomous mobile robot designed to transport pallets up to 1,200 kg inside distribution centers.

## 2. Technical Stack
- **OS & Framework:** Ubuntu 22.04 LTS with ROS 2 Humble.
- **Core Navigation:** Custom 2D/3D LiDAR-SLAM pipeline built in Rust for high-throughput localization.
- **Fleet Orchestration:** WebRTC and MQTT connection to Acme Central Fleet Dispatcher.
- **Safety System:** dual SICK safety scanners certified to PLd / SIL2.

## 3. Current Milestones & Test Results
- Phase 2 testing concluded at the Pune testing facility on September 8, 2026.
- Achieved **98.4% obstacle avoidance success rate** in dense dynamic clutter.
- Mean time between interventions (MTBI) measured at 14.2 operating hours.

## 4. Upcoming Pilot Deployment
- A 4-robot beta pilot is slated for deployment at the **Apex Logistics distribution center (Pune facility)** on **October 15, 2026**.
- Pre-commissioning sensor calibration will take place on-site starting October 5, 2026.

## 5. Current Blockers & Dependencies
- Awaiting motor driver firmware patch `v2.4` from hardware supplier Shenzhen Robotics Components Ltd.
- Interim project handover scheduled for late September due to planned staff leave.

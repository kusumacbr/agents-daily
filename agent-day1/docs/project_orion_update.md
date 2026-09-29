# Project Orion - Status Update & Architecture Notes

**Project Name:** Project Orion (Intelligent Robotic Pick-and-Place Cell)  
**Project Owner / Technical Lead:** Ananya Rao (`ananya.r@acmerobotics.internal`)  
**Department:** Perception & Manipulation Group  
**Last Updated:** September 12, 2026  
**Status:** In Active Development (Pre-Alpha)  

---

## 1. Project Scope
Project Orion focuses on an automated robotic arm station capable of picking, orienting, and sorting un-singulated parcel packages and e-commerce SKUs directly from conveyor belts into sortation bins.

## 2. Hardware Architecture & Edge Compute
- **Manipulator:** Universal Robots UR10e 6-axis cobot arm.
- **End-Effector:** Custom pneumatic vacuum suction array with active flow sensing.
- **Vision Sensors:** Dual Intel RealSense D435i stereo depth sensors paired with an overhead Basler ace 2 gigabit color camera.
- **Edge Compute Engine:** **NVIDIA Jetson Orin AGX (64GB)** module running real-time TensorRT model inference for 6-DoF pose estimation.

## 3. Performance Benchmarks
- **Target Cycle Time:** 2.8 seconds per pick-and-place cycle.
- **Current Achieved Time:** 3.1 seconds (reduced from 3.6s following TensorRT optimization).
- **Pick Success Rate:** 96.2% on standard corrugated boxes; 89.1% on deformable polybags.

## 4. Key Deadlines
- System integration with Project Atlas fleet dispatcher: October 28, 2026.
- Formal Factory Acceptance Test (FAT): **November 12, 2026**.

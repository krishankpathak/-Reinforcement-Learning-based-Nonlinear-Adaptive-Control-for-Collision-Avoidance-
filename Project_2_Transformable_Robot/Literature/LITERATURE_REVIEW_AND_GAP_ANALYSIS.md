# Systematic Literature Review & Research Gap Analysis: Project 2
**Topic:** Generative Design, Multiphysics Modeling, and Aeromechanical Analysis of a Transformable Flying and Walking Inspection Robot

---

## 1. Domain Overview & Taxonomy
Infrastructure inspection in complex environments (e.g., offshore oil platforms, nuclear containment facilities, long-span bridge truss networks, and narrow culverts) imposes mutually conflicting mobility constraints. Unmanned Aerial Vehicles (UAVs) provide rapid vertical transit to elevated structures but suffer from severe battery depletion during hover (endurance typically $< 25\text{ minutes}$) and vulnerability to aerodynamic turbulence near wall boundaries. Conversely, Unmanned Ground Vehicles (UGVs) and legged crawlers achieve orders-of-magnitude higher operational endurance and steady physical contact for non-destructive testing (NDT), but cannot negotiate vertical cliffs, severed stairwells, or structural chasms.

This has stimulated research into **hybrid aerial-terrestrial / multimodal robotic systems**.

---

## 2. Comprehensive Literature Review & Comparison Matrix

| Ref | Authors & Year | Venue / Platform | Locomotion Modes | Transformation Mechanism | Total Actuators / DOFs | Structural Efficiency (Payload/Mass) | Terrestrial Stability | Aerodynamic Interference | Critical Engineering Limitations |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **[R10]** | Zarrouk et al. (2019) | *IEEE T-RO*, F-STAR | Quadrotor flight + Wheeled crawling | Sprawl angle adjustment via central spur gear | 4 flight + 1 morph + 2 drive = 7 motors | $0.18$ (Rigid chassis) | Low (Prone to high-center tipping on rubble) | High drag in flight due to exposed wheels | Uses passive wheels rather than articulated legs; cannot step over pipes or negotiate irregular industrial grating. |
| **[R11]** | Korpela et al. (2018) | *IEEE ICRA*, Transformable Aerial Manipulator | Quadrotor + Dual 3-DOF arms | Compliant robotic arms mounted underneath | 4 flight + 6 arm servos = 10 actuators | $0.12$ (Severe mass penalty) | None (Tethered ground perching only) | Arm wake causes $14\%$ thrust reduction | Heavy independent appendages drastically reduce flight endurance to $< 7\text{ min}$; arms cannot bear walking impact loads. |
| **[R12]** | Zhao et al. (2018/2021) | *IEEE/ASME T-MECH*, Aerial-Ground Legged Robot | Multirotor + 2-DOF parallel leg gear | 4-bar linkage deployable landing skids | 4 flight + 4 linear actuators = 8 actuators | $0.15$ | Moderate (Planar trot only) | Symmetric | Linear leg deployment adds deadweight without dual-use mechanical integration; high actuation stress concentrations. |
| **[R13]** | Saldaña et al. (2020) | *IEEE T-RO*, ModQuad-DoF | Modulating quadrotor structure | Articulated modular docking cages | 4 flight + 2 docking = 6 per module | $0.14$ | None | Severe multi-rotor wake turbulence | Lacks terrestrial crawling entirely; collective reconfiguration requires multi-agent assembly rather than single-agent multi-modality. |
| **[R14]** | Kalantari et al. (2020) | *Science Robotics*, D-STAR | Bi-copter + Roll-cage locomotion | Reorienting passive outer spherical shell | 2 flight + 2 tilt = 4 actuators | $0.22$ | Rolling only (No discrete foot placement) | Heavy aerodynamic drag from cage in forward flight | Rolling cage impedes direct sensor access for ultrasonic or eddy-current contact inspection probes. |
| **[R15]** | Bjelonic et al. (2020) | *IEEE RA-L*, ANYmal on Wheels | Legged-Wheeled Quadruped | Non-morphing hybrid drive on leg tips | 12 joint motors + 4 hub motors = 16 | $0.28$ | High | N/A (Ground only) | Purely ground-based ($> 45\text{ kg}$); zero vertical obstacle flight capability. |

---

## 3. The Identified Research Gap

An engineering breakdown of existing aerial-terrestrial robots reveals two polarized paradigms:
1. **Parasitic Appendage Addition:** Attaching independent crawling legs or rolling cages beneath standard drone frames ([R11], [R12]). This introduces passive structural deadweight, drastically degrading flight endurance and payload capacity.
2. **Kinematically Restricted Mobility:** Using wheels or passive rolling cages ([R10], [R14]) which cannot navigate discrete industrial obstacles (steps, pipes, grating) and prevent direct sensor contact.

> **The Research Gap:** There is an absence of an **integrated, kinematically shared rotor-arm morphology** that operates with minimal dedicated transformation actuation, where the multirotor propulsion arms themselves mechanically reorient through a bi-stable high-torque linkage to become an articulated walking quadruped. Furthermore, current literature lacks a unified multiphysics modeling methodology that co-optimizes the **aerodynamic prop-wash interference during hover** and the **structural dynamic impact stress during legged contact transitions** through generative topology optimization.

---

## 4. Proposed Solution in Project 2
Project 2 resolves this bottleneck through:
1. **Dual-Use Articulated Rotor-Leg Kinematics:** A 4-limb symmetric architecture where each multirotor boom serves as an active leg segment, driven by high-reduction planetary servos capable of holding rigid flight geometry and articulating dynamic walking gaits.
2. **Generative Topology Optimization:** Finite element structural synthesis minimizing arm compliance under 4g dynamic landing loads while maintaining hollow internal channels for cabling and reducing aerodynamic drag profiles.
3. **Multiphysics Validation:** Simultaneous simulation of 6-DOF aerial flight, actuator-disk downwash wake interactions, and ZMP-stable quadruped crawling for close-range industrial ultrasonic inspection.

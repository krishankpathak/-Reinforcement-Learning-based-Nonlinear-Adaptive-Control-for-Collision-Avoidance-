# Experiment Status & Physical Validation Roadmap
**Distinguishing Completed Computational Simulations from Proposed Hardware Trials**

---

## 1. Project 1: Multi-Agent Quadruped Safety & Navigation

| Experiment Index | Description | Methodological Target | Status | Summary of Empirical Findings |
| :--- | :--- | :--- | :---: | :--- |
| **Exp A** | Variable-Friction Braking | Estimator RMSE & stopping distance | **COMPLETED** | Verified across $\mu \in [0.2, 0.8]$. Estimator converges in $< 0.35\text{ s}$; RMSE $\le 0.42\text{ m/s}^2$; certified lower bound $\underline{a}_{\mathrm{brake}}$ covers true limit $100\%$ of the time. |
| **Exp B** | Human Pedestrian Crossing | Dynamic avoidance under low friction | **COMPLETED** | Tested with dynamic crossing pedestrians ($\mu=0.25$ vs $0.75$). Maintained safe margin $\ge 1.18\text{ m}$ without skidding. |
| **Exp C** | Two-Quadruped Corridor Navigation | Deadlock & conflict resolution | **COMPLETED** | Evaluated opposing quadrupeds in narrow $2.0\text{ m}$ corridor. Mutual clearance certified above $1.12\text{ m}$ with zero deadlocks. |
| **Exp D** | Multi-Robot Crowd Interaction | Scaled coordination in dense arena | **COMPLETED** | 2 quadrupeds + 4 pedestrians navigating simultaneously. Achieved $100\%$ goal completion rate with zero collisions. |
| **Exp E** | Partial Observability & Occlusion | Tracking dropout resilience | **COMPLETED** | Robust HOCBF buffer maintained forward invariance even with $0.2\text{ s}$ simulated tracking sensor latency. |
| **Exp F** | Communication-Free Execution | Decentralized execution integrity | **COMPLETED** | Zero wireless telemetry exchanged between agents; decisions purely based on local observation and conservative peer bounds. |
| **Exp G** | Combined Multi-Source Uncertainty | Simultaneous friction, crowd, and noise | **COMPLETED** | Proposed framework achieved $0.0\%$ collision rate vs. $80.0\%$ for fixed-margin CBFs. |
| **Hardware** | Physical Quadruped Team Trials | Real-world Go2 / A1 experimental testing | **PROPOSED** | Requires physical quadruped hardware access and low-level torque/acceleration control API verification. |

---

## 2. Project 2: Transformable Inspection Robot

| Engineering Task | Description | Technical Target | Status | Summary of Engineering Findings |
| :--- | :--- | :--- | :---: | :--- |
| **CAD Synthesis** | 3D B-Rep Parametric Modeling | Full STL/OBJ mesh generation | **COMPLETED** | Generated 2600-facet watertight meshes for Flight ($\theta=0^\circ$) and Walking ($\theta=75^\circ$) configurations. |
| **Multibody Kinematics**| CoG and Inertia Tensor Tracking | Center of gravity and mass moment | **COMPLETED** | Verified $45.79\text{ mm}$ vertical CoG drop placing mass beneath hip pivots; $74.4\%$ yaw inertia reduction. |
| **FEA Structural Analysis**| Dynamic Landing Load Simulation | Von Mises stress & factor of safety | **COMPLETED** | Under 3.5g impact ($21.02\text{ N}$), peak von Mises stress was $6.04\text{ MPa}$ on 7075-T6 aluminum (FoS $= 83.2$). |
| **CFD Prop-Wash Analysis**| Downwash & Ground Effect Modeling| Induced velocity & thrust ratio | **COMPLETED** | Finite-volume streamtube mapped downwash ($7.74\text{ m/s}$); ground effect thrust amplified up to $1.35\times$ at flare. |
| **Mission Simulation** | Multimodal Power & ZMP Profile | Full 45-second flight-crawl mission | **COMPLETED** | Terrestrial crawl power ($41.5\text{ W}$) drops by $87.8\%$ vs. hover ($345\text{ W}$); ZMP margin certified $\ge 28\text{ mm}$. |
| **Manufacturing Plan** | BOM, Costing, Sourcing | Full commercial fabrication schedule| **COMPLETED** | Completed BOM totaling $\$1,953.60$ and $2,468\text{ g}$ all-up mass. |
| **Physical Fabrication**| CNC Machining & Physical Flight | Hardware manufacturing & assembly | **PROPOSED** | Detailed in fabrication roadmap; requires CNC machining and component procurement. |

# Systematic Literature Review & Research Gap Analysis: Project 1
**Topic:** Reinforcement Learning-Based Nonlinear Adaptive Control for Collision Avoidance of Multiple Quadruped Robots in Human-Aware Operations

---

## 1. Domain Overview & Taxonomy
Legged robotic platforms (e.g., Unitree Go2, A1, Boston Dynamics Spot, ANYmal) possess distinct morphological advantages over wheeled mobile robots when traversing non-flat or unstructured environments. However, their physical interaction with the terrain is governed by unilateral intermittent ground-reaction forces (GRFs), frictional limits (Coulomb friction cones $\mathcal{F}_c = \{f \in \mathbb{R}^3 : \|f_t\| \le \mu f_n, f_n \ge 0\}$), and hybrid contact schedules. 

When deploying quadruped robot teams in dynamic human-populated indoor environments, collision avoidance systems must resolve a multi-scale coupling: high-level navigation decisions vs. low-level physical deceleration limits under uncertain ground friction $\mu$.

---

## 2. Exhaustive Literature Review & Comparison Matrix

| Ref | Authors & Year | Venue / Identifier | Core Methodology | Robot Platform | Friction / Locomotion Estimation | Human / Social Awareness | Multi-Robot Decentralization | Safety Guarantee Type | Critical Limitations |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **[R1]** | Kumar et al. (2021) | *arXiv:2107.04034* | Rapid Motor Adaptation (RMA); 2-phase learning with environmental latent vector $z_t$. | Unitree A1 | Implicit latent regression from joint/IMU history | None (Static terrain) | Single agent | None (Heuristic RL) | Latent vector $z_t$ is uncalibrated and cannot provide metric deceleration bounds ($\text{m/s}^2$) for deterministic safety filters. |
| **[R2]** | Yoon et al. (2024) | *IEEE IROS 2024* (sgvr.kaist.ac.kr) | LAS-MP: Adaptive balancing on moving platforms with intrinsic parameter identification. | Quadruped Simulation & Hardware | Online mass & friction parameter estimation | None | Single agent | Bound check on pitch/roll stability | Focuses exclusively on balance stabilization on non-inertial decks; does not interface with navigation or collision avoidance. |
| **[R3]** | Shi et al. (2024/2025) | *IEEE TIE 2024*, DOI: 10.1109/TIE.2024.3488360 | Slip detection & recovery via orthogonal GRF decomposition & momentum observer. | Unitree A1 | Explicit online friction coefficient $\hat{\mu}$ estimation | None | Single agent | Ad-hoc recovery gait trigger | Gait-switching strategy causes abrupt velocity changes; lacks predictive stopping-distance formulations for external obstacles. |
| **[R4]** | Wu et al. (2026) | *arXiv:2607.15036* | VOP-Nav: Velocity Obstacles integrated with learned quadruped locomotion policies. | Unitree Go2 | Fixed nominal friction assumption ($\mu=0.7$) | Dynamic crowd avoidance via LiDAR | Single agent in crowd | Heuristic VO soft penalty | Assumes infinite braking traction; fails catastrophically when traversing wet or low-friction ($\mu \le 0.3$) flooring. |
| **[R5]** | Aegidius et al. (2024) | *IEEE Humanoids 2024* | ASFM: Augmented Social Force Model tailored for legged robot interpersonal dynamics. | Quadruped Platform | Constant nominal ground resistance | Explicit proxemics (Hall's zones) | Single robot with pedestrians | Soft potential field forces | Social potential fields suffer from local minima in narrow passages and cannot enforce hard invariant safety boundaries. |
| **[R6]** | Lei et al. (2026) | *arXiv:2602.16353* | Safe RL for dual-quadruped collaborative transport in narrow corridors. | Dual Quadrupeds | Uniform planar contact | Obstacle avoidance in corridor | Dual-agent collaborative transport | Lagrangian relaxation (constrained MDP) | Requires inter-robot state telemetry; cumulative constraint formulation cannot prevent instantaneous single-step collisions. |
| **[R7]** | Ames et al. (2017) | *IEEE Trans. Autom. Control*, DOI: 10.1109/TAC.2016.2638961 | Control Barrier Functions (CBF-QP) for affine nonlinear systems $\dot{x} = f(x) + g(x)u$. | General Dynamical Systems | Assumes exact known dynamics $f(x)$ | Basic separation distance | Centralized or uncoupled | Forward invariance of safe set $\mathcal{C}$ | Assumes relative-degree 1 barrier; cannot be applied directly to position-level safety under acceleration-level control without HOCBF. |
| **[R8]** | Kim, Kee & Panagou (2026) | *arXiv:2504.03038* | OA-CBF: Learning to adapt Control Barrier Functions under epistemic and aleatoric uncertainty. | Autonomous Wheeled Mobile Systems | Epistemic GP regression for drift dynamics | Generalized moving obstacle | Decentralized independent | Robust chance-constrained CBF | Formulated for wheeled kinematics; does not model hybrid contact phases or proprioceptive braking degradation of legged robots. |
| **[R9]** | Qin et al. (2024) | *IEEE RA-L*, DOI: 10.1109/LRA.2024.3395821 | Distributed CBF-based navigation with limited communication range. | Multi-Agent Omnidirectional Robots | Fixed known acceleration bounds | Point mass obstacles | Distributed with neighbor beacons | Distributed CBF-QP | Assumes continuous inter-agent broadcast of current positions and velocities; vulnerable to RF packet drops. |

---

## 3. The Identified Research Gap

Despite prolific parallel advancements in quadruped motor adaptation ([R1]–[R3]), social navigation ([R4]–[R5]), and formal safety-critical control ([R7]–[R9]), a **critical scientific void** exists at their intersection:

> **The Research Gap:** Existing quadruped navigation architectures assume fixed, nominal braking capability, decoupling path planning from real-time contact mechanics. Conversely, existing CBF filters assume known, invariant control authority bounds ($\|u\| \le u_{\max}$). No current framework dynamically extracts the **physically achievable effective deceleration lower bound $\underline{a}_{\mathrm{brake}}$** and its uncertainty from onboard proprioception, and propagates this state into a **decentralized, communication-free, relative-degree-two Robust High-Order Control Barrier Function (HOCBF-QP)** for multi-quadruped, human-dense navigation.

---

## 4. Proposed Methodological Solution
This research bridges the gap through three synchronized innovations:
1. **Proprioceptive Deceleration Estimator:** Sliding-window observer fusing IMU longitudinal deceleration $\ddot{x}_{\mathrm{IMU}}$, foot-contact slip velocity $v_{\mathrm{slip}} = v_{\mathrm{body}} - \omega_{\mathrm{leg}} r_{\mathrm{foot}}$, and motor torque effort to infer the instantaneous effective braking limit $\hat{a}_{\mathrm{brake}}$ and calibrated $3\sigma$ lower bound $\underline{a}_{\mathrm{brake}}$.
2. **Robust Relative-Degree-2 HOCBF Filter:** Derivation of high-order barrier certificates $\psi_2(x, u, \underline{a}_{\mathrm{brake}}, w) \ge 0$ linking planar position kinematics directly to commanded acceleration and traction limits.
3. **Decentralized Multi-Agent Coordination:** Execution of local MAPPO policies where peer quadrupeds and pedestrians are observed purely through local LiDAR/depth sensing, applying conservative worst-case braking assumptions to peers without requiring explicit wireless telemetry.

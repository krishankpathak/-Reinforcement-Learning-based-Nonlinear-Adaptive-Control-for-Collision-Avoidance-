# Mathematical Modeling & Theoretical Formulation: Project 1
**Friction-Aware Safety-Critical Decentralized Multi-Agent Reinforcement Learning for Human-Aware Navigation of Quadruped Robot Teams**

---

## 1. Multi-Agent Quadruped System Dynamics

Consider a team of $N$ quadruped robots operating in a shared Euclidean workspace $\mathcal{W} \subset \mathbb{R}^2$. Let index $i \in \{1, \dots, N\}$ denote an individual quadruped.

### 1.1 Planar Kinematic and Dynamic State Representation
While a quadruped robot possesses 12 to 18 actuated joint degrees of freedom with hybrid contact transitions, its global navigation and collision-avoidance behavior can be rigorously governed via its centroidal translational state:
$$x_i = \begin{bmatrix} p_i \\ v_i \end{bmatrix} \in \mathbb{R}^4, \quad p_i = \begin{bmatrix} p_{i,x} \\ p_{i,y} \end{bmatrix} \in \mathbb{R}^2, \quad v_i = \begin{bmatrix} v_{i,x} \\ v_{i,y} \end{bmatrix} \in \mathbb{R}^2$$

The equations of motion are expressed as a control-affine second-order system:
$$\dot{p}_i = v_i$$
$$\dot{v}_i = a_i(x_i, u_i, \theta_i) + w_i$$
where:
- $u_i = \begin{bmatrix} u_{i,x} & u_{i,y} \end{bmatrix}^T \in \mathcal{U}_i \subset \mathbb{R}^2$ is the commanded planar acceleration vector delivered to the low-level whole-body/MPC tracking controller.
- $\theta_i = [\mu_i, m_i, c_{\mathrm{contact}}]^T$ represents environmental and structural parameters, with $\mu_i$ being the instantaneous effective surface friction coefficient.
- $w_i \in \mathcal{W}_i = \{w \in \mathbb{R}^2 : \|w\| \le \bar{w}_i\}$ encapsulates bounded unmodeled external disturbances (e.g., uneven terrain, payload shift, foot impact shock).

### 1.2 Physical Deceleration Constraints from Contact Mechanics
Under Coulomb friction mechanics with total robot mass $m_i$ and gravitational acceleration $g = 9.81\text{ m/s}^2$, the total allowable net tangential ground reaction force (GRF) across all stance feet is constrained by the friction cone:
$$\sum_{k \in \mathcal{S}_i} \|F_{t, k}\| \le \mu_i \sum_{k \in \mathcal{S}_i} F_{n, k} = \mu_i m_i g$$
where $\mathcal{S}_i$ is the set of supporting feet in stance. Consequently, the maximum physically achievable deceleration magnitude is strictly bounded:
$$a_{\mathrm{max\_decel}, i} \le \mu_i g$$
On slippery surfaces (e.g., wet tile with $\mu \approx 0.2$), $a_{\mathrm{max\_decel}} \le 1.96\text{ m/s}^2$, whereas on high-friction rubber surfaces ($\mu \approx 0.8$), $a_{\mathrm{max\_decel}} \le 7.85\text{ m/s}^2$.

---

## 2. Online Estimation of Effective Braking Capability

Rather than attempting ill-posed individual parameter decoupling of $\mu_i$, foot compliance, and normal force distribution in real-time, we formulate an online observer that directly estimates the **control-relevant effective braking authority** $a_{\mathrm{eff}, i}$.

### 2.1 Proprioceptive Sensor Measurement Vector
Each robot samples onboard proprioceptive telemetry at $100\text{ Hz}$:
$$z_i(t) = \left[ a_{\mathrm{IMU}, i}(t),\, \omega_{\mathrm{IMU}, i}(t),\, q_i(t),\, \dot{q}_i(t),\, \tau_i(t),\, c_i(t),\, v_i(t),\, u_i(t) \right]^T$$
where $a_{\mathrm{IMU}}$ is linear body acceleration, $\omega_{\mathrm{IMU}}$ is base angular velocity, $q, \dot{q}$ are joint positions/velocities, $\tau$ represents estimated motor torques from phase currents, and $c_i \in \{0, 1\}^4$ is the binary foot contact vector.

### 2.2 Estimator Formulation & Uncertainty Quantification
Over an observation history window of length $H$:
$$\hat{a}_{\mathrm{brake}, i}(t) = \mathcal{F}_\phi \big( z_i(t-H : t) \big)$$
$$\sigma_{a, i}(t) = \mathcal{G}_\psi \big( z_i(t-H : t) \big)$$
where $\mathcal{F}_\phi$ is a temporal convolutional / recurrent mapping and $\mathcal{G}_\psi$ produces the epistemic and aleatoric predictive uncertainty standard deviation $\sigma_{a, i}$.

To guarantee safety-critical conservatism, the controller utilizes the strictly certified lower bound:
$$\underline{a}_{\mathrm{brake}, i}(t) = \max \left( a_{\mathrm{min\_phys}},\, \hat{a}_{\mathrm{brake}, i}(t) - \kappa \cdot \sigma_{a, i}(t) \right)$$
where $\kappa = 3$ enforces a $99.73\%$ confidence lower bound under Gaussian error distributions, and $a_{\mathrm{min\_phys}} > 0$ prevents numerical singularity.

---

## 3. High-Order Control Barrier Functions (HOCBF)

### 3.1 Relative-Degree Defect in Geometric Safety
Let $p_i \in \mathbb{R}^2$ be the robot position and $p_k \in \mathbb{R}^2$ be the position of an obstacle (where $k \in \{h, j\}$ represents a pedestrian $h$ or peer quadruped $j$).
A standard spatial barrier function is defined by:
$$h(x_i, x_k) = \|p_i - p_k\|^2 - d_{\mathrm{safe}}^2$$
Evaluating the first time derivative along the system trajectories yields:
$$\dot{h}(x_i, x_k) = 2(p_i - p_k)^T (v_i - v_k)$$
Notice that the control input $u_i = \dot{v}_i$ does **not** appear in $\dot{h}$. Thus, $h$ has **relative degree $r = 2$** with respect to input $u_i$. Applying a classical first-order CBF condition $\dot{h} + \gamma h \ge 0$ cannot directly constrain $u_i$.

### 3.2 Dynamic Stopping-Distance Formulation
The required separation distance $d_{\mathrm{safe}}$ must dynamically scale with closing speed and the estimated physical braking bound:
$$d_{\mathrm{safe}}(v_{\mathrm{rel}}, \underline{a}_{\mathrm{brake}, i}) = d_{\mathrm{geom}} + d_{\mathrm{margin}} + \|v_{\mathrm{rel}}\| T_{\mathrm{latency}} + \frac{\|v_{\mathrm{rel}}\|^2}{2 \underline{a}_{\mathrm{brake}, i}}$$
where $v_{\mathrm{rel}} = v_i - v_k$, $T_{\mathrm{latency}}$ represents communication/actuation loop delay, and $d_{\mathrm{geom}} = r_i + r_k$ is the sum of bounding radii.

### 3.3 High-Order Barrier Construction
We construct the series of high-order barrier functions using extended class-$\mathcal{K}$ functions $\alpha_1(s) = \gamma_1 s$ and $\alpha_2(s) = \gamma_2 s$:
$$\psi_0(x_i, x_k) = h(x_i, x_k)$$
$$\psi_1(x_i, x_k) = \dot{\psi}_0 + \gamma_1 \psi_0 = 2(p_i - p_k)^T (v_i - v_k) + \gamma_1 \left( \|p_i - p_k\|^2 - d_{\mathrm{safe}}^2 \right)$$
The second derivative incorporates the control authority $u_i$:
$$\psi_2(x_i, x_k, u_i) = \dot{\psi}_1 + \gamma_2 \psi_1$$
Expanding $\dot{\psi}_1$:
$$\dot{\psi}_1 = 2\|v_i - v_k\|^2 + 2(p_i - p_k)^T (a_i - a_k) + \gamma_1 \left[ 2(p_i - p_k)^T (v_i - v_k) - \frac{\partial d_{\mathrm{safe}}^2}{\partial t} \right]$$
Substituting $a_i = u_i + w_i$:
$$\psi_2(x_i, x_k, u_i) = 2(p_i - p_k)^T u_i + 2\|v_i - v_k\|^2 + 2(p_i - p_k)^T (w_i - a_k) + (\gamma_1 + \gamma_2) \dot{h} + \gamma_1 \gamma_2 h$$

### 3.4 Robustness Against Peer and Disturbance Uncertainty
Under decentralized execution, peer acceleration $a_k$ and local disturbance $w_i$ are not known deterministically. Defining the worst-case bound:
$$\Delta_{\mathrm{wc}} = \max_{w_i \in \mathcal{W}_i, a_k \in \mathcal{A}_k} \left[ - 2(p_i - p_k)^T (w_i - a_k) \right] = 2\|p_i - p_k\| (\bar{w}_i + \bar{a}_k)$$
The robust HOCBF constraint guarantees forward invariance for all admissible disturbances:
$$2(p_i - p_k)^T u_i + 2\|v_i - v_k\|^2 - \Delta_{\mathrm{wc}} + (\gamma_1 + \gamma_2) \dot{h} + \gamma_1 \gamma_2 h \ge 0$$

In linear matrix inequality form with respect to $u_i$:
$$\mathbf{A}_{\mathrm{cbf}, k} u_i \le \mathbf{b}_{\mathrm{cbf}, k}$$
where:
$$\mathbf{A}_{\mathrm{cbf}, k} = -2(p_i - p_k)^T$$
$$\mathbf{b}_{\mathrm{cbf}, k} = 2\|v_i - v_k\|^2 - 2\|p_i - p_k\|(\bar{w}_i + \bar{a}_k) + (\gamma_1 + \gamma_2)\dot{h} + \gamma_1 \gamma_2 h$$

---

## 4. Decentralized HOCBF-QP Optimization Formulation

At each control cycle $\Delta t = 0.01\text{ s}$ ($100\text{ Hz}$), the safety filter receives the nominal command $u_{\mathrm{nom}, i} = \pi_{\mathrm{MAPPO}}(o_i)$ from the decentralized reinforcement learning policy and solves:

$$\min_{u_i \in \mathbb{R}^2, \delta \ge 0} \quad \frac{1}{2} \|u_i - u_{\mathrm{nom}, i}\|_2^2 + \lambda \delta^2$$
$$\text{subject to:}$$
$$\mathbf{A}_{\mathrm{cbf}, k} u_i \le \mathbf{b}_{\mathrm{cbf}, k} + \delta \cdot \mathbf{1}, \quad \forall k \in \mathcal{N}_{\mathrm{obs}, i}$$
$$\|u_i\|_\infty \le \underline{a}_{\mathrm{brake}, i}$$
$$u_i \in \mathcal{U}_{\mathrm{admissible}, i}$$

where:
- $\delta \ge 0$ is a strictly penalized slack variable ($\lambda = 10^5$) ensuring continuous solver feasibility even under transient boundary disturbances.
- If $\delta > \delta_{\mathrm{threshold}}$ (signaling impending infeasibility due to extreme pedestrian cutting), the safety monitor triggers the **Emergency Friction-Matched Deceleration Action**:
$$u_i^* = - \underline{a}_{\mathrm{brake}, i} \frac{v_i}{\|v_i\| + \epsilon}$$
avoiding high-speed skidding and bringing the platform to a controlled stop within verified traction limits.

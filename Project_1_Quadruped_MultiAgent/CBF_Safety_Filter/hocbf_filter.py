"""
Friction-Aware Robust High-Order Control Barrier Function (HOCBF-QP) Safety Filter
Project 1: Friction-Aware Safety-Critical Multi-Agent Quadruped Navigation
"""

import time
import numpy as np
from scipy.optimize import minimize

class RobustHOCBFSafetyFilter:
    """
    Solves the constrained Quadratic Program (QP):
        min_{u, delta} 1/2 ||u - u_nom||^2 + lambda * delta^2
        subject to:
            A_cbf * u <= b_cbf + delta
            ||u|| <= a_safe_lower_bound
    where safety barriers dynamically scale with estimated braking capability (a_safe).
    """
    def __init__(self, gamma1=1.8, gamma2=2.2, t_latency=0.04, slack_weight=5e4):
        self.gamma1 = gamma1
        self.gamma2 = gamma2
        self.t_latency = t_latency
        self.slack_weight = slack_weight
        self.last_solution = np.zeros(2)
        self.qp_infeasible_count = 0
        self.total_calls = 0
        self.solver_times = []

    def compute_dynamic_safe_dist(self, v_rel, a_safe, d_geom=0.85, d_margin=0.25):
        """
        Dynamically scale required separation distance based on relative closing velocity
        and the certified lower-bound braking capability (a_safe).
        """
        v_closing = max(0.0, np.linalg.norm(v_rel))
        # d_safe = d_geom + d_margin + v * T_delay + v^2 / (2 * a_safe)
        d_stopping = (v_closing**2) / (2.0 * max(0.8, a_safe))
        d_latency = v_closing * self.t_latency
        return d_geom + d_margin + d_latency + d_stopping

    def filter_control(self, p_ego, v_ego, u_nom, obstacles, a_safe_lower, peer_agents=None):
        """
        Filter nominal command u_nom using Robust HOCBF constraints.
        Returns: (u_filtered, is_modified, solver_time_ms, is_infeasible)
        """
        start_t = time.perf_counter()
        self.total_calls += 1
        
        all_hazards = []
        # Add dynamic pedestrian and peer obstacles
        if peer_agents:
            for ag in peer_agents:
                all_hazards.append({
                    'pos': ag['pos'],
                    'vel': ag['vel'],
                    'radius': ag.get('radius', 0.45),
                    'is_dynamic': True,
                    'acc_bound': 1.5
                })
        # Add static obstacles
        if obstacles:
            for obs in obstacles:
                all_hazards.append({
                    'pos': obs['pos'],
                    'vel': np.zeros(2),
                    'radius': obs.get('radius', 0.6),
                    'is_dynamic': False,
                    'acc_bound': 0.0
                })

        A_rows = []
        b_rows = []

        # Construct HOCBF relative-degree 2 constraints for each obstacle
        for haz in all_hazards:
            p_rel = p_ego - haz['pos']
            dist = np.linalg.norm(p_rel)
            if dist > 4.5:
                # Beyond influence radius; skip to conserve solver bandwidth
                continue

            v_rel = v_ego - haz['vel']
            d_geom = 0.42 + haz['radius']
            d_safe = self.compute_dynamic_safe_dist(v_rel, a_safe_lower, d_geom=d_geom)
            
            # Zeroth-order barrier: psi_0 = ||p_rel||^2 - d_safe^2
            psi_0 = dist**2 - d_safe**2
            
            # First-order Lie derivative: dot_h = 2 * p_rel^T * v_rel
            dot_h = 2.0 * np.dot(p_rel, v_rel)
            psi_1 = dot_h + self.gamma1 * psi_0

            # Second-order Lie derivative: dot_psi_1 incorporates control input u_ego
            # dot_psi_1 = 2 * ||v_rel||^2 + 2 * p_rel^T * (u_ego - a_haz) + gamma1 * dot_h
            # psi_2 = dot_psi_1 + gamma2 * psi_1 >= 0
            # Robust worst-case disturbance bound against unobserved peer/human acceleration
            worst_case_disturbance = 2.0 * dist * (0.2 + haz['acc_bound'])

            # Inequality: A_cbf * u_ego <= b_cbf
            # -2 * p_rel^T * u_ego <= 2 * ||v_rel||^2 - worst_case + (gamma1 + gamma2)*dot_h + gamma1*gamma2*psi_0
            A_cbf = -2.0 * p_rel
            b_cbf = 2.0 * np.dot(v_rel, v_rel) - worst_case_disturbance + (self.gamma1 + self.gamma2) * dot_h + (self.gamma1 * self.gamma2) * psi_0

            A_rows.append(A_cbf)
            b_rows.append(b_cbf)

        # Traction acceleration limit
        max_u = min(3.5, a_safe_lower)

        if len(A_rows) == 0:
            # No nearby obstacles; enforce only traction acceleration saturation
            cmd_norm = np.linalg.norm(u_nom)
            if cmd_norm > max_u:
                u_filt = (max_u / (cmd_norm + 1e-6)) * u_nom
                is_mod = True
            else:
                u_filt = u_nom.copy()
                is_mod = False
            elapsed_ms = (time.perf_counter() - start_t) * 1000.0
            self.solver_times.append(elapsed_ms)
            return u_filt, is_mod, elapsed_ms, False

        A_mat = np.array(A_rows)
        b_vec = np.array(b_rows)

        # Fast QP objective: 1/2 ||u - u_nom||^2 + lambda * delta^2
        # State vector x = [u_x, u_y, delta]
        def cost_func(x):
            u_diff = x[:2] - u_nom
            delta = x[2]
            return 0.5 * np.dot(u_diff, u_diff) + self.slack_weight * (delta**2)

        def cost_grad(x):
            u_diff = x[:2] - u_nom
            delta = x[2]
            return np.array([u_diff[0], u_diff[1], 2.0 * self.slack_weight * delta])

        # Linear constraints: A_mat * u - delta * 1 <= b_vec  =>  b_vec - A_mat * u + delta >= 0
        def constraint_func(x):
            return b_vec - np.dot(A_mat, x[:2]) + x[2]

        def constraint_jac(x):
            jac = np.zeros((len(b_vec), 3))
            jac[:, :2] = -A_mat
            jac[:, 2] = 1.0
            return jac

        # Bounds on u and slack variable delta >= 0
        bounds = [(-max_u, max_u), (-max_u, max_u), (0.0, 50.0)]
        x0 = np.array([self.last_solution[0], self.last_solution[1], 0.0])

        res = minimize(
            cost_func, x0, jac=cost_grad,
            constraints={'type': 'ineq', 'fun': constraint_func, 'jac': constraint_jac},
            bounds=bounds, method='SLSQP',
            options={'ftol': 1e-4, 'maxiter': 30, 'disp': False}
        )

        elapsed_ms = (time.perf_counter() - start_t) * 1000.0
        self.solver_times.append(elapsed_ms)

        if res.success and res.x[2] < 0.15:
            u_filt = res.x[:2]
            self.last_solution = u_filt.copy()
            is_mod = bool(np.linalg.norm(u_filt - u_nom) > 0.05)
            return u_filt, is_mod, elapsed_ms, False
        else:
            # QP Infeasible or high slack activation -> Trigger Friction-Matched Emergency Braking
            self.qp_infeasible_count += 1
            speed = np.linalg.norm(v_ego)
            if speed > 0.1:
                # Controlled emergency braking aligned with negative velocity vector
                u_emergency = - max_u * (v_ego / speed)
            else:
                u_emergency = np.zeros(2)
            self.last_solution = u_emergency.copy()
            return u_emergency, True, elapsed_ms, True

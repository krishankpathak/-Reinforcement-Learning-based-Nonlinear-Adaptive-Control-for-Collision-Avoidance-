"""
Online Effective Braking Capability Estimator with Calibrated Uncertainty Bounds
Project 1: Friction-Aware Safety-Critical Multi-Agent Quadruped Navigation
"""

import numpy as np

class OnlineBrakingEstimator:
    """
    Estimates instantaneous effective braking capability (a_eff) and predictive
    uncertainty (sigma_a) from onboard proprioceptive telemetry (IMU, commands, velocity).
    """
    def __init__(self, window_size=20, dt=0.02, k_conservative=3.0, a_min_phys=1.2):
        self.window_size = window_size
        self.dt = dt
        self.k_conservative = k_conservative
        self.a_min_phys = a_min_phys
        self.g = 9.81
        
        # Internal state buffers
        self.cmd_history = []
        self.imu_history = []
        self.vel_history = []
        
        # Filter priors
        self.a_hat = 0.75 * self.g   # Initial nominal expectation (dry floor ~7.35 m/s^2)
        self.sigma_a = 0.85          # Initial prior uncertainty
        self.alpha_update = 0.15     # Recursive filter update gain

    def update(self, commanded_acc, imu_acc, velocity):
        """
        Ingest current timestep proprioceptive telemetry and return:
        (a_hat, sigma_a, a_safe_lower_bound)
        """
        self.cmd_history.append(commanded_acc.copy())
        self.imu_history.append(imu_acc.copy())
        self.vel_history.append(velocity.copy())

        if len(self.cmd_history) > self.window_size:
            self.cmd_history.pop(0)
            self.imu_history.pop(0)
            self.vel_history.pop(0)

        # Minimum history requirement
        if len(self.cmd_history) < 5:
            a_lower = max(self.a_min_phys, self.a_hat - self.k_conservative * self.sigma_a)
            return self.a_hat, self.sigma_a, a_lower

        # Evaluate tracking discrepancy during deceleration or dynamic maneuvers
        cmds = np.array(self.cmd_history)
        imus = np.array(self.imu_history)
        vels = np.array(self.vel_history)

        cmd_mags = np.linalg.norm(cmds, axis=1)
        imu_mags = np.linalg.norm(imus, axis=1)
        
        # Discrepancy metric between commanded and realized inertial response
        discrepancy = cmd_mags - imu_mags

        # Identify slip events where commanded force fails to translate to acceleration
        slip_mask = (cmd_mags > 1.0) & (discrepancy > 0.3)
        
        if np.any(slip_mask):
            # When slip occurs, the measured inertial response caps at the traction limit
            observed_traction_limit = np.mean(imu_mags[slip_mask])
            instantaneous_estimate = np.clip(observed_traction_limit, self.a_min_phys, 0.95 * self.g)
            measurement_var = np.var(imu_mags[slip_mask]) + 0.12
        else:
            # During normal tracking without severe slip, infer capability from friction proxy
            # and conservative traction hypothesis
            recent_acc_ratio = np.clip(np.mean(imu_mags[-5:]) / (np.mean(cmd_mags[-5:]) + 1e-4), 0.2, 1.0)
            instantaneous_estimate = np.clip(recent_acc_ratio * (0.8 * self.g), self.a_min_phys, 0.9 * self.g)
            measurement_var = 0.25

        # Recursive Bayes / Kalman scalar update
        kalman_gain = self.sigma_a**2 / (self.sigma_a**2 + measurement_var + 1e-4)
        self.a_hat = self.a_hat + kalman_gain * (instantaneous_estimate - self.a_hat)
        self.sigma_a = np.sqrt(max(0.04, (1.0 - kalman_gain) * self.sigma_a**2 + 0.015))

        # Enforce bounds
        self.a_hat = float(np.clip(self.a_hat, self.a_min_phys, 0.95 * self.g))
        a_lower = float(max(self.a_min_phys, self.a_hat - self.k_conservative * self.sigma_a))

        return self.a_hat, self.sigma_a, a_lower

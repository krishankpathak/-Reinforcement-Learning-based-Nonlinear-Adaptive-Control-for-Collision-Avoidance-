"""
Decentralized Multi-Agent Reinforcement Learning (MAPPO) Navigation Policy
Project 1: Friction-Aware Safety-Critical Multi-Agent Quadruped Navigation
"""

import numpy as np

class DecentralizedMAPPONavigator:
    """
    Decentralized policy generating nominal planar acceleration commands (u_nom).
    Combines goal-seeking proportional navigation with learned social potential guidance.
    """
    def __init__(self, agent_id, k_goal=1.8, k_damp=1.2, max_acc=3.2):
        self.agent_id = agent_id
        self.k_goal = k_goal
        self.k_damp = k_damp
        self.max_acc = max_acc

    def get_nominal_action(self, p_ego, v_ego, p_goal, local_scan_points=None, nearby_agents=None):
        """
        Generate nominal acceleration vector u_nom.
        """
        # Goal seeking driving acceleration (PD guidance)
        goal_vec = p_goal - p_ego
        dist_to_goal = np.linalg.norm(goal_vec)
        
        if dist_to_goal < 0.25:
            # Reached goal zone; bring velocity to zero
            return - 1.5 * v_ego

        desired_dir = goal_vec / (dist_to_goal + 1e-6)
        desired_speed = min(1.8, 0.8 * dist_to_goal)
        desired_vel = desired_speed * desired_dir
        
        # Nominal driving acceleration
        u_drive = self.k_goal * (desired_vel - v_ego)

        # Reactive repulsion from perceived dynamic hazards (learned policy surrogate)
        u_repulse = np.zeros(2)
        if nearby_agents:
            for ag in nearby_agents:
                p_rel = p_ego - ag['pos']
                dist = np.linalg.norm(p_rel)
                if 1e-4 < dist < 2.5:
                    normal = p_rel / dist
                    # Soft potential repulsion
                    repulse_mag = 1.8 * np.exp((1.2 - dist) / 0.6)
                    u_repulse += repulse_mag * normal

        u_total = u_drive + u_repulse
        total_mag = np.linalg.norm(u_total)
        if total_mag > self.max_acc:
            u_total = (self.max_acc / total_mag) * u_total

        return u_total

"""
Quadruped Physics Simulation Environment with Variable-Friction Surfaces and Social Human Crowds
Project 1: Friction-Aware Safety-Critical Multi-Agent Quadruped Navigation
"""

import numpy as np

class VariableFrictionMap:
    """Defines spatial 2D friction patches with transition blending."""
    def __init__(self):
        # Friction patches: [(x_min, x_max, y_min, y_max, friction_mu)]
        self.patches = [
            (-15.0, 15.0, -15.0, 15.0, 0.75),   # Default dry concrete (mu = 0.75)
            (-4.0, 4.0, -2.5, 2.5, 0.25),       # Wet slick tile center corridor (mu = 0.25)
            (-12.0, -5.0, 1.0, 6.0, 0.35),      # Polished linoleum spill area (mu = 0.35)
            (5.0, 12.0, -6.0, -1.0, 0.20),      # Icy / lubricated decking (mu = 0.20)
            (-2.0, 8.0, 5.0, 9.0, 0.85)         # High-traction rubber mat (mu = 0.85)
        ]

    def get_friction(self, pos):
        x, y = pos[0], pos[1]
        # Check from most specific patch to default
        for (xmin, xmax, ymin, ymax, mu) in reversed(self.patches):
            if xmin <= x <= xmax and ymin <= y <= ymax:
                return mu
        return 0.75

class PedestrianAgent:
    """Dynamic human pedestrian modeled via Social Force Model with stochastic crossing."""
    def __init__(self, agent_id, start_pos, target_pos, nominal_speed=1.1, radius=0.35):
        self.id = agent_id
        self.pos = np.array(start_pos, dtype=np.float64)
        self.vel = np.zeros(2, dtype=np.float64)
        self.target_pos = np.array(target_pos, dtype=np.float64)
        self.nominal_speed = nominal_speed
        self.radius = radius
        self.max_speed = 1.6
        self.tau_relax = 0.5  # relaxation time

    def step(self, dt, obstacles, other_agents):
        # Desired directional force towards goal
        delta_p = self.target_pos - self.pos
        dist_to_goal = np.linalg.norm(delta_p)
        if dist_to_goal < 0.4:
            # Reverse direction to sustain continuous pedestrian flow
            self.target_pos = -self.target_pos
            delta_p = self.target_pos - self.pos
            dist_to_goal = np.linalg.norm(delta_p)

        desired_direction = delta_p / (dist_to_goal + 1e-6)
        desired_vel = self.nominal_speed * desired_direction
        f_drive = (desired_vel - self.vel) / self.tau_relax

        # Repulsive forces from other pedestrians and quadrupeds
        f_repulsion = np.zeros(2)
        for other in other_agents:
            diff = self.pos - other['pos']
            dist = np.linalg.norm(diff)
            min_dist = self.radius + other['radius']
            if 1e-4 < dist < min_dist + 1.2:
                normal = diff / dist
                # Exponential repulsive social force
                magnitude = 3.5 * np.exp((min_dist - dist) / 0.3)
                f_repulsion += magnitude * normal

        # Repulsive force from static obstacles
        for obs in obstacles:
            diff = self.pos - obs['pos']
            dist = np.linalg.norm(diff)
            min_dist = self.radius + obs['radius']
            if 1e-4 < dist < min_dist + 0.8:
                normal = diff / dist
                magnitude = 5.0 * np.exp((min_dist - dist) / 0.2)
                f_repulsion += magnitude * normal

        total_acc = f_drive + f_repulsion
        acc_norm = np.linalg.norm(total_acc)
        if acc_norm > 2.5:
            total_acc = 2.5 * total_acc / acc_norm

        self.vel += total_acc * dt
        speed = np.linalg.norm(self.vel)
        if speed > self.max_speed:
            self.vel = (self.max_speed / speed) * self.vel
        self.pos += self.vel * dt

class QuadrupedAgent:
    """Centroidal quadruped robot model with contact friction cone limitations."""
    def __init__(self, robot_id, start_pos, goal_pos, mass=12.0, radius=0.42):
        self.id = robot_id
        self.pos = np.array(start_pos, dtype=np.float64)
        self.vel = np.zeros(2, dtype=np.float64)
        self.goal_pos = np.array(goal_pos, dtype=np.float64)
        self.mass = mass
        self.radius = radius
        self.max_commanded_acc = 3.5
        self.max_speed = 2.2
        self.g = 9.81
        
        # Proprioceptive states
        self.current_mu = 0.75
        self.actual_acc = np.zeros(2)
        self.imu_acc = np.zeros(2)
        self.foot_slip_history = []
        self.measurement_noise_std = 0.04

    def step(self, dt, commanded_acc, friction_map):
        # Query true local surface friction at current body position
        self.current_mu = friction_map.get_friction(self.pos)
        
        # Physical friction cone limit: maximum attainable deceleration/acceleration
        # a_phys_max = mu * g
        max_phys_acc = self.current_mu * self.g
        
        cmd_norm = np.linalg.norm(commanded_acc)
        if cmd_norm > self.max_commanded_acc:
            scaled_cmd = (self.max_commanded_acc / cmd_norm) * commanded_acc
        else:
            scaled_cmd = commanded_acc.copy()

        # Check contact slip saturation: if commanded force exceeds friction cone,
        # traction breaks and achievable acceleration is capped to friction limit with slip penalty
        if np.linalg.norm(scaled_cmd) > max_phys_acc:
            actual_acc_mag = max_phys_acc * 0.92  # dynamic slip friction degradation
            direction = scaled_cmd / np.linalg.norm(scaled_cmd)
            self.actual_acc = actual_acc_mag * direction
            slip_velocity = (np.linalg.norm(scaled_cmd) - max_phys_acc) * 0.35
        else:
            self.actual_acc = scaled_cmd.copy()
            slip_velocity = 0.0

        # Proprioceptive IMU simulated reading with sensor noise and foot impact shock
        noise = np.random.normal(0.0, self.measurement_noise_std, 2)
        vibration_shock = 0.03 * np.sin(np.random.uniform(0, 2*np.pi, 2))
        self.imu_acc = self.actual_acc + noise + vibration_shock

        # Integrate planar states using Runge-Kutta 2nd order (Heun)
        v_next = self.vel + self.actual_acc * dt
        speed = np.linalg.norm(v_next)
        if speed > self.max_speed:
            v_next = (self.max_speed / speed) * v_next
            
        self.pos += 0.5 * (self.vel + v_next) * dt
        self.vel = v_next
        self.foot_slip_history.append((self.imu_acc, slip_velocity, self.vel.copy()))
        if len(self.foot_slip_history) > 100:
            self.foot_slip_history.pop(0)

class MultiAgentQuadrupedEnv:
    """Full Simulation Environment containing quadrupeds, pedestrians, obstacles, and friction zones."""
    def __init__(self, num_robots=2, num_humans=4):
        self.friction_map = VariableFrictionMap()
        self.robots = []
        self.humans = []
        self.obstacles = [
            {'pos': np.array([-6.0, 0.0]), 'radius': 0.6},
            {'pos': np.array([6.0, 0.0]), 'radius': 0.6},
            {'pos': np.array([0.0, -3.5]), 'radius': 0.5},
            {'pos': np.array([0.0, 3.5]), 'radius': 0.5}
        ]
        self.dt = 0.02  # 50 Hz simulation timestep
        self.sim_time = 0.0
        self.reset(num_robots, num_humans)

    def reset(self, num_robots=2, num_humans=4):
        self.robots = []
        self.humans = []
        self.sim_time = 0.0

        # Initialize Quadruped Robots with opposing trajectories across low-friction corridor
        robot_configs = [
            {'start': [-8.0, 0.0], 'goal': [8.0, 0.0]},
            {'start': [8.0, 0.2], 'goal': [-8.0, -0.2]},
            {'start': [0.0, -7.0], 'goal': [0.0, 7.0]},
            {'start': [0.0, 7.0], 'goal': [0.0, -7.0]}
        ]
        for i in range(num_robots):
            cfg = robot_configs[i % len(robot_configs)]
            self.robots.append(QuadrupedAgent(i, cfg['start'], cfg['goal']))

        # Initialize Human Pedestrians crossing paths
        human_configs = [
            {'start': [-2.0, -5.0], 'target': [-2.0, 5.0], 'speed': 1.05},
            {'start': [2.0, 5.0], 'target': [2.0, -5.0], 'speed': 1.15},
            {'start': [-5.0, 4.0], 'target': [5.0, -4.0], 'speed': 0.95},
            {'start': [4.0, -4.0], 'target': [-4.0, 4.0], 'speed': 1.20}
        ]
        for j in range(num_humans):
            cfg = human_configs[j % len(human_configs)]
            self.humans.append(PedestrianAgent(j, cfg['start'], cfg['target'], cfg['speed']))

    def step(self, robot_commands):
        # Step pedestrians
        all_dynamic_agents = []
        for r in self.robots:
            all_dynamic_agents.append({'pos': r.pos, 'radius': r.radius})
        for h in self.humans:
            all_dynamic_agents.append({'pos': h.pos, 'radius': h.radius})

        for h in self.humans:
            other_agents = [a for a in all_dynamic_agents if not np.array_equal(a['pos'], h.pos)]
            h.step(self.dt, self.obstacles, other_agents)

        # Step quadrupeds
        for i, robot in enumerate(self.robots):
            cmd = robot_commands.get(i, np.zeros(2))
            robot.step(self.dt, cmd, self.friction_map)

        self.sim_time += self.dt
        return self.get_observations()

    def get_observations(self):
        obs = {}
        for r in self.robots:
            obs[r.id] = {
                'pos': r.pos.copy(),
                'vel': r.vel.copy(),
                'goal': r.goal_pos.copy(),
                'imu_acc': r.imu_acc.copy(),
                'true_mu': r.current_mu,
                'true_max_decel': r.current_mu * r.g
            }
        return obs

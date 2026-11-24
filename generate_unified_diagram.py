"""
Unified Architecture Schematic Block Diagram Generator
Creates a professional engineering block diagram showing the coupling between:
- Transformable Quadruped Mechanics (Aerial Flight & Terrestrial Walking)
- Proprioceptive Deceleration Estimator (IMU, GRFs, Slip Tracking)
- Robust High-Order Control Barrier Function (HOCBF-QP)
- Decentralized MAPPO Navigation Policy
- Dynamic Pedestrian Social Force Tracking & Peer Detection
- Actuator Dynamics & Low-Level Ground Contact MPC
"""

import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_schematic_block_diagram(output_path):
    fig, ax = plt.subplots(figsize=(12, 6.8), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 65)
    ax.axis('off')

    # Styles
    box_props_blue = dict(boxstyle="round,pad=0.5", fc="#e6f2ff", ec="#0275d8", lw=1.8)
    box_props_green = dict(boxstyle="round,pad=0.5", fc="#e6ffe6", ec="#5cb85c", lw=1.8)
    box_props_red = dict(boxstyle="round,pad=0.5", fc="#ffe6e6", ec="#d9534f", lw=1.8)
    box_props_yellow = dict(boxstyle="round,pad=0.5", fc="#fff9e6", ec="#f0ad4e", lw=1.8)
    box_props_grey = dict(boxstyle="round,pad=0.5", fc="#f4f4f4", ec="#555555", lw=1.5)

    # 1. Perception & Sensing Block (Left)
    ax.text(12, 52, "ONBOARD SENSING & TRACKING\n• 3D LiDAR / Depth Camera\n• Proprioceptive IMU (100 Hz)\n• Joint Encoders & Torques (tau)\n• Stance Foot Contact Forces (Fz)",
            ha="center", va="center", bbox=box_props_grey, fontsize=8.5, fontname="Times New Roman")

    ax.text(12, 28, "PERCEPTION & TRACKING MODULE\n• Moving Pedestrian Tracking (SFM)\n• Peer Quadruped Relative State (r_rel)\n• Static Obstacle Distance Field\n• Observation Covariance (Sigma_obs)",
            ha="center", va="center", bbox=box_props_yellow, fontsize=8.5, fontname="Times New Roman")

    # 2. Decision & Estimation (Middle-Left)
    ax.text(45, 52, "PROPRIOCEPTIVE BRAKING ESTIMATOR\n• Slip Velocity Detection: v_slip\n• Command Discrepancy Tracking\n• Online Estimation: a_hat_brake\n• Certified 3-sigma Lower Bound: a_safe",
            ha="center", va="center", bbox=box_props_red, fontsize=8.5, fontname="Times New Roman")

    ax.text(45, 28, "DECENTRALIZED MARL POLICY (MAPPO)\n• Goal-Seeking PD Guidance Vector\n• Local Social Force Potential Field\n• Decentralized Runtime (Zero Telemetry)\n• Output: Nominal Acceleration u_nom",
            ha="center", va="center", bbox=box_props_green, fontsize=8.5, fontname="Times New Roman")

    # 3. Safety Filter & Optimization (Middle-Right)
    ax.text(78, 40, "ROBUST HOCBF-QP SAFETY FILTER\n• Dynamic Distance Dilation:\n  d_safe = d_geom + v*T_del + v^2 / (2*a_safe)\n• Relative-Degree-2 Barrier: psi_2 >= 0\n• Quadratic Program with Slack Relaxation:\n  min 0.5||u - u_nom||^2 + lambda*delta^2\n• Active Fallback: u* = -a_safe * (v / ||v||)",
            ha="center", va="center", bbox=box_props_blue, fontsize=8.5, fontname="Times New Roman")

    # 4. Plant / Robot Hardware & Low-Level Control (Bottom)
    ax.text(45, 8, "TRANSFORMABLE FLYING-WALKING QUADRUPED PLATFORM\n• Dual-Use Rotor-Leg Kinematics (4 BLDC Motors + 8 Cycloidal Joint Servos)\n• Mode State Machine: Aerial Flight (theta=0 deg) <---> Terrestrial Crawl (theta=75 deg)\n• Low-Level Whole-Body Contact MPC / Pixhawk 6C Flight Autopilot\n• Ground Interaction: Coulomb Friction Cones (mu in [0.18, 0.88])",
            ha="center", va="center", bbox=box_props_grey, fontsize=9.0, fontweight="bold", fontname="Times New Roman")

    # Interconnecting Arrows
    arrow_args = dict(arrowstyle="->", lw=1.6, color="#0F2537")

    # Sensing to Modules
    ax.annotate("", xy=(26, 52), xytext=(30, 52), arrowprops=arrow_args)
    ax.annotate("", xy=(12, 43), xytext=(12, 37), arrowprops=arrow_args)
    
    # Perception to MAPPO and HOCBF
    ax.annotate("", xy=(26, 28), xytext=(30, 28), arrowprops=arrow_args)
    ax.annotate("", xy=(59, 28), xytext=(65, 33), arrowprops=arrow_args)

    # Estimator to HOCBF
    ax.annotate("", xy=(59, 52), xytext=(65, 47), arrowprops=arrow_args)
    ax.text(62, 52, "Certified a_safe", fontsize=7.5, color="#d9534f", fontname="Times New Roman")

    # MAPPO to HOCBF
    ax.annotate("", xy=(55, 33), xytext=(65, 37), arrowprops=arrow_args)
    ax.text(58, 37, "u_nom", fontsize=8.0, color="#5cb85c", fontname="Times New Roman")

    # HOCBF to Platform
    ax.annotate("", xy=(78, 23), xytext=(78, 16), arrowprops=arrow_args)
    ax.annotate("", xy=(78, 16), xytext=(68, 12), arrowprops=arrow_args)
    ax.text(79, 19, "Safe Commanded Acceleration u*", fontsize=8.0, color="#0275d8", fontname="Times New Roman", fontweight="bold")

    # Platform Feedback loop to Sensing
    ax.annotate("", xy=(22, 12), xytext=(12, 16), arrowprops=arrow_args)
    ax.annotate("", xy=(12, 16), xytext=(12, 43), arrowprops=arrow_args)
    ax.text(6, 20, "Proprioceptive & Inertial States (100 Hz)", rotation=90, fontsize=7.5, color="#555555", fontname="Times New Roman")

    # Title
    ax.text(50, 62, "Integrated System Architecture: Friction-Aware Safety-Critical Adaptive Control\nof Transformable Aerial-Legged Quadruped Robot Teams",
            ha="center", va="center", fontsize=11.5, fontweight="bold", fontname="Times New Roman", color="#0F2537")

    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"Generated Unified Schematic Block Diagram: {output_path}")

if __name__ == "__main__":
    out_dir = r"C:\Users\lenovo\.gemini\antigravity\scratch\Research_Work\Unified_Research_Proposal"
    os.makedirs(out_dir, exist_ok=True)
    generate_schematic_block_diagram(os.path.join(out_dir, "Unified_System_Architecture_Block_Diagram.png"))

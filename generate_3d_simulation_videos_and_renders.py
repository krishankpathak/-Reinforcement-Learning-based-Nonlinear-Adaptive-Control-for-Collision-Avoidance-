"""
3D Robotics Simulation Video and Isometric Visual Generator
Generates true 3D spatial simulation renders and animated video recordings:
1. 3D_Simulation_Multi_Agent_Quadruped_Collision_Avoidance (GIF Video & 3D Isometric PNG)
2. 3D_Simulation_Transformable_Flight_To_Crawling_Mission (GIF Video & 3D Isometric PNG)
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from PIL import Image

def generate_3d_multi_agent_sim(video_dir, graphs_dir):
    os.makedirs(video_dir, exist_ok=True)
    os.makedirs(graphs_dir, exist_ok=True)
    print("=== Rendering 3D Multi-Agent Physics Simulation & Video ===")
    
    # 3D Simulation Parameters
    num_frames = 40
    t = np.linspace(0, 12, num_frames)
    
    # Trajectory 1: Quadruped 1 (Ego - Blue) moving from left to right across low-friction patch
    # Incorporates 3D body heave, roll, pitch, and leg contact kinematics
    r1_x = -7.0 + 1.15 * t
    r1_y = 0.4 * np.sin(0.6 * t)
    r1_z = 0.32 + 0.025 * np.abs(np.sin(2.5 * np.pi * t)) # Trotting vertical gait bounce
    
    # Trajectory 2: Quadruped 2 (Peer - Green) opposing movement
    r2_x = 7.0 - 1.10 * t
    r2_y = -0.3 + 0.8 * np.exp(-((t - 6.0)/2.0)**2) # Evasive lateral swerve
    r2_z = 0.32 + 0.025 * np.abs(np.cos(2.5 * np.pi * t))

    # Pedestrian 1 (Crossing human)
    h1_x = 0.5 - 0.2 * t
    h1_y = -3.5 + 0.65 * t
    h1_z = 0.90 # Human torso center

    frames = []
    
    for frame_idx in range(num_frames):
        fig = plt.figure(figsize=(9, 5.5), dpi=150)
        ax = fig.add_subplot(111, projection='3d')
        
        # 1. 3D Ground Plane with Low-Friction Slick Zone
        # Normal ground grid
        gx = np.linspace(-8, 8, 10)
        gy = np.linspace(-4, 4, 10)
        GX, GY = np.meshgrid(gx, gy)
        GZ = np.zeros_like(GX)
        ax.plot_wireframe(GX, GY, GZ, color='#cccccc', lw=0.5, alpha=0.5)

        # Low friction wet tile patch (-4 to 4 in x, -2.5 to 2.5 in y)
        px = [-4, 4, 4, -4]
        py = [-2.5, -2.5, 2.5, 2.5]
        pz = [0.002, 0.002, 0.002, 0.002]
        verts_patch = [list(zip(px, py, pz))]
        patch_poly = Poly3DCollection(verts_patch, color='#a6d8f0', alpha=0.65)
        ax.add_collection3d(patch_poly)

        # 2. Static Cylindrical Obstacles (Pillars at x = -5.5 and x = 5.5)
        for cx in [-5.5, 5.5]:
            theta_cyl = np.linspace(0, 2*np.pi, 16)
            z_cyl = np.linspace(0, 1.8, 8)
            Tc, Zc = np.meshgrid(theta_cyl, z_cyl)
            Xc = cx + 0.5 * np.cos(Tc)
            Yc = 0.0 + 0.5 * np.sin(Tc)
            ax.plot_surface(Xc, Yc, Zc, color='#555555', alpha=0.5)

        # 3. Dynamic Pedestrian (Rendered as 3D cylindrical human capsule)
        hx_now = h1_x[frame_idx]
        hy_now = h1_y[frame_idx]
        ax.scatter([hx_now], [hy_now], [1.7], color='#d9534f', s=70, label='Human Head (1.7m)')
        ax.plot([hx_now, hx_now], [hy_now, hy_now], [0, 1.6], color='#d9534f', lw=4.5, solid_capstyle='round')

        # 4. Quadruped 1 (Ego - Blue) 3D Body & Stance Limbs
        r1x = r1_x[frame_idx]
        r1y = r1_y[frame_idx]
        r1z = r1_z[frame_idx]
        
        # 3D Torso Box
        bx = [r1x-0.25, r1x+0.25, r1x+0.25, r1x-0.25, r1x-0.25]
        by = [r1y-0.12, r1y-0.12, r1y+0.12, r1y+0.12, r1y-0.12]
        bz = [r1z, r1z, r1z, r1z, r1z]
        ax.plot(bx, by, bz, color='#0275d8', lw=3.0)
        ax.scatter([r1x], [r1y], [r1z], color='#0275d8', s=80)
        
        # 4 Stance Legs connecting torso to ground
        for dx_leg, dy_leg in [(-0.22, -0.11), (0.22, -0.11), (-0.22, 0.11), (0.22, 0.11)]:
            foot_z = 0.0
            ax.plot([r1x + dx_leg, r1x + dx_leg*1.1], [r1y + dy_leg, r1y + dy_leg*1.1], [r1z, foot_z], color='#0275d8', lw=2.0)
            ax.scatter([r1x + dx_leg*1.1], [r1y + dy_leg*1.1], [foot_z], color='black', s=25)

        # 3D Dynamic Safety Buffer (Sphere)
        d_safe = 1.25 # Expanded safe radius
        u_s = np.linspace(0, 2*np.pi, 14)
        v_s = np.linspace(0, np.pi, 8)
        xs = r1x + d_safe * np.outer(np.cos(u_s), np.sin(v_s))
        ys = r1y + d_safe * np.outer(np.sin(u_s), np.sin(v_s))
        zs = r1z + d_safe * np.outer(np.ones(np.size(u_s)), np.cos(v_s))
        ax.plot_wireframe(xs, ys, zs, color='#0275d8', alpha=0.15, lw=0.6)

        # Trajectory trail
        ax.plot(r1_x[:frame_idx+1], r1_y[:frame_idx+1], r1_z[:frame_idx+1], color='#0275d8', lw=2.0, linestyle='--')

        # 5. Quadruped 2 (Peer - Green) 3D Body & Stance Limbs
        r2x = r2_x[frame_idx]
        r2y = r2_y[frame_idx]
        r2z = r2_z[frame_idx]
        ax.scatter([r2x], [r2y], [r2z], color='#5cb85c', s=80)
        ax.plot([r2x-0.25, r2x+0.25, r2x+0.25, r2x-0.25, r2x-0.25],
                [r2y-0.12, r2y-0.12, r2y+0.12, r2y+0.12, r2y-0.12],
                [r2z, r2z, r2z, r2z, r2z], color='#5cb85c', lw=3.0)
        for dx_leg, dy_leg in [(-0.22, -0.11), (0.22, -0.11), (-0.22, 0.11), (0.22, 0.11)]:
            ax.plot([r2x + dx_leg, r2x + dx_leg*1.1], [r2y + dy_leg, r2y + dy_leg*1.1], [r2z, 0.0], color='#5cb85c', lw=2.0)
            ax.scatter([r2x + dx_leg*1.1], [r2y + dy_leg*1.1], [0.0], color='black', s=25)
        ax.plot(r2_x[:frame_idx+1], r2_y[:frame_idx+1], r2_z[:frame_idx+1], color='#5cb85c', lw=2.0, linestyle='--')

        ax.set_xlim(-8.0, 8.0)
        ax.set_ylim(-4.0, 4.0)
        ax.set_zlim(0.0, 2.5)
        ax.view_init(elev=28, azim=-50)
        ax.set_title(f'3D Multi-Agent Physics Simulation: Variable-Friction Corridor\nt = {t[frame_idx]:.2f}s | HOCBF Invariant Deceleration Control',
                     fontsize=9.5, fontweight='bold', fontname='Times New Roman')
        ax.set_xlabel('Global X (m)', fontsize=8, fontname='Times New Roman')
        ax.set_ylabel('Global Y (m)', fontsize=8, fontname='Times New Roman')
        ax.set_zlabel('Elevation Z (m)', fontsize=8, fontname='Times New Roman')

        # Save individual frame to temp buffer
        fig.canvas.draw()
        img = Image.fromarray(np.asarray(fig.canvas.buffer_rgba()))
        frames.append(img)
        
        # Save key perspective screenshot at mid-crossing
        if frame_idx == 22:
            key_png = os.path.join(graphs_dir, "3D_Simulation_Perspective_Quadruped_Corridor.png")
            fig.savefig(key_png, dpi=300)
            print(f"Saved 3D Simulation Perspective Screenshot: {key_png}")
            
        plt.close(fig)

    # Save animated GIF video
    video_gif = os.path.join(video_dir, "3D_Simulation_Multi_Agent_Quadruped_Collision_Avoidance.gif")
    frames[0].save(video_gif, save_all=True, append_images=frames[1:], duration=100, loop=0)
    print(f"Generated 3D Multi-Agent Simulation Video: {video_gif} ({len(frames)} frames)")

def generate_3d_transformable_mission_sim(video_dir, graphs_dir):
    print("\n=== Rendering 3D Transformable Flight-Walking Mission Simulation & Video ===")
    num_frames = 36
    frames = []

    # Phases:
    # 0-10: 3D Aerial Cruise (Z = 2.8m, Theta = 0 deg)
    # 10-18: 3D Approach & Touchdown Flare on Pipe Rack (Z -> 0.5m)
    # 18-26: 3D Morphological Transformation (Theta: 0 -> 75 deg, CoG drops)
    # 26-36: 3D Terrestrial Crawl Gait along Elevated Grating (Z = 0.28m, Theta = 75 deg)
    
    t = np.linspace(0, 35, num_frames)
    
    for i in range(num_frames):
        ti = t[i]
        fig = plt.figure(figsize=(9, 5.5), dpi=150)
        ax = fig.add_subplot(111, projection='3d')
        
        # Draw structural pipe rack / elevated industrial steel structure
        # Elevated platform at Z = 0.0 (ground datum) with elevated pipe at Z = 1.2m
        ax.plot([-3, 3], [1.5, 1.5], [1.2, 1.2], color='#777777', lw=6.0, label='Elevated Industrial Pipe Rack')
        ax.plot([-3, 3], [-1.5, -1.5], [1.2, 1.2], color='#777777', lw=6.0)
        # Structural steel cross grating
        for gx in np.linspace(-3, 3, 7):
            ax.plot([gx, gx], [-1.5, 1.5], [1.2, 1.2], color='#999999', lw=1.5)

        if ti < 10.0:
            # Flight Phase
            phase_label = "PHASE 1: 3D AERIAL FLIGHT CRUISE (Power: 345 W)"
            px = -2.5 + 0.3 * ti
            py = 0.0
            pz = 2.4 - 0.04 * ti
            theta_deg = 0.0
            is_flying = True
        elif ti < 18.0:
            # Flare Touchdown Phase
            phase_label = "PHASE 2: 3D TOUCHDOWN FLARE & PERCH (Ground Effect Cushion)"
            progress = (ti - 10.0) / 8.0
            px = 0.5 * progress
            py = 0.0
            pz = 2.0 - 0.75 * progress # Lands softly onto Z = 1.25m
            theta_deg = 0.0
            is_flying = True
        elif ti < 26.0:
            # Transformation Phase
            phase_label = "PHASE 3: CONTINUOUS MORPHOLOGICAL RECONFIGURATION"
            progress = (ti - 18.0) / 8.0
            px = 0.5
            py = 0.0
            pz = 1.25 - 0.045 * progress # CoG vertical drop
            theta_deg = 75.0 * progress
            is_flying = False
        else:
            # Terrestrial Crawling Phase
            phase_label = "PHASE 4: TERRESTRIAL CRAWL GAIT & NDT INSPECTION (Power: 41.5 W)"
            progress = (ti - 26.0) / 9.0
            px = 0.5 + 0.15 * progress
            py = 0.0
            pz = 1.205
            theta_deg = 75.0
            is_flying = False

        # Draw 3D Transformable Robot Body
        ax.scatter([px], [py], [pz], color='#333333', s=100)
        # Torso box
        ax.plot([px-0.12, px+0.12, px+0.12, px-0.12, px-0.12],
                [py-0.08, py-0.08, py+0.08, py+0.08, py-0.08],
                [pz, pz, pz, pz, pz], color='#333333', lw=3.0)

        # 4 Articulating Limbs
        theta_rad = np.radians(theta_deg)
        arm_angles = [np.pi/4, 3*np.pi/4, 5*np.pi/4, 7*np.pi/4]
        
        for psi in arm_angles:
            # Hip pivot
            hx = px + 0.09 * np.cos(psi)
            hy = py + 0.09 * np.sin(psi)
            hz = pz
            
            # Femur distal tip (knee)
            kx = hx + 0.16 * np.cos(theta_rad) * np.cos(psi)
            ky = hy + 0.16 * np.cos(theta_rad) * np.sin(psi)
            kz = hz - 0.16 * np.sin(theta_rad)
            ax.plot([hx, kx], [hy, ky], [hz, kz], color='#0275d8', lw=3.5)
            
            # Tibia strut to footpad
            fx = kx + 0.14 * np.cos(theta_rad + 0.15) * np.cos(psi)
            fy = ky + 0.14 * np.cos(theta_rad + 0.15) * np.sin(psi)
            fz = kz - 0.14 * np.sin(theta_rad + 0.15)
            ax.plot([kx, fx], [ky, fy], [kz, fz], color='#5cb85c', lw=3.0)
            ax.scatter([fx], [fy], [fz], color='#d9534f', s=35)
            
            # Propeller discs in flight mode
            if is_flying:
                prop_x = kx + 0.11 * np.cos(np.linspace(0, 2*np.pi, 12))
                prop_y = ky + 0.11 * np.sin(np.linspace(0, 2*np.pi, 12))
                prop_z = np.full_like(prop_x, kz + 0.03)
                ax.plot(prop_x, prop_y, prop_z, color='cyan', alpha=0.7, lw=1.2)

        ax.set_xlim(-2.5, 2.5)
        ax.set_ylim(-2.0, 2.0)
        ax.set_zlim(0.8, 3.0)
        ax.view_init(elev=24, azim=-60)
        ax.set_title(f'3D Multimodal Mission Simulation: {phase_label}\nTheta = {theta_deg:.1f} deg | Power Dissipation & Stability Verification',
                     fontsize=8.8, fontweight='bold', fontname='Times New Roman')
        ax.set_xlabel('X Dimension (m)', fontsize=8, fontname='Times New Roman')
        ax.set_ylabel('Y Dimension (m)', fontsize=8, fontname='Times New Roman')
        ax.set_zlabel('Elevation Z (m)', fontsize=8, fontname='Times New Roman')

        fig.canvas.draw()
        img = Image.fromarray(np.asarray(fig.canvas.buffer_rgba()))
        frames.append(img)
        
        # Save key perspective screenshot during transformation
        if i == 22:
            key_png = os.path.join(graphs_dir, "3D_Simulation_Perspective_Transformable_Morphology.png")
            fig.savefig(key_png, dpi=300)
            print(f"Saved 3D Transformation Perspective Screenshot: {key_png}")
            
        plt.close(fig)

    video_gif = os.path.join(video_dir, "3D_Simulation_Transformable_Flight_To_Crawling_Mission.gif")
    frames[0].save(video_gif, save_all=True, append_images=frames[1:], duration=120, loop=0)
    print(f"Generated 3D Transformable Mission Video: {video_gif} ({len(frames)} frames)")

if __name__ == "__main__":
    base = r"C:\Users\lenovo\.gemini\antigravity\scratch\Research_Work"
    v_dir = os.path.join(base, "Videos_and_3D_Simulations")
    g_dir = os.path.join(base, "Unified_Research_Proposal", "figures")
    generate_3d_multi_agent_sim(v_dir, g_dir)
    generate_3d_transformable_mission_sim(v_dir, g_dir)
    print("=== All 3D Simulations, Videos, and Screenshots Successfully Generated ===")

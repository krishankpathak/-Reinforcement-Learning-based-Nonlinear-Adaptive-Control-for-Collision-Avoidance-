"""
Parametric 3D CAD Model Synthesis & Multibody Morphing Kinematics
Project 2: Transformable Flying and Walking Inspection Robot
Generates full B-Rep 3D meshes (STL/OBJ), computes inertial tensors, CoG migration, and mass properties.
"""

import os
import numpy as np
import trimesh

def create_fuselage():
    """Central avionics and battery fuselage chassis."""
    # Main octagonal / rounded rectangular pod
    fuselage = trimesh.creation.box(extents=[0.18, 0.14, 0.065])
    # Top lid chamfer
    top_cap = trimesh.creation.box(extents=[0.16, 0.12, 0.02])
    top_cap.apply_translation([0, 0, 0.04])
    # Sensor turret / NDT ultrasonic probe bay
    probe_bay = trimesh.creation.cylinder(radius=0.03, height=0.035)
    probe_bay.apply_translation([0.07, 0, -0.04])
    return trimesh.util.concatenate([fuselage, top_cap, probe_bay])

def create_limb_link(length=0.16, width=0.028, height=0.018):
    """Hollow rectangular carbon-fiber composite structural arm."""
    link = trimesh.creation.box(extents=[length, width, height])
    # Pivot joint knuckle
    joint_knuckle = trimesh.creation.cylinder(radius=0.016, height=width*1.1)
    joint_knuckle.apply_transform(trimesh.transformations.rotation_matrix(np.pi/2, [1, 0, 0]))
    joint_knuckle.apply_translation([-length/2, 0, 0])
    return trimesh.util.concatenate([link, joint_knuckle])

def create_motor_rotor_assembly():
    """BLDC motor housing and 9-inch propeller disc."""
    # Stator / rotor bell
    bell = trimesh.creation.cylinder(radius=0.018, height=0.022)
    shaft = trimesh.creation.cylinder(radius=0.003, height=0.015)
    shaft.apply_translation([0, 0, 0.015])
    # Propeller blade envelope (9x4.5 inch)
    blade1 = trimesh.creation.box(extents=[0.228, 0.02, 0.003])
    blade1.apply_translation([0, 0, 0.02])
    return trimesh.util.concatenate([bell, shaft, blade1])

def create_landing_foot():
    """Distal silicone compliant footpad with integrated ground contact pivot."""
    foot = trimesh.creation.cone(radius=0.02, height=0.03)
    foot.apply_transform(trimesh.transformations.rotation_matrix(np.pi, [1, 0, 0]))
    return foot

def build_full_robot(morph_angle_deg=0.0):
    """
    Assembles the 4-limb transformable robot at specified morphing angle:
    morph_angle_deg = 0.0 -> Flight Configuration
    morph_angle_deg = 75.0 -> Terrestrial Walking Configuration
    """
    chassis = create_fuselage()
    components = [chassis]
    
    arm_angles = [np.pi/4, 3*np.pi/4, 5*np.pi/4, 7*np.pi/4]
    morph_rad = np.radians(morph_angle_deg)
    
    hip_mount_radius = 0.09
    femur_len = 0.16
    tibia_len = 0.14
    
    for i, psi in enumerate(arm_angles):
        # Hip mount position on chassis corner
        hip_x = hip_mount_radius * np.cos(psi)
        hip_y = hip_mount_radius * np.sin(psi)
        hip_z = 0.0
        
        # 1. Femur boom
        femur = create_limb_link(length=femur_len)
        # Apply transformation angle (pitch down)
        femur.apply_translation([femur_len/2, 0, 0])
        femur.apply_transform(trimesh.transformations.rotation_matrix(morph_rad, [0, 1, 0]))
        # Orient to arm quadrant
        femur.apply_transform(trimesh.transformations.rotation_matrix(psi, [0, 0, 1]))
        femur.apply_translation([hip_x, hip_y, hip_z])
        components.append(femur)
        
        # Knee position in global frame
        knee_x = hip_x + femur_len * np.cos(morph_rad) * np.cos(psi)
        knee_y = hip_y + femur_len * np.cos(morph_rad) * np.sin(psi)
        knee_z = hip_z - femur_len * np.sin(morph_rad)
        
        # 2. Tibia strut
        tibia = create_limb_link(length=tibia_len)
        tibia_pitch = morph_rad + np.radians(15.0 if morph_angle_deg > 10 else 0)
        tibia.apply_translation([tibia_len/2, 0, 0])
        tibia.apply_transform(trimesh.transformations.rotation_matrix(tibia_pitch, [0, 1, 0]))
        tibia.apply_transform(trimesh.transformations.rotation_matrix(psi, [0, 0, 1]))
        tibia.apply_translation([knee_x, knee_y, knee_z])
        components.append(tibia)
        
        # 3. Motor & Propeller assembly
        motor = create_motor_rotor_assembly()
        if morph_angle_deg < 20.0:
            # Flight mode: motors face strictly upward
            motor.apply_translation([knee_x, knee_y, knee_z + 0.02])
        else:
            # Terrestrial mode: motors stowed and tilted inward
            motor.apply_transform(trimesh.transformations.rotation_matrix(np.radians(45), [0, 1, 0]))
            motor.apply_transform(trimesh.transformations.rotation_matrix(psi, [0, 0, 1]))
            motor.apply_translation([knee_x, knee_y, knee_z + 0.03])
        components.append(motor)
        
        # 4. Footpad at distal tip
        foot_x = knee_x + tibia_len * np.cos(tibia_pitch) * np.cos(psi)
        foot_y = knee_y + tibia_len * np.cos(tibia_pitch) * np.sin(psi)
        foot_z = knee_z - tibia_len * np.sin(tibia_pitch)
        foot = create_landing_foot()
        foot.apply_translation([foot_x, foot_y, foot_z])
        components.append(foot)

    full_assembly = trimesh.util.concatenate(components)
    return full_assembly

def analyze_morphing_properties():
    """
    Computes mass properties, center of gravity migration, and inertia tensor
    across transformation angle theta in [0, 90] degrees.
    """
    angles = np.linspace(0, 85, 18)
    cog_z_list = []
    j_xx_list = []
    j_yy_list = []
    j_zz_list = []
    
    # Material density: composite/aluminum hybrid effective density ~ 1650 kg/m^3
    target_mass = 2.45 # kg
    
    print("Evaluating multibody kinematic inertia migration...")
    for theta in angles:
        mesh = build_full_robot(theta)
        vol = mesh.volume
        density = target_mass / (vol + 1e-8)
        mesh.density = density
        
        cog = mesh.center_mass
        cog_z_list.append(cog[2] * 1000.0) # in mm
        
        inertia = mesh.moment_inertia
        j_xx_list.append(inertia[0, 0])
        j_yy_list.append(inertia[1, 1])
        j_zz_list.append(inertia[2, 2])

    return angles, np.array(cog_z_list), np.array(j_xx_list), np.array(j_yy_list), np.array(j_zz_list)

if __name__ == "__main__":
    cad_dir = os.path.dirname(__file__)
    print("=== Generating 3D CAD Geometry Models for Project 2 ===")
    
    # 1. Export Flight Configuration Model (theta = 0 deg)
    flight_robot = build_full_robot(morph_angle_deg=0.0)
    flight_stl = os.path.join(cad_dir, "transformable_robot_flight_config.stl")
    flight_obj = os.path.join(cad_dir, "transformable_robot_flight_config.obj")
    flight_robot.export(flight_stl)
    flight_robot.export(flight_obj)
    print(f"Exported Flight CAD Model: {flight_stl} ({len(flight_robot.faces)} faces)")
    
    # 2. Export Terrestrial Walking Configuration Model (theta = 75 deg)
    walk_robot = build_full_robot(morph_angle_deg=75.0)
    walk_stl = os.path.join(cad_dir, "transformable_robot_walking_config.stl")
    walk_obj = os.path.join(cad_dir, "transformable_robot_walking_config.obj")
    walk_robot.export(walk_stl)
    walk_robot.export(walk_obj)
    print(f"Exported Walking CAD Model: {walk_stl} ({len(walk_robot.faces)} faces)")

    # 3. Analyze Morphological Kinematics & Save Data
    angles, cog_z, jxx, jyy, jzz = analyze_morphing_properties()
    
    kinematics_data = np.column_stack([angles, cog_z, jxx, jyy, jzz])
    data_path = os.path.join(cad_dir, "..", "Results", "morphing_kinematics_properties.csv")
    os.makedirs(os.path.dirname(data_path), exist_ok=True)
    np.savetxt(data_path, kinematics_data, delimiter=",", 
               header="Morph_Angle_deg,CoG_Z_mm,Jxx_kg_m2,Jyy_kg_m2,Jzz_kg_m2", comments="")
    print(f"Saved Morphing Kinematics Properties to: {data_path}")
    print(f"CoG vertical drop from 0 deg to 75 deg: {cog_z[0] - cog_z[-1]:.2f} mm")
    print(f"Yaw inertia reduction: {(1.0 - jzz[-1]/jzz[0])*100.0:.1f}%")

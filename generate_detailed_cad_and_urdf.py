"""
Detailed 3D CAD Part Generator and URDF/SDF Model Synthesis
Generates individual mechanical parts (Chassis, Knuckle, Femur, Tibia, Motor, Footpad, Probe),
assembles full flight & walking configurations, and generates ROS 2 / Gazebo URDF/Xacro models.
"""

import os
import trimesh
import numpy as np

def generate_individual_cad_parts(cad_dir):
    os.makedirs(cad_dir, exist_ok=True)
    parts_dir = os.path.join(cad_dir, "parts")
    os.makedirs(parts_dir, exist_ok=True)
    
    print("=== Synthesizing Individual 3D Mechanical Part Models ===")
    
    # 1. Main Fuselage Chassis (with electronics compartment, battery bay, lidar mount)
    fuselage_body = trimesh.creation.box(extents=[0.18, 0.14, 0.065])
    lidar_puck = trimesh.creation.cylinder(radius=0.035, height=0.03)
    lidar_puck.apply_translation([0, 0, 0.045])
    chassis = trimesh.util.concatenate([fuselage_body, lidar_puck])
    chassis.export(os.path.join(parts_dir, "chassis_fuselage.stl"))
    print("Exported: parts/chassis_fuselage.stl")

    # 2. 7075-T6 Aluminum Hip Yoke Knuckle
    knuckle_base = trimesh.creation.cylinder(radius=0.018, height=0.035)
    knuckle_flange = trimesh.creation.box(extents=[0.03, 0.025, 0.02])
    knuckle_flange.apply_translation([0.02, 0, 0])
    knuckle = trimesh.util.concatenate([knuckle_base, knuckle_flange])
    knuckle.export(os.path.join(parts_dir, "hip_yoke_knuckle.stl"))
    print("Exported: parts/hip_yoke_knuckle.stl")

    # 3. Carbon Fiber Composite Femur Boom Link (Length 0.16m, square profile 20x20mm)
    femur = trimesh.creation.box(extents=[0.16, 0.022, 0.022])
    femur.apply_translation([0.08, 0, 0])
    femur.export(os.path.join(parts_dir, "femur_rotor_boom.stl"))
    print("Exported: parts/femur_rotor_boom.stl")

    # 4. Carbon Fiber Tibia Landing Strut (Length 0.14m)
    tibia = trimesh.creation.box(extents=[0.14, 0.018, 0.018])
    tibia.apply_translation([0.07, 0, 0])
    tibia.export(os.path.join(parts_dir, "tibia_landing_strut.stl"))
    print("Exported: parts/tibia_landing_strut.stl")

    # 5. BLDC Motor Housing & 9-inch Propeller Assembly
    motor_stator = trimesh.creation.cylinder(radius=0.017, height=0.024)
    prop_disc = trimesh.creation.cylinder(radius=0.114, height=0.003)
    prop_disc.apply_translation([0, 0, 0.02])
    prop_assembly = trimesh.util.concatenate([motor_stator, prop_disc])
    prop_assembly.export(os.path.join(parts_dir, "motor_bell_9inch_prop.stl"))
    print("Exported: parts/motor_bell_9inch_prop.stl")

    # 6. Molded Silicone Ground Contact Footpad
    foot = trimesh.creation.cone(radius=0.02, height=0.032)
    foot.apply_transform(trimesh.transformations.rotation_matrix(np.pi, [1, 0, 0]))
    foot.export(os.path.join(parts_dir, "silicone_contact_foot.stl"))
    print("Exported: parts/silicone_contact_foot.stl")

    # 7. NDT Ultrasonic Thickness Probe
    probe = trimesh.creation.cylinder(radius=0.014, height=0.04)
    probe.apply_translation([0, 0, -0.02])
    probe.export(os.path.join(parts_dir, "ndt_ultrasonic_probe.stl"))
    print("Exported: parts/ndt_ultrasonic_probe.stl")

def generate_urdf_and_sdf(urdf_dir, worlds_dir):
    os.makedirs(urdf_dir, exist_ok=True)
    os.makedirs(worlds_dir, exist_ok=True)
    
    print("\n=== Generating ROS 2 URDF/Xacro and Gazebo Simulation SDF ===")
    
    # Parametric URDF/Xacro
    urdf_content = """<?xml version="1.0"?>
<robot name="transformable_quadruped" xmlns:xacro="http://www.ros.org/wiki/xacro">

  <!-- Physical Constants -->
  <xacro:property name="total_mass" value="2.45" />
  <xacro:property name="chassis_mass" value="1.25" />
  <xacro:property name="femur_mass" value="0.18" />
  <xacro:property name="tibia_mass" value="0.12" />
  <xacro:property name="femur_length" value="0.16" />
  <xacro:property name="tibia_length" value="0.14" />

  <!-- Base Footprint & Center of Mass -->
  <link name="base_footprint"/>

  <joint name="base_joint" type="fixed">
    <parent link="base_footprint"/>
    <child link="base_link"/>
    <origin xyz="0 0 0.22" rpy="0 0 0"/>
  </joint>

  <!-- Fuselage Chassis Link -->
  <link name="base_link">
    <inertial>
      <mass value="${chassis_mass}"/>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <inertia ixx="0.0052" ixy="0.0" ixz="0.0" iyy="0.0078" iyz="0.0" izz="0.0115"/>
    </inertial>
    <visual>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <box size="0.18 0.14 0.065"/>
      </geometry>
      <material name="dark_grey">
        <color rgba="0.2 0.2 0.2 1.0"/>
      </material>
    </visual>
    <collision>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <box size="0.18 0.14 0.065"/>
      </geometry>
    </collision>
  </link>

  <!-- Macro for 4 Transformable Rotor-Leg Limbs -->
  <xacro:macro name="rotor_leg" params="prefix quadrant angle_z">
    <!-- Hip Roll / Yaw Knuckle Joint -->
    <joint name="${prefix}_hip_joint" type="revolute">
      <parent link="base_link"/>
      <child link="${prefix}_femur_link"/>
      <origin xyz="${0.09 * cos(angle_z)} ${0.09 * sin(angle_z)} 0" rpy="0 0 ${angle_z}"/>
      <axis xyz="0 1 0"/>
      <limit lower="-0.1" upper="1.57" effort="12.0" velocity="4.5"/>
      <dynamics damping="0.15" friction="0.05"/>
    </joint>

    <!-- Femur Boom Link (Houses BLDC motor and propeller) -->
    <link name="${prefix}_femur_link">
      <inertial>
        <mass value="${femur_mass}"/>
        <origin xyz="${femur_length/2} 0 0" rpy="0 0 0"/>
        <inertia ixx="0.00012" ixy="0" ixz="0" iyy="0.00045" iyz="0" izz="0.00045"/>
      </inertial>
      <visual>
        <origin xyz="${femur_length/2} 0 0" rpy="0 0 0"/>
        <geometry>
          <box size="${femur_length} 0.022 0.022"/>
        </geometry>
        <material name="carbon_fiber">
          <color rgba="0.1 0.1 0.1 1.0"/>
        </material>
      </visual>
      <collision>
        <origin xyz="${femur_length/2} 0 0" rpy="0 0 0"/>
        <geometry>
          <box size="${femur_length} 0.022 0.022"/>
        </geometry>
      </collision>
    </link>

    <!-- Knee Pitch Joint -->
    <joint name="${prefix}_knee_joint" type="revolute">
      <parent link="${prefix}_femur_link"/>
      <child link="${prefix}_tibia_link"/>
      <origin xyz="${femur_length} 0 0" rpy="0 0 0"/>
      <axis xyz="0 1 0"/>
      <limit lower="0.0" upper="2.09" effort="8.0" velocity="6.0"/>
      <dynamics damping="0.1" friction="0.02"/>
    </joint>

    <!-- Tibia Strut Link -->
    <link name="${prefix}_tibia_link">
      <inertial>
        <mass value="${tibia_mass}"/>
        <origin xyz="${tibia_length/2} 0 0" rpy="0 0 0"/>
        <inertia ixx="0.00008" ixy="0" ixz="0" iyy="0.00028" iyz="0" izz="0.00028"/>
      </inertial>
      <visual>
        <origin xyz="${tibia_length/2} 0 0" rpy="0 0 0"/>
        <geometry>
          <box size="${tibia_length} 0.018 0.018"/>
        </geometry>
        <material name="blue">
          <color rgba="0.1 0.3 0.8 1.0"/>
        </material>
      </visual>
      <collision>
        <origin xyz="${tibia_length/2} 0 0" rpy="0 0 0"/>
        <geometry>
          <box size="${tibia_length} 0.018 0.018"/>
        </geometry>
      </collision>
    </link>

    <!-- Footpad Link with Dynamic Ground Friction Parameters -->
    <joint name="${prefix}_foot_joint" type="fixed">
      <parent link="${prefix}_tibia_link"/>
      <child link="${prefix}_foot_link"/>
      <origin xyz="${tibia_length} 0 0" rpy="0 0 0"/>
    </joint>

    <link name="${prefix}_foot_link">
      <collision>
        <geometry>
          <sphere radius="0.02"/>
        </geometry>
      </collision>
    </link>

    <!-- Gazebo Contact and Surface Friction Properties -->
    <gazebo reference="${prefix}_foot_link">
      <mu1>0.85</mu1>
      <mu2>0.85</mu2>
      <kp>1000000.0</kp>
      <kd>100.0</kd>
      <minDepth>0.001</minDepth>
      <material>Gazebo/Red</material>
    </gazebo>
  </xacro:macro>

  <!-- Instantiate 4 Limbs: FL, FR, RL, RR -->
  <xacro:rotor_leg prefix="fl" quadrant="1" angle_z="0.785398"/>
  <xacro:rotor_leg prefix="fr" quadrant="2" angle_z="2.356194"/>
  <xacro:rotor_leg prefix="rl" quadrant="3" angle_z="3.926991"/>
  <xacro:rotor_leg prefix="rr" quadrant="4" angle_z="5.497787"/>

  <!-- IMU Sensor Plugin -->
  <gazebo reference="base_link">
    <sensor name="imu_sensor" type="imu">
      <always_on>true</always_on>
      <update_rate>100</update_rate>
      <topic>/imu/data</topic>
    </sensor>
  </gazebo>

  <!-- Gazebo ROS 2 Joint Controller Plugin -->
  <gazebo>
    <plugin filename="gz-sim-joint-position-controller-system" name="gz::sim::systems::JointPositionController">
      <sub_topic>/cmd_joint_positions</sub_topic>
    </plugin>
  </gazebo>

</robot>
"""
    urdf_path = os.path.join(urdf_dir, "transformable_quadruped.urdf.xacro")
    with open(urdf_path, "w") as f:
        f.write(urdf_content)
    print(f"Generated ROS 2 URDF: {urdf_path}")

    # Gazebo World SDF with Variable Friction Floor Zones
    world_content = """<?xml version="1.0" ?>
<sdf version="1.8">
  <world name="variable_friction_corridor">
    <physics name="1ms" type="ignored">
      <max_step_size>0.002</max_step_size>
      <real_time_factor>1.0</real_time_factor>
    </physics>

    <!-- Global Sun & Lighting -->
    <light type="directional" name="sun">
      <cast_shadows>true</cast_shadows>
      <pose>0 0 10 0 0 0</pose>
      <diffuse>0.8 0.8 0.8 1</diffuse>
      <specular>0.2 0.2 0.2 1</specular>
      <direction>-0.5 0.1 -0.9</direction>
    </light>

    <!-- Normal Concrete Floor (mu = 0.75) -->
    <model name="concrete_ground">
      <static>true</static>
      <link name="link">
        <collision name="collision">
          <geometry>
            <plane><normal>0 0 1</normal><size>30 30</size></plane>
          </geometry>
          <surface>
            <friction>
              <ode><mu>0.75</mu><mu2>0.75</mu2></ode>
            </friction>
          </surface>
        </collision>
        <visual name="visual">
          <geometry>
            <plane><normal>0 0 1</normal><size>30 30</size></plane>
          </geometry>
          <material><ambient>0.6 0.6 0.6 1</ambient><diffuse>0.6 0.6 0.6 1</diffuse></material>
        </visual>
      </link>
    </model>

    <!-- Low Friction Wet Tile Corridor (mu = 0.22) -->
    <model name="wet_tile_zone">
      <static>true</static>
      <pose>0 0 0.001 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry>
            <box><size>8.0 5.0 0.002</size></box>
          </geometry>
          <surface>
            <friction>
              <ode><mu>0.22</mu><mu2>0.22</mu2></ode>
            </friction>
          </surface>
        </collision>
        <visual name="visual">
          <geometry>
            <box><size>8.0 5.0 0.002</size></box>
          </geometry>
          <material><ambient>0.2 0.5 0.9 0.8</ambient><diffuse>0.2 0.5 0.9 0.8</diffuse></material>
        </visual>
      </link>
    </model>

    <!-- Static Obstacle Pillars -->
    <model name="pillar_left">
      <static>true</static>
      <pose>-6.0 0 1.0 0 0 0</pose>
      <link name="link">
        <collision name="col"><geometry><cylinder><radius>0.6</radius><length>2.0</length></cylinder></geometry></collision>
        <visual name="vis"><geometry><cylinder><radius>0.6</radius><length>2.0</length></cylinder></geometry></visual>
      </link>
    </model>

    <model name="pillar_right">
      <static>true</static>
      <pose>6.0 0 1.0 0 0 0</pose>
      <link name="link">
        <collision name="col"><geometry><cylinder><radius>0.6</radius><length>2.0</length></cylinder></geometry></collision>
        <visual name="vis"><geometry><cylinder><radius>0.6</radius><length>2.0</length></cylinder></geometry></visual>
      </link>
    </model>

  </world>
</sdf>
"""
    world_path = os.path.join(worlds_dir, "variable_friction_corridor.sdf")
    with open(world_path, "w") as f:
        f.write(world_content)
    print(f"Generated Gazebo World SDF: {world_path}")

if __name__ == "__main__":
    base_p2 = r"C:\Users\lenovo\.gemini\antigravity\scratch\Research_Work\Project_2_Transformable_Robot\CAD"
    base_ros = r"C:\Users\lenovo\.gemini\antigravity\scratch\Research_Work\Project_1_Quadruped_MultiAgent\ROS2_Workspace"
    generate_individual_cad_parts(base_p2)
    generate_urdf_and_sdf(os.path.join(base_ros, "urdf"), os.path.join(base_ros, "worlds"))

# Step-by-Step Software Execution Guide
**Autonomous Robotics Research Suite**

---

## 1. System Requirements & Dependencies
- **Python Version:** 3.11+ (Confirmed working on standard Windows Python).
- **Core Scientific Libraries:** `numpy`, `scipy`, `matplotlib`, `pandas`, `trimesh`, `reportlab`.
- **Hardware Compatibility:** Executes purely on standard multi-threaded CPU; no GPU or cloud server needed.

---

## 2. Reproducing Project 1 (Quadruped Multi-Agent Simulation)

### Step 2.1: Run Full Multi-Agent Simulation & Baseline Benchmarking
To execute the multi-agent simulation, run controlled braking experiments across variable friction ($\mu \in [0.2, 0.8]$), evaluate all 5 baselines (B1 to B5), log CSV data, and generate high-resolution figures:
```powershell
python "C:\Users\lenovo\Desktop\Research_Work\Project_1_Quadruped_MultiAgent\Experiments\generate_plots.py"
```
*Outputs generated:*
- `Results/experiment_A_braking_results.csv`
- `Results/benchmark_baselines_results.csv`
- `Graphs/Fig1_braking_estimation_and_calibration.png`
- `Graphs/Fig2_multi_agent_trajectories_variable_friction.png`
- `Graphs/Fig3_hocbf_barrier_margin_time_series.png`
- `Graphs/Fig4_baseline_collision_and_safety_comparison.png`
- `Graphs/Fig5_solver_execution_latency_distribution.png`

### Step 2.2: Verify ROS 2 Node Architecture
To test the modular ROS 2 node architecture and message flow:
```powershell
python "C:\Users\lenovo\Desktop\Research_Work\Project_1_Quadruped_MultiAgent\ROS2_Workspace\ros2_nodes.py"
```

---

## 3. Reproducing Project 2 (Transformable Inspection Robot)

### Step 3.1: Generate 3D CAD Meshes & Multibody Kinematics
To synthesize the full 3D B-Rep CAD models for both Flight and Walking configurations, export STL/OBJ files, and evaluate CoG migration:
```powershell
python "C:\Users\lenovo\Desktop\Research_Work\Project_2_Transformable_Robot\CAD\generate_cad_and_kinematics.py"
```
*Outputs generated:*
- `CAD/transformable_robot_flight_config.stl` (2600 triangular facets)
- `CAD/transformable_robot_flight_config.obj`
- `CAD/transformable_robot_walking_config.stl` (2600 triangular facets)
- `CAD/transformable_robot_walking_config.obj`
- `Results/morphing_kinematics_properties.csv`

### Step 3.2: Execute FEA, CFD Downwash, and Multimodal Mission Simulation
To run the structural FEA under 3.5g impact, CFD rotor downwash analysis, and 45-second multimodal mission simulation:
```powershell
python "C:\Users\lenovo\Desktop\Research_Work\Project_2_Transformable_Robot\run_project2_all.py"
```
*Outputs generated:*
- `Results/fea_structural_stress_results.csv`
- `Results/cfd_ground_effect_results.csv`
- `Results/multimodal_mission_telemetry.csv`
- `Graphs/Fig1_cad_flight_and_walking_morphology.png`
- `Graphs/Fig2_morphing_cog_and_inertia_migration.png`
- `Graphs/Fig3_fea_structural_stress_and_deflection.png`
- `Graphs/Fig4_cfd_downwash_and_aerodynamic_interference.png`
- `Graphs/Fig5_multimodal_mission_power_and_gait_stability.png`

---

## 4. Re-compiling Research Papers (PDF & DOCX)

To re-compile both full 5-page research reports:
```powershell
python "C:\Users\lenovo\Desktop\Research_Work\generate_pdf_reports.py"
python "C:\Users\lenovo\Desktop\Research_Work\generate_docx_reports.py"
```
*Outputs generated:*
- `Project_1_Quadruped_MultiAgent/Report/Project_1_Research_Paper.pdf`
- `Project_1_Quadruped_MultiAgent/Report/Project_1_Research_Paper.docx`
- `Project_2_Transformable_Robot/Report/Project_2_Research_Paper.pdf`
- `Project_2_Transformable_Robot/Report/Project_2_Research_Paper.docx`

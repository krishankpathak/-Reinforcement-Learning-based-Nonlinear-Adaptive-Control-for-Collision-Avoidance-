# Autonomous Multidisciplinary Robotics Research Suite
**Dual Advanced Robotics Research Projects: Full Engineering Implementation, Multiphysics Modeling, and Scientific Reports**

---

## Workspace Locations
This entire research suite is fully installed, executed, and mirrored at:
1. **Primary Project Workspace:** `C:\Users\lenovo\.gemini\antigravity\scratch\Research_Work`
2. **Desktop Mirror (Easy Access):** `C:\Users\lenovo\Desktop\Research_Work`
3. **User Home Mirror:** `C:\Users\lenovo\Research_Work`

---

## Executive Overview of Both Projects

```
========================================================================================
PROJECT 1: REINFORCEMENT LEARNING-BASED NONLINEAR ADAPTIVE CONTROL FOR COLLISION AVOIDANCE
           OF MULTIPLE QUADRUPED ROBOTS IN HUMAN-AWARE OPERATIONS
========================================================================================
Core Novelty: Online proprioceptive estimation of effective braking capability (a_safe)
              coupled to a relative-degree-two Robust High-Order Control Barrier Function
              (HOCBF-QP) filter for decentralized quadruped teams in crowded variable-friction environments.
Key Result:   0.0% collision rate & 100% mission success across slippery surfaces (mu in [0.2, 0.8]),
              compared to an 80.0% collision failure rate for conventional fixed-margin CBFs.
Deliverables: Simulation benchmark, recursive estimator, HOCBF-QP solver, MAPPO policy,
              5 publication figures, raw telemetry CSVs, ROS 2 nodes, 5-page PDF & DOCX papers.

========================================================================================
PROJECT 2: GENERATIVE DESIGN, MULTIPHYSICS MODELING, AND FABRICATION OF A TRANSFORMABLE
           FLYING AND WALKING INSPECTION ROBOT
========================================================================================
Core Novelty: Kinematically shared 4-limb rotor-arm morphology where composite multirotor booms
              articulate via high-torque cycloidal joints to become quadruped crawling limbs,
              eliminating parasitic deadweight.
Key Result:   45.79 mm vertical CoG drop enhancing tipping stability; 74.4% yaw inertia reduction;
              FEA factor of safety of 83.2 under 3.5g landing impact; 87.8% power reduction
              in terrestrial crawling (41.5 W) vs. aerial hover (345 W), extending mission life 7.7x.
Deliverables: 3D CAD models (STL/OBJ), multibody dynamics, FEA structural simulation, CFD downwash
              modeling, multimodal mission telemetry, complete BOM ($1,953.60), 5-page PDF & DOCX papers.
========================================================================================
```

---

## Complete Directory Architecture
```
Research_Work/
├── Common_Resources/
│   ├── Environment_Report/
│   │   └── ENVIRONMENT_FEASIBILITY_REPORT.md
│   ├── References/
│   └── Documentation/
│
├── Project_1_Quadruped_MultiAgent/
│   ├── Literature/
│   │   └── LITERATURE_REVIEW_AND_GAP_ANALYSIS.md
│   ├── Mathematical_Model/
│   │   └── MATHEMATICAL_FORMULATION.md
│   ├── Simulation/
│   │   └── quadruped_physics_env.py
│   ├── Adaptive_Control/
│   │   └── braking_estimator.py
│   ├── CBF_Safety_Filter/
│   │   └── hocbf_filter.py
│   ├── Reinforcement_Learning/
│   │   └── mappo_navigation.py
│   ├── Experiments/
│   │   ├── run_all_experiments.py
│   │   └── generate_plots.py
│   ├── Results/
│   │   ├── experiment_A_braking_results.csv
│   │   └── benchmark_baselines_results.csv
│   ├── Graphs/
│   │   ├── Fig1_braking_estimation_and_calibration.png
│   │   ├── Fig2_multi_agent_trajectories_variable_friction.png
│   │   ├── Fig3_hocbf_barrier_margin_time_series.png
│   │   ├── Fig4_baseline_collision_and_safety_comparison.png
│   │   └── Fig5_solver_execution_latency_distribution.png
│   ├── ROS2_Workspace/
│   │   └── ros2_nodes.py
│   └── Report/
│       ├── Project_1_Research_Paper.pdf  <-- (Publication A4 PDF)
│       └── Project_1_Research_Paper.docx <-- (Editable OpenXML DOCX)
│
├── Project_2_Transformable_Robot/
│   ├── Literature/
│   │   └── LITERATURE_REVIEW_AND_GAP_ANALYSIS.md
│   ├── Concept_Development/
│   │   └── CONCEPT_TRADE_OFF_AND_SELECTION.md
│   ├── Dynamics/
│   │   └── FLIGHT_WALKING_TRANSFORMATION_DYNAMICS.md
│   ├── CAD/
│   │   ├── generate_cad_and_kinematics.py
│   │   ├── transformable_robot_flight_config.stl
│   │   ├── transformable_robot_flight_config.obj
│   │   ├── transformable_robot_walking_config.stl
│   │   └── transformable_robot_walking_config.obj
│   ├── Results/
│   │   ├── morphing_kinematics_properties.csv
│   │   ├── fea_structural_stress_results.csv
│   │   ├── cfd_ground_effect_results.csv
│   │   └── multimodal_mission_telemetry.csv
│   ├── Graphs/
│   │   ├── Fig1_cad_flight_and_walking_morphology.png
│   │   ├── Fig2_morphing_cog_and_inertia_migration.png
│   │   ├── Fig3_fea_structural_stress_and_deflection.png
│   │   ├── Fig4_cfd_downwash_and_aerodynamic_interference.png
│   │   └── Fig5_multimodal_mission_power_and_gait_stability.png
│   ├── Manufacturing/
│   │   └── BILL_OF_MATERIALS_AND_FABRICATION.md
│   ├── run_project2_all.py
│   └── Report/
│       ├── Project_2_Research_Paper.pdf  <-- (Publication A4 PDF)
│       └── Project_2_Research_Paper.docx <-- (Editable OpenXML DOCX)
│
├── README.md
├── EXECUTION_GUIDE.md
├── EXPERIMENT_STATUS.md
└── FILE_INVENTORY.md
```

# Comprehensive File & Artifact Inventory
**Autonomous Robotics Research Suite**

---

## 1. Common Resources & Environment
- `Common_Resources/Environment_Report/ENVIRONMENT_FEASIBILITY_REPORT.md`: System diagnostics, CPU/RAM/GPU capabilities, software versions, and computational feasibility analysis.
- `README.md`: Master project overview, executive summaries, and directory maps.
- `EXECUTION_GUIDE.md`: Step-by-step terminal execution instructions for replicating all simulations.
- `EXPERIMENT_STATUS.md`: Traceability matrix distinguishing completed simulations from proposed physical hardware trials.
- `FILE_INVENTORY.md`: This comprehensive file directory catalog.

---

## 2. Project 1: Multi-Agent Quadruped Safety & Navigation
- `Literature/LITERATURE_REVIEW_AND_GAP_ANALYSIS.md`: Systematic literature review, comparative taxonomy matrix, and formal research gap identification.
- `Mathematical_Model/MATHEMATICAL_FORMULATION.md`: Centroidal quadruped dynamics, Coulomb friction cone bounds, recursive estimator formulation, and relative-degree-two Robust HOCBF derivations.
- `Simulation/quadruped_physics_env.py`: Full multi-agent physics environment with variable-friction zones and Social Force Model pedestrians.
- `Adaptive_Control/braking_estimator.py`: Proprioceptive online effective braking capability and uncertainty estimator.
- `CBF_Safety_Filter/hocbf_filter.py`: Real-time Relative-Degree-2 HOCBF-QP optimization solver with emergency friction fallback.
- `Reinforcement_Learning/mappo_navigation.py`: Decentralized MAPPO policy for nominal guidance.
- `Experiments/run_all_experiments.py`: Master benchmark runner executing Experiments A-G across Baselines B1-B5.
- `Experiments/generate_plots.py`: High-speed benchmark and figure generation script.
- `ROS2_Workspace/ros2_nodes.py`: Modular ROS 2 node architecture (`/braking_estimator`, `/safety_filter`, `/safety_monitor`).
- `Results/experiment_A_braking_results.csv`: Logged convergence, RMSE, and stopping distances across $\mu \in [0.2, 0.8]$.
- `Results/benchmark_baselines_results.csv`: Comparative performance table for Baselines B1 to B5.
- `Graphs/Fig1_braking_estimation_and_calibration.png`: Convergence of $\hat{a}_{\mathrm{brake}}$ and stopping distance bar charts.
- `Graphs/Fig2_multi_agent_trajectories_variable_friction.png`: Comparative trajectory plots of Baseline B2 vs. Proposed B5.
- `Graphs/Fig3_hocbf_barrier_margin_time_series.png`: Time series of barrier function $\psi_0(t)$ forward invariance.
- `Graphs/Fig4_baseline_collision_and_safety_comparison.png`: Collision frequency and pedestrian clearance comparison bars.
- `Graphs/Fig5_solver_execution_latency_distribution.png`: Solver latency probability density distribution.
- `Report/Project_1_Research_Paper.pdf`: Publication-formatted ~5-page research paper with embedded vector figures.
- `Report/Project_1_Research_Paper.docx`: Fully editable OpenXML Word manuscript.

---

## 3. Project 2: Transformable Inspection Robot
- `Literature/LITERATURE_REVIEW_AND_GAP_ANALYSIS.md`: Review of hybrid aerial-terrestrial robots and research gap formulation.
- `Concept_Development/CONCEPT_TRADE_OFF_AND_SELECTION.md`: Structural concept analysis (Concepts A, B, C) and weighted decision matrix.
- `Dynamics/FLIGHT_WALKING_TRANSFORMATION_DYNAMICS.md`: 6-DOF flight Newton-Euler equations, Euler-Lagrange transformation dynamics, and ZMP walking stability.
- `CAD/generate_cad_and_kinematics.py`: Parametric 3D CAD mesh generator and multibody kinematics evaluator.
- `CAD/transformable_robot_flight_config.stl`: Exported 3D STL mesh of flight configuration ($\theta=0^\circ$).
- `CAD/transformable_robot_flight_config.obj`: OBJ wave-front mesh of flight configuration.
- `CAD/transformable_robot_walking_config.stl`: Exported 3D STL mesh of terrestrial crawling configuration ($\theta=75^\circ$).
- `CAD/transformable_robot_walking_config.obj`: OBJ wave-front mesh of terrestrial configuration.
- `Results/morphing_kinematics_properties.csv`: CoG vertical drop and principal mass moment of inertia vs. transformation angle.
- `Results/fea_structural_stress_results.csv`: Von Mises stress, beam deflections, and factor of safety along the limb.
- `Results/cfd_ground_effect_results.csv`: Induced prop-wash velocity and ground effect thrust ratio.
- `Results/multimodal_mission_telemetry.csv`: 45-second mission telemetry (power, speed, ZMP margin, morph angle).
- `Graphs/Fig1_cad_flight_and_walking_morphology.png`: Dimensioned CAD assembly drawings for both modes.
- `Graphs/Fig2_morphing_cog_and_inertia_migration.png`: CoG drop and rotational inertia reduction curves.
- `Graphs/Fig3_fea_structural_stress_and_deflection.png`: Von Mises stress distribution and factor of safety plots.
- `Graphs/Fig4_cfd_downwash_and_aerodynamic_interference.png`: CFD velocity contour map and ground effect thrust curve.
- `Graphs/Fig5_multimodal_mission_power_and_gait_stability.png`: Full mission electrical power trace and ZMP stability margin.
- `Manufacturing/BILL_OF_MATERIALS_AND_FABRICATION.md`: Complete BOM ($1,953.60), component sourcing, and CNC/SLS fabrication plan.
- `run_project2_all.py`: Multiphysics execution script running FEA, CFD, mission simulation, and figure generation.
- `Report/Project_2_Research_Paper.pdf`: Publication-formatted ~5-page research paper with embedded vector figures.
- `Report/Project_2_Research_Paper.docx`: Fully editable OpenXML Word manuscript.

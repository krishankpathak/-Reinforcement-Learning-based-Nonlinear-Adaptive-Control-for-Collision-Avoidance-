# Concept Development & Trade-off Selection: Project 2
**Generative Design, Multiphysics Modeling, and Aeromechanical Analysis of a Transformable Flying and Walking Inspection Robot**

---

## 1. Morphological Requirements & Mission Profile
The target robot must execute close-range non-destructive testing (NDT) and visual/ultrasonic inspection of structural steel trusses, storage tank welds, and elevated pipeline racks. The mission envelope mandates:
1. **Vertical Transit:** Rapid ascent up to $25\text{ m}$ elevation in aerial mode.
2. **Stable Landing & Perching:** Compliant touchdown on flat, inclined, or cylindrical grating.
3. **Morphological Reconfiguration:** Deterministic transition from high-aspect-ratio flight quadrotor to low-profile ground crawling quadruped in under $4.0\text{ seconds}$.
4. **Terrestrial Locomotion:** Omnidirectional, statically stable creeping or crawling gait negotiating $\pm 35\text{ mm}$ surface irregularities with zero propeller downwash (conserving power by $> 80\%$ compared to hover).
5. **Sensor Payload Delivery:** Rigid contact engagement of ultrasonic / eddy-current inspection probe against target surface.

---

## 2. Structural Architecture Concepts

```
        CONCEPT A                      CONCEPT B (Selected)                  CONCEPT C
   [Conventional Quadrotor]          [Dual-Use Rotor-Leg Arm]          [Folding Articulated Ring]
         +------------+                    +------------+                    +------------+
     O---|   Torso    |---O            O---|   Torso    |---O            O---|   Torso    |---O
         | (4 Rotors) |                    | (Reorient) |                    |  (Bi-fold) |
     O---|            |---O            O---|  (Rotors/  |---O            O---|            |---O
         +------------+                    |   Legs)    |                    +------------+
         /  |      |  \                    +------------+                    /            \
       [4 Dedicated Legs]               [Integrated Morphing]               [Compliant Wheels]
      (Heavy Parasitic Mass)            (Maximum Mass Sharing)            (Cannot Step Over Grating)
```

### Concept A: Conventional Quadrotor with Dedicated Deployable Legs
- **Kinematic Scheme:** Rigid carbon-fiber multirotor cross-frame with 4 independent 2-DOF robotic legs mounted beneath the belly.
- **Flight Actuation:** 4 Brushless DC (BLDC) motors with 9-inch propellers.
- **Ground Actuation:** 8 dedicated smart servo motors driving hip/knee linkages.
- **Actuator Count:** 12 total actuators.
- **Advantages:** Decoupled flight and walking control; standard quadrotor flight dynamics.
- **Disadvantages:** Severe parasitic deadweight; structural payload-to-mass ratio drops to $< 0.14$; aerodynamic drag in forward flight increased by $38\%$.

### Concept B: Dual-Purpose Articulated Rotor-Leg Morphology (SELECTED)
- **Kinematic Scheme:** 4 symmetrical articulated limbs connected to a central fuselage. Each limb serves as both a multirotor motor boom during flight and an active 2-DOF leg during ground locomotion.
- **Flight Actuation:** 4 BLDC motors mounted at the distal tips. In flight mode, arms lock into a planar horizontal configuration ($\theta_{\mathrm{morph}} = 0^\circ$).
- **Ground Actuation:** High-reduction cycloidal/harmonic drive actuators at the hip pitch and knee joints reorient the arms into vertical stances ($\theta_{\mathrm{morph}} = 65^\circ \text{ to } 85^\circ$), with the motor hubs acting as distal foot pivots equipped with high-friction silicone elastomer footpads.
- **Actuator Count:** 4 BLDC motors + 8 cycloidal servos = 12 actuators (every actuator contributes directly to both locomotion modes).
- **Advantages:** Zero parasitic leg mass; optimal structural mass sharing; compact stowed envelope; CoG shifts downward during terrestrial mode enhancing static tipping stability.
- **Disadvantages:** Complex multibody transformation dynamics; requires high-torque joint locks during flight to prevent vibration modal flutter.

### Concept C: Foldable Multirotor with Compliant Driven Wheels
- **Kinematic Scheme:** Quadrotor with outer carbon-fiber ring cages enclosing compliant driven wheels. A central servo folds the arms into an inline rolling configuration.
- **Flight Actuation:** 4 BLDC motors.
- **Ground Actuation:** 2 drive hub motors + 1 folding actuator = 7 actuators.
- **Advantages:** Lightweight; mechanically simple rolling motion.
- **Disadvantages:** Cannot navigate discrete obstacles, industrial grating, or vertical pipe steps; rolling motion induces continuous chassis vibration detrimental to ultrasonic sensor calibration.

---

## 3. Engineering Decision & Trade-off Matrix

Each parameter is weighted $w_i \in [1, 5]$ based on the inspection mission requirements:

| Evaluation Criteria | Weight ($w_i$) | Concept A (Parasitic Legs) | Concept B (Integrated Rotor-Leg) | Concept C (Rolling Wheels) |
| :--- | :---: | :---: | :---: | :---: |
| **Structural Mass Efficiency** | 5 | 2 (10) | **5 (25)** | 4 (20) |
| **Obstacle Traversability (Grating/Pipes)** | 5 | 4 (20) | **5 (25)** | 1 (5) |
| **Flight Aerodynamics & Endurance** | 4 | 2 (8) | **4 (16)** | 3 (12) |
| **Terrestrial Power Reduction vs. Hover** | 4 | 4 (16) | **5 (20)** | 5 (20) |
| **NDT Sensor Contact Stability** | 4 | 3 (12) | **5 (20)** | 2 (8) |
| **Mechanical Simplicity & Reliability** | 3 | 3 (9) | **3 (9)** | 4 (12) |
| **Dynamic Stability Margin** | 3 | 3 (9) | **4 (12)** | 3 (9) |
| **Total Weighted Score** | **28** | **84 / 140** | **127 / 140** | **86 / 140** |

**Selection Conclusion:** Concept B (Dual-Purpose Articulated Rotor-Leg Morphology) achieves the highest structural efficiency ($90.7\%$ score), eliminating non-functional deadweight by using the structural arms as functional walking limbs.

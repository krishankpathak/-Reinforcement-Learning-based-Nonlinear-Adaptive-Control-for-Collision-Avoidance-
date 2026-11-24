# Manufacturing Specification & Bill of Materials (BOM)
**Project 2: Transformable Flying and Walking Inspection Robot**

---

## 1. System Engineering Specifications
- **Total Flying Mass:** $2.45\text{ kg}$ (all-up weight including battery and NDT sensor payload).
- **Wingspan / Stowed Envelope:** Flight diagonal $560\text{ mm}$ (motor-to-motor); Stowed crawling footprint $320\text{ mm} \times 280\text{ mm} \times 165\text{ mm}$.
- **Structural Materials:** 7075-T6 Aerospace Aluminum (CNC milled brackets) + Toray T700 3K Twill Carbon Fiber composite tubes ($1.5\text{ mm}$ wall) + PA12 Nylon (Selective Laser Sintering - SLS for avionics pods).
- **Flight Endurance:** $18.5\text{ minutes}$ hover / cruise ($6S\text{ }4500\text{ mAh}$ LiPo).
- **Terrestrial Crawl Endurance:** $142\text{ minutes}$ continuous crawling at $0.12\text{ m/s}$ ($87.8\%$ power reduction vs. hover).
- **Inspection Payload:** Olympus 5MHz Dual-Element Ultrasonic Thickness Transducer + Micro-actuated spring gimbal ($220\text{ g}$).

---

## 2. Complete Bill of Materials (BOM)

| Category | Component Description | Manufacturer / Part No. | Qty | Unit Mass (g) | Total Mass (g) | Unit Cost (USD) | Total Cost (USD) | Sourcing / Specification Reference |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Flight Propulsion** | T-Motor F90 1300KV High-Efficiency BLDC | T-Motor F90-1300 | 4 | 46.5 | 186.0 | $34.90 | $139.60 | 9x4.5 inch Carbon Fiber Folding Props |
| **Propellers** | HQProp 9x4.5MR Carbon-Reinforced | HQ-9045-3K | 4 pairs | 12.0 | 48.0 | $8.50 | $34.00 | Balanced 2-blade high-lift profile |
| **Speed Controllers** | Hobbywing XRotor Pro 40A 6S Opto ESC | HW-XR-40A | 4 | 26.0 | 104.0 | $28.00 | $112.00 | DShot600, active freewheeling |
| **Morphing Servos** | Damiao DM-J4310-2EC Integrated Cycloidal Servo | Damiao J4310 | 4 | 142.0 | 568.0 | $95.00 | $380.00 | 7.0 N*m peak torque, CAN-bus, 17-bit magnetic encoder |
| **Knee Joint Servos** | KST X20-3012 High-Torque Titanium Micro-Servo | KST-X20-3012 | 4 | 72.0 | 288.0 | $68.00 | $272.00 | 3.5 N*m stall torque, 0.08s/60deg |
| **Avionics & Flight** | Holybro Pixhawk 6C + M10 GPS Module | HB-PX6C-M10 | 1 | 65.0 | 65.0 | $185.00 | $185.00 | STM32H753, triple redundant IMU, PX4 Autopilot |
| **Onboard Computer** | Raspberry Pi CM4 (4GB RAM, 32GB eMMC) + Carrier | RPi-CM4-4G32 | 1 | 42.0 | 42.0 | $75.00 | $75.00 | ROS 2 Humble middleware, mode state-machine |
| **Power Storage** | Tattu R-Line Version 5.0 6S 4500mAh 120C LiPo | TA-RL-6S-4500 | 1 | 610.0 | 610.0 | $115.00 | $115.00 | 22.2V nominal, XT90-S anti-spark connector |
| **Power Distribution** | Matek PDB-HEX 12S with 5V/12V Regulators | MT-PDB-HEX | 1 | 22.0 | 22.0 | $22.00 | $22.00 | Continuous 140A rating with current sensor |
| **Structural Frame** | CNC Milled 7075-T6 Aluminum Hip Yokes | Custom CNC Machined | 4 | 38.0 | 152.0 | $32.00 | $128.00 | High-stress transformation pivot knuckle |
| **Structural Booms** | 3K Matte Roll-Wrapped Carbon Fiber Square Tubes | DragonPlate 20x20 | 4 | 28.0 | 112.0 | $18.50 | $74.00 | $1.5\text{ mm}$ wall, 20mm outer profile |
| **Fuselage Enclosure**| SLS 3D Printed PA12 Nylon Weatherproof Shell | Custom Formlabs SLS | 1 | 94.0 | 94.0 | $45.00 | $45.00 | IP54 dust/water ingress protection |
| **Contact Footpads** | Molded Shore 60A Silicone Elastomer Foot Pivots | Custom Cast Silicone | 4 | 14.0 | 56.0 | $6.50 | $26.00 | High static coefficient ($\mu \ge 0.85$ on steel) |
| **NDT Sensor** | Olympus Dual-Element 5MHz NDT Transducer | Olympus DHC-706 | 1 | 95.0 | 95.0 | $340.00 | $340.00 | High-temperature structural steel thickness testing |
| **Fasteners & Bearings**| Titanium Grade 5 M3 Hex Hardware & EZO Bearings | EZO 688ZZ / Ti M3 | 1 set| 24.0 | 24.0 | $28.00 | $28.00 | Vibration-resistant nylon patch locking threads |
| **TOTALS** | | | | | **2,468 g** | | **$1,953.60** | Complete ready-to-fabricate assembly |

---

## 3. Fabrication & Assembly Sequence
1. **CNC Milling:** Machine hip knuckle brackets from solid 7075-T6 billet on a 4-axis VMC with tight dimensional tolerances ($\pm 0.02\text{ mm}$) for bearing press fits.
2. **Composite Boom Preparation:** Cut square carbon-fiber arms to length using diamond-coated abrasive wheels under water mist; ream pivot holes.
3. **Additive Manufacturing:** Print the main torso shell, battery cradle, and inspection probe gimbal housing on an industrial SLS PA12 system. Post-process with bead blasting and graphite black seal.
4. **Subassembly Integration:**
   - Press-fit dual 688ZZ flanged miniature bearings into hip knuckles.
   - Mount Damiao cycloidal servos into chassis corner bulkheads with Loctite 243 on M3 grade 10.9 fasteners.
   - Assemble femur and tibia linkages, routing silicone-insulated wiring through hollow internal channels.
5. **Electrical Integration:**
   - Solder ESC power leads directly to Matek PDB with heavy copper trace potting.
   - Wire CAN-bus transceiver bus linking Pixhawk 6C, Raspberry Pi CM4, and 4 cycloidal joint controllers.
6. **Calibration & Verification:**
   - Execute zero-point optical calibration of magnetic joint encoders.
   - Bench test static transformation torque hold under $12.0\text{ N}\cdot\text{m}$ proof load.

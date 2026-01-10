# Supersonic Mixed Compression Intake Sizing Tool (Python Script)

# Supersonic Intake Sizing Tool (Python Script)

### Description
This is an interactive Python tool designed for the **parametric sizing and performance analysis** of mixed-compression supersonic intakes. It simulates a 3-shock system (Oblique + Reflected + Normal) to optimize geometry for high-supersonic flight regimes.

Unlike static solvers, this tool includes **engineering logic checks** to ensure the selected design strategy is physically appropriate for the input Mach number.

### Key Features
* **Dynamic Simulation:** Solves theta-beta-M relations iteratively starting from the Mach wave angle to find exact shock solutions.
* **Smart Regime Detection:** * Rejects Subsonic inputs (M < 1.0).
  * **New:** Detects low-supersonic regimes (1.0 < M < 1.4) where mixed-compression is inefficient, advising the user to use a Pitot intake instead.
* **Automated Optimization:** Sweeps through ramp angles to find the maximum Pressure Recovery point before shock detachment.
* **Geometric Sizing:** Outputs the required **Ramp Length (L/H)** ratio to satisfy "Shock-on-Lip" conditions.

### How to Run
1. Install dependencies:
   ```bash
   pip install -r numpy, matplotlib

2- Run the script:
    python Supersonic_Intake_Design.py

3- Enter your desired Mach number when prompted.
    Example 1 (Valid): Input 2.2 → Generates plots and sizing data.
    Example 2 (Low Speed): Input 1.2 → Returns an engineering recommendation for a Normal Shock intake.

Technical Constraints & Physics
    Operating Range: Optimized for M > 1.4.
    Physics Model: 2D Planar Oblique Shock Theory (Ideal Gas, gamma=1.4).
    Failure Modes: Automatically detects and visualizes Shock Detachment limits for high ramp angles.

Author: Husam ASLAN

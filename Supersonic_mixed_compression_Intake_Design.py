
# Parametric Sizing of a Mixed-Compression Supersonic Intake
import numpy as np
import matplotlib.pyplot as plt
import sys

# --- 1. Constants ---
gamma = 1.4

print("--- Supersonic Intake Sizing Tool ---")

# Mach Number Input
try:
    user_input = input("Enter Flight Mach Number (e.g., 2.2): ")
    M_design = float(user_input)

    # Protection for Invalid Reynolds Number
    if M_design < 1.0:
        print("Error: Mach number must be Supersonic (>1.0).")
        sys.exit()
    elif M_design < 1.4:
        print("\n" + "="*50)
        print(f"  ENGINEERING NOTICE for Mach {M_design}")
        print("This 2-shock design (Mixed Compression) is inefficient for M < 1.4.")
        print("Recommendation: Use a simple Normal Shock (Pitot) intake instead.")
        print("The program will stop here to avoid unrealistic geometry.")
        print("="*50)
        sys.exit() 

    print(f"Running analysis for Mach {M_design}...")

except ValueError:
    print("Invalid input! Using default Mach 2.2")
    M_design = 2.2



# --- 2. Physics Functions ---
def get_shock_angle(Mach, theta_deg):
    theta = np.radians(theta_deg)

    # Find The Shock Angle (Weak Solution)
    for beta_deg in np.arange(1, 90, 0.01): 
        beta = np.radians(beta_deg)
        num = (Mach**2 * np.sin(beta)**2 - 1)
        den = (Mach**2 * (gamma + np.cos(2*beta)) + 2)
        tan_theta = 2 * (1 / np.tan(beta)) * (num / den)

        if np.arctan(tan_theta) >= theta:
            return beta_deg
    return None

def calc_shock_properties(M_up, beta_deg):
    beta = np.radians(beta_deg)
    Mn1 = M_up * np.sin(beta)

    # Check for subsonic normal component (physically impossible for shock)
    if Mn1 <= 1.0: return M_up, 1.0, 0

    # Normal Shock Relations
    Mn2_sq = (1 + 0.5 * (gamma - 1) * Mn1**2) / (gamma * Mn1**2 - 0.5 * (gamma - 1))

    term1 = ((gamma + 1) * Mn1**2 / (2 + (gamma - 1) * Mn1**2)) ** (gamma / (gamma - 1))
    term2 = ((gamma + 1) / (2 * gamma * Mn1**2 - (gamma - 1))) ** (1 / (gamma - 1))
    recov = term1 * term2

    # Calculate M_downstream
    # Re-calculate theta to be precise
    num = (M_up**2 * np.sin(beta)**2 - 1)
    den = (M_up**2 * (gamma + np.cos(2*beta)) + 2)
    tan_theta = 2 * (1/np.tan(beta)) * (num/den)
    theta = np.arctan(tan_theta)

    M_down = np.sqrt(Mn2_sq) / np.sin(beta - theta)
    return M_down, recov, np.degrees(theta)

print("Physics Engine Loaded Successfully.")

# --- 3. Parametric Study Loop ---
angles = np.arange(1, 50, 0.5)  # Try From 5 Degree to 20 Degree with 0.5 Degree Step
results_eta = []
results_theta = []
results_sizing = []

print("Running simulation...")

for theta in angles:
    # Stage 1: Ramp Shock
    beta1 = get_shock_angle(M_design, theta)
    if beta1 is None: continue
    M2, eta1, _ = calc_shock_properties(M_design, beta1)
    beta_rad = np.radians(beta1)
    L_over_H = 1 / np.tan(beta_rad)

    # Stage 2: Reflected Shock (Turning back by theta)
    beta2 = get_shock_angle(M2, theta)
    if beta2 is None: continue
    M3, eta2, _ = calc_shock_properties(M2, beta2)

    # Stage 3: Normal Shock
    M4, eta3, _ = calc_shock_properties(M3, 90)

    # Total Recovery
    total_recovery = eta1 * eta2 * eta3
    results_eta.append(total_recovery)
    results_theta.append(theta)
    results_sizing.append(L_over_H)


# --- 3. (Subplots) ---

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

# First Graph (Efficiency)
ax1.plot(results_theta, results_eta, 'b-', linewidth=3)
ax1.set_title('1. Performance: Pressure Recovery', fontsize=12)
ax1.set_xlabel('Ramp Angle (deg)')
ax1.set_ylabel('Total Recovery')
ax1.grid(True)

# Define the Peak Efficiency
max_val = (max(results_eta))
best_idx = results_eta.index(max_val)
best_theta = results_theta[best_idx]
best_sizing = results_sizing[best_idx]

ax1.plot(best_theta, max_val, 'ro')
ax1.text(best_theta, max_val-0.02, f' Peak: {max_val:.3f}', color='red')

# Second Graph (Sizing)
ax2.plot(results_theta, results_sizing, 'g-', linewidth=3)
ax2.set_title('2. Sizing: Ramp Geometry (L/H Ratio)', fontsize=12)
ax2.set_xlabel('Ramp Angle (deg)')
ax2.set_ylabel('Ramp Length / Inlet Height (L/H)')
ax2.grid(True)

# Define The Design Point
ax2.plot(best_theta, best_sizing, 'ro')
ax2.text(best_theta, best_sizing+0.1, f' L/H = {best_sizing:.2f}', color='red')

plt.tight_layout()
plt.show()

# --- 4. Final Resultsv---
print("-" * 40)
print(f"RESULTS FOR PORTFOLIO (Design Point):")
print(f"1. Optimal Ramp Angle: {best_theta:.1f} degrees")
print(f"2. Max Efficiency:     {max_val:.3f}")
print(f"3. INTAKE SIZING:      For every 1 meter of height,")
print(f"                       the ramp must be {best_sizing:.2f} meters long.")
print("-" * 40)



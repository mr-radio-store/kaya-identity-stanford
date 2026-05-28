import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Time settings
# -----------------------------
years = np.arange(2000, 2101)
np.random.seed(42)  # reproducible random noise

# -----------------------------
# Kaya Identity parameters
# -----------------------------
population = 6.1 + 0.01 * (years - 2000)          # billions
gdp_per_capita = 10 + 0.05 * (years - 2000)      # normalized trillion USD per billion people
energy_per_gdp = 1.0 - 0.002 * (years - 2000)    # energy per GDP
co2_per_energy = 1.0 - 0.003 * (years - 2000)    # CO2 per energy

# -----------------------------
# Initialize CO2 array
# -----------------------------
co2_emissions = np.zeros(len(years))

# -----------------------------
# Crisis definitions
# -----------------------------
pandemic_years = [2020, 2021, 2022]       # COVID-like
financial_crisis_years = [2008, 2029]    # past/future examples
energy_crisis_years = [1973, 2022]       # example energy shocks

# -----------------------------
# Simulation loop with noise & crises
# -----------------------------
for t, y in enumerate(years):
    # Random annual noise (uncertainty in population, GDP, efficiency)
    noise_pop = np.random.normal(0, 0.005)         # ~0.5% variation
    noise_gdp = np.random.normal(0, 0.01)          # ~1% variation
    noise_energy = np.random.normal(0, 0.005)
    noise_co2 = np.random.normal(0, 0.005)

    # Base Kaya emissions
    pop = population[t] * (1 + noise_pop)
    gdp = gdp_per_capita[t] * (1 + noise_gdp)
    energy = energy_per_gdp[t] * (1 + noise_energy)
    co2_int = co2_per_energy[t] * (1 + noise_co2)

    co2 = pop * gdp * energy * co2_int

    # Apply shocks
    # Pandemic: temporary drop (population mobility + industry drop)
    if y in pandemic_years:
        co2 *= 0.90  # 10% drop

    # Financial crisis: GDP & consumption drop
    if y in financial_crisis_years:
        co2 *= 0.92  # 8% drop

    # Energy/tech crisis: energy supply/CO2 intensity spike
    if y in energy_crisis_years:
        co2 *= 1.05  # 5% temporary increase

    co2_emissions[t] = co2

# -----------------------------
# Plot the results
# -----------------------------
plt.figure(figsize=(10, 6))
plt.plot(years, co2_emissions, label="CO₂ Emissions", color='red', linewidth=2)

plt.xlabel("Year")
plt.ylabel("CO₂ Emissions (arbitrary units)")
plt.title("Kaya Identity CO₂ Trend with Crises & Noise")
plt.grid(True)
plt.legend()

# Save as JPEG
plt.savefig("kaya_identity_emissions_crisis.jpg", dpi=200)
plt.close()

print("Saved: kaya_identity_emissions_crisis.jpg")

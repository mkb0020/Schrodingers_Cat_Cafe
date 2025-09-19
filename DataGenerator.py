import numpy as np
import pandas as pd

np.random.seed(42)
n = 100  # Number of rows

# Box Temperature (°C) / Generate 100 box temperatures with a normal distribution / Affects comfort and decay rate of quantum particles
box_temp = np.round(np.random.normal(loc=22, scale=5, size=n), 2)

# Photon Count per Minute / Poisson distribution for discrete quantum events / Measures quantum activity inside the box
photon_count = np.random.poisson(lam=300, size=n)

# Quantum Entanglement Index (0.0 to 1.0, skewed toward higher entanglement) / Degree of entanglement with external systems
entanglement_index = np.round(np.random.beta(a=2, b=1.5, size=n), 3)

# Observer Presence (0 = unobserved, 1 = observed)
observer_presence = np.random.choice([0, 1], size=n, p=[0.7, 0.3])  # Mostly unobserved

# Radioactive Decay Rate / Probability of poison release mechanism triggering / 0.0 to 1.0, higher means more likely to trigger poison
decay_rate = np.round(np.random.uniform(0.1, 0.9, size=n), 3)

# Wavefunction Stability / How stable the cat’s quantum state is / 0.0 to 1.0, higher = more stable
wavefunction_stability = np.round(np.random.normal(loc=0.6, scale=0.15, size=n), 3)
wavefunction_stability = np.clip(wavefunction_stability, 0, 1)

# Box Material (categorical) / Categorical: cardboard, lead, graphene, etc.
materials = ['Cardboard', 'Lead', 'Graphene', 'Velvet', 'Quantum Foam']
box_material = np.random.choice(materials, size=n)

# Assemble into DataFrame
df = pd.DataFrame({
    'Box Temperature (°C)': box_temp,
    'Photon Count per Minute': photon_count,
    'Quantum Entanglement Index': entanglement_index,
    'Observer Presence': observer_presence,
    'Radioactive Decay Rate': decay_rate,
    'Wavefunction Stability': wavefunction_stability,
    'Box Material': box_material
})

print(df.head())



















import pandas as pd
import matplotlib.pyplot as plt
import os

# File paths (replace with your actual paths if running locally)

FOLDER_PATH = r"C:\Github\Data Processing\data_folder\2025-04-30"
H2_PATH = "GENERATOR_h2_generation.xlsx"
O2_PATH = "PURIFIER_analyzer.xlsx"

h2_path = os.path.join(FOLDER_PATH, H2_PATH)
o2_path = os.path.join(FOLDER_PATH, O2_PATH)

# Load Excel files
h2_df = pd.read_excel(h2_path)
o2_df = pd.read_excel(o2_path)

# Convert time columns to datetime
h2_df['Time'] = pd.to_datetime(h2_df['Time'])
o2_df['Time'] = pd.to_datetime(o2_df['Time'])

# Resample and compute 5-minute mean values
h2_resampled = (
    h2_df.set_index('Time')
    .resample('5T')
    .mean()
    .reset_index()[['Time', '[PLC1]ACTUAL_FLOW']]
)

o2_resampled = (
    o2_df.set_index('Time')
    .resample('5T')
    .mean()
    .reset_index()[['Time', '[PLC1]ZQ_AI_AT1101']]
)


# Export selected columns only
h2_resampled.to_excel(
    os.path.join(FOLDER_PATH, "H2_generation_5min.xlsx"), index=False
)
o2_resampled.to_excel(
    os.path.join(FOLDER_PATH, "O2_PPM_5min.xlsx"), index=False
)

# Plot H2 Flow
plt.figure(figsize=(12, 5))
plt.plot(
    h2_resampled['Time'],
    h2_resampled['[PLC1]ACTUAL_FLOW'],
    label='H2 Flow (Nm^3/hr)'
)
plt.xlabel('Time')
plt.ylabel('Hydrogen (H2) Flow (Nm^3/hr)')
plt.title('Hydrogen Generation Over Time (Averaged every 5 minutes)')
plt.legend()
plt.grid(True)
plt.gca().xaxis.set_major_formatter(
    plt.matplotlib.dates.DateFormatter('%H:%M')
)
plt.tight_layout()
plt.show()

# Plot O2 ppm
plt.figure(figsize=(12, 5))
plt.plot(
    o2_resampled['Time'],
    o2_resampled['[PLC1]ZQ_AI_AT1101'],
    label='O2 ppm',
    color='orange'
)
plt.xlabel('Time')
plt.ylabel('Oxygen (O2) ppm')
plt.title('Oxygen ppm Level Over Time (Averaged every 5 minutes)')
plt.legend()
plt.grid(True)
plt.gca().xaxis.set_major_formatter(
    plt.matplotlib.dates.DateFormatter('%H:%M')
)
plt.tight_layout()
plt.show()


# Constants
H2_DENSITY = 0.083  # kg/Nm3 at 20°C, 1 atm

# Convert H2 flow from Nm³/hr to kg/hr by multiplying by density
h2_resampled['H2_kg_per_hr'] = h2_resampled['[PLC1]ACTUAL_FLOW'] * H2_DENSITY

# Plot H2 Flow in kg/hr
plt.figure(figsize=(12, 5))
plt.plot(
    h2_resampled['Time'],
    h2_resampled['H2_kg_per_hr'],
    label='H2 Flow (kg/hr)',
    color='green'
)
plt.xlabel('Time')
plt.ylabel('H2 Flow (kg/hr)')
plt.title('Hydrogen Generation Over Time (Averaged 5 minutes, kg/hr)')
plt.legend()
plt.grid(True)
plt.gca().xaxis.set_major_formatter(
    plt.matplotlib.dates.DateFormatter('%H:%M')
)
plt.tight_layout()
plt.show()

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
import config
'''
# === Load and combine H2 data ===
h2_dfs = [
    pd.read_excel(os.path.join(config.FOLDER_29, config.H2_FILENAME)),
    pd.read_excel(os.path.join(config.FOLDER_30, config.H2_FILENAME)),
]
h2_df = pd.concat(h2_dfs, ignore_index=True)

# === Load and combine O2 data ===
o2_dfs = [
    pd.read_excel(os.path.join(config.FOLDER_29, config.O2_FILENAME)),
    pd.read_excel(os.path.join(config.FOLDER_30, config.O2_FILENAME)),
]
o2_df = pd.concat(o2_dfs, ignore_index=True)
'''

h2_df = pd.read_excel(os.path.join(config.FOLDER_29, config.H2_FILENAME))
o2_df = pd.read_excel(os.path.join(config.FOLDER_29, config.O2_FILENAME))

# === Convert time columns ===
h2_df['Time'] = pd.to_datetime(h2_df['Time'])
o2_df['Time'] = pd.to_datetime(o2_df['Time'])

# === Resample to 5-minute mean ===
h2_resampled = (
    h2_df.set_index('Time')
    .resample('5T')
    .mean()
    .reset_index()[['Time', '[PLC1]ACTUAL_FLOW']]
    .rename(columns={'[PLC1]ACTUAL_FLOW': 'H2 Generation (Nm^3/hr)'})
)

# Convert to kg/hr (Nm³ * 0.083 kg/Nm^3)
h2_resampled['H2 Generation (kg/hr)'] = (
    h2_resampled['H2 Generation (Nm^3/hr)']
    * config.H2_DENSITY
)

o2_resampled = (
    o2_df.set_index('Time')
    .resample('5T')
    .mean()
    .reset_index()[['Time', '[PLC1]ZQ_AI_AT1101']]
    .rename(columns={'[PLC1]ZQ_AI_AT1101': 'O2 Concentration (ppm)'})
)

# Split 'Time' into separate 'Date' and 'Time' columns
# Keep full 'Time' for plotting, and prepare separate version for export
h2_export = h2_resampled.copy()
h2_export['Date'] = h2_export['Time'].dt.date.astype(str)
h2_export['Time'] = h2_export['Time'].dt.time.astype(str)
h2_export = h2_export[
    ['Date', 'Time',
     'H2 Generation (Nm^3/hr)',
     'H2 Generation (kg/hr)'
     ]
]

o2_export = o2_resampled.copy()
o2_export['Date'] = o2_export['Time'].dt.date.astype(str)
o2_export['Time'] = o2_export['Time'].dt.time.astype(str)
o2_export = o2_export[['Date', 'Time', 'O2 Concentration (ppm)']]


# === Output folder ===
OUTPUT_FOLDER = os.path.join(config.FOLDER_29, "output")
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# === Save cleaned Excel files ===
H2_OUTPUT = os.path.join(OUTPUT_FOLDER, "H2_generation_5min_combined.xlsx")
O2_OUTPUT = os.path.join(OUTPUT_FOLDER, "O2_PPM_5min_combined.xlsx")

# Save export-friendly version
h2_export.to_excel(H2_OUTPUT, index=False)
o2_export.to_excel(O2_OUTPUT, index=False)

'''
# === Plot 1: H2 Nm³/hr ===
plt.figure(figsize=(12, 5))
plt.plot(
    h2_resampled['Time'],
    h2_resampled['H2 Generation (Nm^3/hr)'],
    label='H₂ Flow (Nm³/hr)',
    color='blue'
)
plt.xlabel('Time')
plt.ylabel('Nm^3/hr')
plt.title('Hydrogen Generation: 5-Minute Average (Nm^3/hr)')
plt.legend()
plt.grid(True)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# === Plot 2: H2 kg/hr ===
plt.figure(figsize=(12, 5))
plt.plot(
    h2_resampled['Time'],
    h2_resampled['H2 Generation (kg/hr)'],
    label='H2 Flow (kg/hr)',
    color='green'
)
plt.xlabel('Time')
plt.ylabel('kg/hr')
plt.title('Hydrogen Generation: 5-Minute Average (kg/hr)')
plt.legend()
plt.grid(True)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# === Plot 3: O2 ppm ===
plt.figure(figsize=(12, 5))
plt.plot(
    o2_resampled['Time'],
    o2_resampled['O2 Concentration (ppm)'],
    label='O₂ Concentration (ppm)',
    color='orange'
)
plt.xlabel('Time')
plt.ylabel('ppm')
plt.title('Trace Oxygen Level – 5-Minute Average (ppm)')
plt.legend()
plt.grid(True)
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d %H:%M'))
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
'''
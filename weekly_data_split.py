import pandas as pd
import os

# Path to the input Excel file
input_file = 'C:/github/Data-Processing/Data_input/data/PURIFIER_valve_opening.xlsx'
base_filename = os.path.splitext(os.path.basename(input_file))[0]

# Load the original Excel file to capture exact formatting
original_data = pd.read_excel(input_file, sheet_name=None)
# Extract the first sheet name (assuming single sheet)
sheet_name = list(original_data.keys())[0]
df = original_data[sheet_name]

# Convert the 'Time' column to datetime if needed
df['Time'] = pd.to_datetime(df['Time'])

# Define the date ranges for splitting
date_ranges = {
    "April_29_30": (df['Time'].dt.month == 4) & (df['Time'].dt.day >= 29),
    "May_1_2": (df['Time'].dt.month == 5) & (df['Time'].dt.day <= 2),
    "May_3_4": (df['Time'].dt.month == 5) & (df['Time'].dt.day >= 3) & (df['Time'].dt.day <= 4),
    "May_5_6": (df['Time'].dt.month == 5) & (df['Time'].dt.day >= 5) & (df['Time'].dt.day <= 6),
}

# Output directory
output_folder = 'C:/github/Data-Processing/Data_input'  # Use current directory or specify another path

# Split and save each group
for date_label, condition in date_ranges.items():
    split_data = df[condition]
    output_filename = f"{base_filename}_{date_label}.xlsx"
    split_data.to_excel(os.path.join(output_folder, output_filename), sheet_name=sheet_name, index=False)

print("Files have been generated successfully.")

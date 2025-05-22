import pandas as pd
import os

# Set the base folder path and current folder name
folder_path = 'C:/github/Data_Folder/Data_input/'
folder_name = '2025-05-22/'

date_ranges = {
    "May_17_18": lambda dt: (dt.dt.month == 5) & (dt.dt.day >= 17) & (dt.dt.day <= 18),
    "May_19_20": lambda dt: (dt.dt.month == 5) & (dt.dt.day >= 19) & (dt.dt.day <= 20),
}

# Construct the full input and output paths
input_folder = os.path.join(folder_path, folder_name)
output_folder = folder_path

# Get all Excel files in the directory
excel_files = [f for f in os.listdir(input_folder) if f.endswith('.xlsx')]

# Process each Excel file
for filename in excel_files:
    input_file = os.path.join(input_folder, filename)
    base_filename = os.path.splitext(filename)[0]

    # Load the original Excel file to capture exact formatting
    original_data = pd.read_excel(input_file, sheet_name=None)

    # Process each sheet in the Excel file
    for sheet_name, df in original_data.items():
        # Convert the 'Time' column to datetime if needed
        if 'Time' in df.columns:
            try:
                df['Time'] = pd.to_datetime(df['Time'], errors='coerce')
                if df['Time'].isna().all():
                    print(f"Warning: All values in the 'Time' column for file '{filename}' (sheet '{sheet_name}') could not be converted to datetime. Skipping...")
                    continue
            except Exception as e:
                print(f"Error converting 'Time' column in file '{filename}' (sheet '{sheet_name}'): {e}")
                continue
            # Split and save each group
            for date_label, condition_fn in date_ranges.items():
                split_data = df[condition_fn(df['Time'])]
                if not split_data.empty:  # Only save if there is data
                    output_filename = f"{base_filename}_{date_label}.xlsx"
                    split_data.to_excel(os.path.join(output_folder, output_filename), sheet_name=sheet_name, index=False)

print("\nFiles have been generated successfully.")
import h5py
import pandas as pd

# Path to the GEDI Level 2A HDF5 file
file_path = 'GEDI02_A_2023075201011_O24115_03_T08796_02_003_02_V002.h5'

# Lists to store canopy height and coordinate data
canopy_heights = []
latitudes = []
longitudes = []

with h5py.File(file_path, 'r') as f:
    # Loop through each beam (e.g., BEAM1000, BEAM1011, etc.)
    for beam in ['BEAM1000', 'BEAM1011']:  # Add more beam names as needed
        if beam in f:
            # Extract canopy height (rh) and coordinates
            rh = f[f'{beam}/rh'][:]  # Adjust if there’s a specific RH metric like rh100
            lat = f[f'{beam}/lat_lowestmode'][:]
            lon = f[f'{beam}/lon_lowestmode'][:]
            
            # Append data to lists
            canopy_heights.extend(rh)
            latitudes.extend(lat)
            longitudes.extend(lon)

# Create a DataFrame from the extracted data
df = pd.DataFrame({
    'Latitude': latitudes,
    'Longitude': longitudes,
    'Canopy Height (RH)': canopy_heights
})

# Save the DataFrame to a CSV file
csv_output_path = 'gedi_canopy_height.csv'
df.to_csv(csv_output_path, index=False)

print(f"Data successfully saved to {csv_output_path}")

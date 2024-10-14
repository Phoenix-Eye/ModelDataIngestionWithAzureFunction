import requests
import csv
import os

# Output folder
output_folder = "modis_csv_data"
os.makedirs(output_folder, exist_ok=True)

# URL of the CSV file
csv_url = "https://firms.modaps.eosdis.nasa.gov/data/active_fire/noaa-21-viirs-c2/csv/J2_VIIRS_C2_Global_24h.csv"

# Output CSV file path
csv_file_path = os.path.join(output_folder, "viirs_active_fires.csv")

# Fetch the CSV file
response = requests.get(csv_url)
response.raise_for_status()
csv_content = response.content.decode('utf-8')

# Read the CSV content
csv_reader = csv.DictReader(csv_content.splitlines())

# Open the output CSV file and write the header
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    fieldnames = csv_reader.fieldnames  # Get the header from the source CSV
    csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
    csv_writer.writeheader()

    # Process and write each row
    for row in csv_reader:
        # We can add data processing ove here
        # Filter out rows with low confidence, which means the fire detection is not very reliable
        if row.get('confidence', '').lower() not in ['low']:
            csv_writer.writerow(row)

print(f"Data extracted and saved to {csv_file_path}")
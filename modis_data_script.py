import requests
import csv
import os
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup

# Output folder
output_folder = "modis_csv_data"
os.makedirs(output_folder, exist_ok=True)

# URL of the KML file
kml_url = "https://firms.modaps.eosdis.nasa.gov/data/active_fire/noaa-21-viirs-c2/kml/J2_VIIRS_C2_Europe_animated_48h.kml"

# Output CSV file path
csv_file_path = os.path.join(output_folder, "viirs_active_fires.csv")

# Fetch the KML file
response = requests.get(kml_url)
response.raise_for_status()
kml_content = response.content

# Parse the KML file
root = ET.fromstring(kml_content)

# KML uses the namespace 'http://www.opengis.net/kml/2.2'
namespaces = {'kml': 'http://www.opengis.net/kml/2.2'}

# Find all Placemark elements
placemarks = root.findall('.//kml:Placemark', namespaces)

# Open the CSV file
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write header row
    writer.writerow([
        "Latitude", "Longitude", "Brightness", "Scan", "Track", "Acq_Date",
        "Acq_Time", "Satellite", "Confidence", "Version", "Bright_T31",
        "FRP", "DayNight"
    ])
    
    # Iterate over each Placemark
    for placemark in placemarks:
        # Get the description element
        description = placemark.find('kml:description', namespaces)
        # Get the coordinates
        coordinates = placemark.find('.//kml:coordinates', namespaces)
        
        # Extract coordinates
        coord_text = coordinates.text.strip()
        coords = coord_text.split(',')
        
        # Handle cases where altitude might not be present
        if len(coords) >= 2:
            lon = coords[0]
            lat = coords[1]
        else:
            print(f"Unexpected coordinate format: {coord_text}")
            continue  # Skip this placemark if coordinates are not as expected
        
        # The description contains HTML content
        # Parse it using BeautifulSoup
        description_text = description.text.strip()
        soup = BeautifulSoup(description_text, 'html.parser')
        
        # The data is in <td> elements
        td_elements = soup.find_all('td')
        data = {}
        for i in range(0, len(td_elements), 2):
            key = td_elements[i].get_text(strip=True)
            value = td_elements[i+1].get_text(strip=True)
            data[key] = value
        
        # Now, extract the fields we need
        row = [
            lat,  # Latitude
            lon,  # Longitude
            data.get('Brightness', ''),
            data.get('Scan', ''),
            data.get('Track', ''),
            data.get('Acq Date', ''),
            data.get('Acq Time', ''),
            data.get('Satellite', ''),
            data.get('Confidence', ''),
            data.get('Version', ''),
            data.get('Bright T31', ''),
            data.get('FRP', ''),
            data.get('DayNight', ''),
        ]
        
        writer.writerow(row)

print(f"Data extracted and saved to {csv_file_path}")
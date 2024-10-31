import requests
import csv
import os

# Output folder
output_folder = "modis_csv_data"
os.makedirs(output_folder, exist_ok=True)

# URL of the CSV file containing fire data
csv_url = "https://firms.modaps.eosdis.nasa.gov/data/active_fire/noaa-21-viirs-c2/csv/J2_VIIRS_C2_Global_24h.csv"

# Output CSV file path for combined fire and weather data
csv_file_path = os.path.join(output_folder, "fires_with_weather_limited.csv")

# WeatherAPI key (replace with your actual API key)
api_key = "your_weatherapi_key"

# Fallback location (used if weather data for fire location is not available)
fallback_location = {"lat": 50.8503, "lon": 4.3517}  # Brussels

# Fetch the fire data CSV file
response = requests.get(csv_url)
response.raise_for_status()
csv_content = response.content.decode('utf-8')

# Read the fire data CSV content
csv_reader = csv.DictReader(csv_content.splitlines())

# Define the fields for the output CSV (fire data + weather data)
fire_fieldnames = csv_reader.fieldnames  # Existing fire data fields
weather_fieldnames = ["last_updated", "temp_c", "humidity", "wind_kph", "weather_description"]  # Weather fields
fieldnames = fire_fieldnames + weather_fieldnames

# Open the output CSV file and write the header
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
    csv_writer.writeheader()

    # Limit the number of rows to fetch (for testing purposes)
    max_rows = 5  # Fetch a small portion of data

    # Process each fire event row
    for idx, row in enumerate(csv_reader):
        if idx >= max_rows:
            break  # Limit the processing to max_rows rows

        # Filter out rows with low confidence
        if row.get('confidence', '').lower() not in ['low']:
            lat = row.get('latitude')
            lon = row.get('longitude')

            # Fetch weather data for the fire location
            api_url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={lat},{lon}"
            weather_response = requests.get(api_url)

            if weather_response.status_code == 200:
                weather_data = weather_response.json().get('current', {})
            else:
                # If weather data is unavailable for the fire location, use fallback
                print(f"Fetching weather data for fallback location due to error at {lat}, {lon}")
                fallback_lat = fallback_location["lat"]
                fallback_lon = fallback_location["lon"]
                api_url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={fallback_lat},{fallback_lon}"
                weather_response = requests.get(api_url)
                weather_data = weather_response.json().get('current', {})

            # Extract relevant weather data
            last_updated = weather_data.get('last_updated')
            temp_c = weather_data.get('temp_c')
            humidity = weather_data.get('humidity')
            wind_kph = weather_data.get('wind_kph')
            weather_description = weather_data.get('condition', {}).get('text')

            # Add the weather data to the current fire row
            row.update({
                "last_updated": last_updated,
                "temp_c": temp_c,
                "humidity": humidity,
                "wind_kph": wind_kph,
                "weather_description": weather_description
            })

            # Write the combined fire and weather data to the output CSV
            csv_writer.writerow(row)

print(f"Data extracted and saved to {csv_file_path}")
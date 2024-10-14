import requests
import csv
import os

# Output folder for weather data
output_folder = "weatherapi_csv_data"
os.makedirs(output_folder, exist_ok=True)

# WeatherAPI key
api_key = "4f51d68de081447585610926241410"  # Replace with your actual WeatherAPI key

# List of coordinates for locations (you can replace this with actual data from your fire zones)
locations = [
    {"lat": 37.7749, "lon": -122.4194},  # Example: San Francisco
    {"lat": 34.0522, "lon": -118.2437},  # Example: Los Angeles
    # Add more coordinates as needed
]

# Output CSV file path
csv_file_path = os.path.join(output_folder, "weatherapi_data.csv")

# Define the fields you want to extract from the API response
fieldnames = ["lat", "lon", "temperature_c", "humidity", "wind_kph", "weather_description"]

# Open the output CSV file and write the header
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
    csv_writer.writeheader()

    # Process each location
    for location in locations:
        lat = location["lat"]
        lon = location["lon"]

        # Make the API request to WeatherAPI
        api_url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={lat},{lon}"
        response = requests.get(api_url)
        response.raise_for_status()
        
        # Parse the JSON response
        weather_data = response.json()

        # Extract relevant data from the response
        current_weather = weather_data.get('current', {})
        temperature_c = current_weather.get('temp_c')
        humidity = current_weather.get('humidity')
        wind_kph = current_weather.get('wind_kph')
        weather_description = current_weather.get('condition', {}).get('text')

        # Write the data to the CSV file
        csv_writer.writerow({
            "lat": lat,
            "lon": lon,
            "temperature_c": temperature_c,
            "humidity": humidity,
            "wind_kph": wind_kph,
            "weather_description": weather_description
        })

print(f"Weather data extracted and saved to {csv_file_path}")
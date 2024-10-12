import json
from datetime import datetime

CURR_DATE = "10-12-2024"
MAX_NUM_VEHICLES = 0
MAX_DAYS_WITHOUT_MAINTENANCE = 0

def time_since_last_maintenance(maintenance_date: str):
    date_format = "%m-%d-%Y"
    last_maintenance = datetime.strptime(maintenance_date, date_format)
    current_date = datetime.strptime(CURR_DATE, date_format)
    delta = current_date - last_maintenance
    return delta.days

with open("input.json", "r") as input_json:
    results = json.load(input_json)

    for key, value in results.items():
        MAX_NUM_VEHICLES = max(MAX_NUM_VEHICLES, value["num_vehicles_past_year"])
        
        days_since_maintenance = time_since_last_maintenance(value["last_maintenance_date"])
        MAX_DAYS_WITHOUT_MAINTENANCE = max(MAX_DAYS_WITHOUT_MAINTENANCE, days_since_maintenance)

def calculate_total_score(intersection_data):
    # Weights for weather, traffic, and maintenance time
    w1 = w2 = w3 = 1/3
    
    # Extract values
    weather_score = intersection_data["total_weather_score"]
    num_vehicles = intersection_data["num_vehicles_past_year"]
    last_maintenance = intersection_data["last_maintenance_date"]
    
    # Normalize weather score (0 to 1)
    normalized_weather = weather_score / 100
    
    # Normalize traffic factor (0 to 1)
    normalized_traffic = min(num_vehicles / MAX_NUM_VEHICLES, 1)
    
    # Normalize time since last maintenance (0 to 1)
    days_since_maintenance = time_since_last_maintenance(last_maintenance)
    normalized_maintenance = min(days_since_maintenance / MAX_DAYS_WITHOUT_MAINTENANCE, 1)
    
    # Calculate the total score
    total_score = (w1 * normalized_weather + 
                   w2 * (1 - normalized_traffic) + 
                   w3 * (1 - normalized_maintenance)) * 100
    return total_score

for key, value in results.items():
    value["total_score"] = round(calculate_total_score(value), 4)

with open("results.json", "w") as result_json:
    result_json.write(json.dumps(results, indent=4))

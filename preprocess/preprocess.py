import json
from datetime import datetime
from weather.weather import weather_score

CURR_DATE = "10-13-2024"
MAX_VEHICLE_WEIGHT = 0

INPUT_JSON = "input.json"
OUTPUT_JSON = "results.json"

def time_since_last_maintenance(maintenance_date: str):
    date_format = "%m-%d-%Y"
    last_maintenance = datetime.strptime(maintenance_date, date_format)
    current_date = datetime.strptime(CURR_DATE, date_format)
    delta = current_date - last_maintenance
    return delta.days

def time_to_next_maintenance(data):
    # get mean of vehicle score and weather score
    # get the total score and maitenece date for this name in json
    total_score = data['total_score']
    maintenance_date = data['last_maintenance_date']
    # get the slop of the line based of days from last maintence date till now and 100 - total score
    days_since_maintenance = time_since_last_maintenance(maintenance_date)
    slope = ((total_score - 100 ) / days_since_maintenance) / 1.75
    # get the days to next maintenance
    return (total_score - 100) / slope


def calculate_vehicle_score(data):
    if (data["num_cars_last_maintenance"] + data["num_trucks_last_maintenance"] != data["num_vehicles_last_maintenance"]):
        print("ERROR. Cars + Trucks doesn't add up")

    vehicle_weight = data["num_cars_last_maintenance"] + (5 * data["num_trucks_last_maintenance"])
    normalized_traffic = min(vehicle_weight / MAX_VEHICLE_WEIGHT, 1)
    return normalized_traffic * 100

def calculate_total_score(data):
    vehicle_score = data["vehicle_score_last_maintenance"]
    weather_score = data["weather_score_last_maintenance"]
    return (vehicle_score + weather_score) / 2


with open(INPUT_JSON, "r") as input_json:
    results = json.load(input_json)

    for key, value in results.items():
        # count 1 truck as 5 cars
        MAX_VEHICLE_WEIGHT = max(
            MAX_VEHICLE_WEIGHT, 
            value["num_cars_last_maintenance"] + (5 * value["num_trucks_last_maintenance"])
        )
        
        days_since_maintenance = time_since_last_maintenance(value["last_maintenance_date"])


for key, value in results.items():
    final_score, penalty_counts, total_penalty = weather_score(value["city"], value["last_maintenance_date"])

    value["weather_score_last_maintenance"] = round(final_score, 4)
    value["weather_penalties"] = {
        "rain": [penalty_counts['rain_penalty'][0], round(penalty_counts['rain_penalty'][1], 4)],
        "snow": [penalty_counts['snow_penalty'][0], round(penalty_counts['snow_penalty'][1], 4)],
        "freezing_rain": [penalty_counts['freezing_rain_penalty'][0], round(penalty_counts['freezing_rain_penalty'][1], 4)],
        "cold_temp": [penalty_counts['cold_weather_penalty'][0], round(penalty_counts['cold_weather_penalty'][1], 4)],
        "hot_temp": [penalty_counts['hot_weather_penalty'][0], round(penalty_counts['hot_weather_penalty'][1], 4)],
        "total_penalty": round(total_penalty, 4)
    }


for key, value in results.items():
    value["vehicle_score_last_maintenance"] = round(calculate_vehicle_score(value), 4)
    value["total_score"] = round(calculate_total_score(value), 4)
    value["days_to_next_maintenance"] = time_to_next_maintenance(value)


with open(OUTPUT_JSON, "w") as result_json:
    result_json.write(json.dumps(results, indent=4))

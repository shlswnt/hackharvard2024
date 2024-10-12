import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

# define a function that takes in a city in the form of at, lv or ny as well as a date
# return the tuples of the penalties and the weather score

def calculate_weather_score(df):
    total_score = 100  # Start with a perfect score
    penalty_counts = {
        'rain_penalty': (0, 0),  # (count, total_penalty)
        'snow_penalty': (0, 0),
        'freezing_rain_penalty': (0, 0),
        'cold_weather_penalty': (0, 0),
        'hot_weather_penalty': (0, 0)
    }

    total_penalty = 0

    for index, row in df.iterrows():
        # Deduct points based on rain and snow
        rain_score_penalty = row['rain_sum (mm)'] * 0.009  # Adjust as needed
        snow_score_penalty = row['snowfall_sum (cm)'] * 0.1  # Adjust as needed

        # Track penalties for rain
        if rain_score_penalty > 0:
            current_rain_count, current_rain_penalty = penalty_counts['rain_penalty']
            penalty_counts['rain_penalty'] = (current_rain_count + 1, current_rain_penalty + rain_score_penalty)

        # Track penalties for snow
        if snow_score_penalty > 0:
            current_snow_count, current_snow_penalty = penalty_counts['snow_penalty']
            penalty_counts['snow_penalty'] = (current_snow_count + 1, current_snow_penalty + snow_score_penalty)

        total_penalty += (rain_score_penalty + snow_score_penalty)

        # Check for freezing rain
        if row['rain_sum (mm)'] > 0:
            if row['temperature_2m_min (°C)'] < 0 or (index + 1 < len(df) and df.iloc[index + 1]['temperature_2m_min (°C)'] < 0):
                current_freezing_rain_count, current_freezing_rain_penalty = penalty_counts['freezing_rain_penalty']
                penalty_counts['freezing_rain_penalty'] = (current_freezing_rain_count + 1, current_freezing_rain_penalty + 1)
                total_penalty += 1  # Heavy penalty for freezing rain

        # Scale penalty for hot weather
        hot_weather_penalty = max(0, row['temperature_2m_max (°C)'] - 38) * 0.0125
        total_penalty += hot_weather_penalty
        if hot_weather_penalty > 0:
            current_hot_weather_count, current_hot_weather_penalty = penalty_counts['hot_weather_penalty']
            penalty_counts['hot_weather_penalty'] = (current_hot_weather_count + 1, current_hot_weather_penalty + hot_weather_penalty)

        # Scale penalty for colder weather
        cold_weather_penalty = max(0, -row['temperature_2m_min (°C)']) * 0.0125  # Adjust scaling factor as needed
        total_penalty += cold_weather_penalty
        if cold_weather_penalty > 0:
            current_cold_weather_count, current_cold_weather_penalty = penalty_counts['cold_weather_penalty']
            penalty_counts['cold_weather_penalty'] = (current_cold_weather_count + 1, current_cold_weather_penalty + cold_weather_penalty)

    final_score = total_score - total_penalty
    return final_score, penalty_counts, total_penalty

def weather_score(city, date):
    date = pd.to_datetime(date)
    df = pd.read_csv(f'{city}2224.csv', parse_dates=['time'], skiprows=2)

    # Ensure that 'time' column is in datetime format
    df['time'] = pd.to_datetime(df['time'])

    # Fill NaN values for rainfall and snowfall
    df['rain_sum (mm)'] = df['rain_sum (mm)'].fillna(0)
    df['snowfall_sum (cm)'] = df['snowfall_sum (cm)'].fillna(0)

    # cut the df to be only greater than the date
    df = df[df['time'] >= date]
    return calculate_weather_score(df)

print(weather_score('ny', '2023-03-20'))
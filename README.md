# Traffix: HackHarvard 2024

## Installation
- Create a new virtual environment with: `python3 -m venv env`
- Activate your virtual environment with: `source env/bin/activate`
- Install necessary dependencies: `pip install -r requirements.txt`

## Running FastAPI
- Enter the following commands in the terminal:
    - `cd api`
    - `source env/bin/activate`
    - `uvicorn main:app --reload`
- Navigate to `localhost:8000` on your browser

## Get Video Frames
- `localhost:8000/video/?video_url={URL_HERE}.m3u8`

## Get Traffic Intersection Data
- `localhost:8000/intersection/?intersection_name={NAME_HERE}`
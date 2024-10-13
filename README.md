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

## Get All Intersection Names
- `localhost:8000/get_all_names/`

## Get Video Frames
- `localhost:8000/video/?name=NAME_HERE`

## Get All Intersection Data
- `localhost:8000/intersection/?name=NAME_HERE`
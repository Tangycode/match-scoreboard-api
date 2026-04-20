from fastapi import FastAPI, HTTPException
from scoreboard_services import generate_match_scoreboard

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Match Scoreboard API is running"}

@app.post("/match/scoreboard")
def match_scoreboard(payload: dict):
    match_id = payload.get("match_id")
    innings_data = payload.get("innings_data")

    if not match_id:
        raise HTTPException(status_code=400, detail="match_id is required")

    if innings_data is not None and not isinstance(innings_data, list):
        raise HTTPException(status_code=400, detail="innings_data must be a list")

    scoreboard = generate_match_scoreboard(match_id, innings_data)
    return scoreboard

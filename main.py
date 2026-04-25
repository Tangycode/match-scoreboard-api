from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import MatchInput
from services import ScoreboardService

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"service": "Khel AI Scoreboard API", "status": "running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/match/scoreboard")
def scoreboard(payload: MatchInput):

    if not payload.match_id:
        raise HTTPException(status_code=400, detail="missing match_id")

    if not payload.innings:
        return ScoreboardService.no_data(payload.match_id)

    return ScoreboardService.compute(payload)

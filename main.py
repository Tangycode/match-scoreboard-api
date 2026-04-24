from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import MatchSchema
from services import ScoreboardService

app = FastAPI()

# CORS (MANDATORY)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ROOT
@app.get("/")
def root():
    return {
        "service": "Khel AI Scoreboard API",
        "status": "running"
    }

# HEALTH CHECK
@app.get("/health")
def health():
    return {"status": "ok"}

# MAIN ENDPOINT
@app.post("/scoreboard")
def scoreboard(payload: MatchSchema):

    # VALIDATION RULES (STRICT 400 ERRORS)
    if not payload.match or not payload.match.match_id:
        raise HTTPException(status_code=400, detail="missing match_id")

    if not payload.ball_events:
        raise HTTPException(status_code=400, detail="ball_events cannot be empty")

    if not payload.innings:
        raise HTTPException(status_code=400, detail="empty innings")

    return ScoreboardService.compute(payload)

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import MatchInput
from services import ScoreboardService

app = FastAPI()

# -----------------------------
# CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# ROOT
# -----------------------------
@app.get("/")
def root():
    return {
        "service": "Khel AI Scoreboard API",
        "version": "v1",
        "status": "running"
    }

# -----------------------------
# HEALTH
# -----------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

# -----------------------------
# MAIN ENDPOINT
# -----------------------------
@app.post("/match/scoreboard")
def scoreboard(payload: MatchInput):

    # -------------------------
    # MATCH VALIDATION
    # -------------------------
    if not payload.match_id:
        raise HTTPException(status_code=400, detail="missing match_id")

    if payload.innings is None or len(payload.innings) == 0:
        return ScoreboardService.no_data(payload.match_id)

    seen_innings_numbers = set()

    # -------------------------
    # INNINGS VALIDATION
    # -------------------------
    for inn in payload.innings:

        if inn.innings_number is None:
            raise HTTPException(status_code=400, detail="missing innings_number")

        if inn.innings_number in seen_innings_numbers:
            raise HTTPException(status_code=400, detail="duplicate innings_number")

        seen_innings_numbers.add(inn.innings_number)

        if not inn.batting_team or not inn.bowling_team:
            raise HTTPException(status_code=400, detail="missing team information")

        if inn.ball_events is None:
            raise HTTPException(status_code=400, detail="ball_events missing")

        if len(inn.ball_events) == 0:
            raise HTTPException(
                status_code=400,
                detail=f"empty ball_events for innings {inn.innings_number}"
            )

        # -------------------------
        # BALL EVENT VALIDATION
        # -------------------------
        for e in inn.ball_events:

            if e.over < 0:
                raise HTTPException(status_code=400, detail="invalid over value")

            if e.ball < 1 or e.ball > 6:
                raise HTTPException(status_code=400, detail="invalid ball value (must be 1–6)")

            if e.runs_off_bat < 0:
                raise HTTPException(status_code=400, detail="negative runs_off_bat")

            if e.wides < 0 or e.no_balls < 0 or e.byes < 0 or e.leg_byes < 0:
                raise HTTPException(status_code=400, detail="invalid extras (negative values)")

        # -------------------------
        # ZERO LEGAL BALL CHECK
        # -------------------------
        legal_balls = sum(
            1 for e in inn.ball_events if e.wides == 0 and e.no_balls == 0
        )

        if legal_balls == 0:
            raise HTTPException(
                status_code=400,
                detail=f"no legal deliveries in innings {inn.innings_number}"
            )

    return ScoreboardService.compute(payload)

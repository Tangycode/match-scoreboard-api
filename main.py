from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import MatchSchema
from services import ScoreboardService

app = FastAPI()

# -----------------------------
# CORS (REQUIRED FOR FRONTEND)
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
# HEALTH CHECK (RENDER)
# -----------------------------
@app.get("/health")
def health():
    return {"status": "ok"}

# -----------------------------
# MAIN ENDPOINT
# -----------------------------
@app.post("/scoreboard")
def scoreboard(payload: MatchSchema):

    # -------------------------
    # BASIC VALIDATIONS
    # -------------------------
    if not payload.match or not payload.match.match_id:
        raise HTTPException(status_code=400, detail="missing match_id")

    if not payload.innings or len(payload.innings) == 0:
        raise HTTPException(status_code=400, detail="empty innings")

    if not payload.ball_events or len(payload.ball_events) == 0:
        raise HTTPException(status_code=400, detail="ball_events cannot be empty")

    # -------------------------
    # INNINGS ID VALIDATION
    # -------------------------
    innings_ids = {i.innings_id for i in payload.innings}

    for event in payload.ball_events:
        if not event.innings_id:
            raise HTTPException(status_code=400, detail="missing innings_id in ball_events")

        if event.innings_id not in innings_ids:
            raise HTTPException(status_code=400, detail=f"invalid innings_id: {event.innings_id}")

        if event.ball < 1 or event.ball > 6:
            raise HTTPException(status_code=400, detail="invalid ball value (must be 1–6)")

        if event.runs < 0:
            raise HTTPException(status_code=400, detail="invalid runs (cannot be negative)")

        if event.over < 0:
            raise HTTPException(status_code=400, detail="invalid over value")

    return ScoreboardService.compute(payload)

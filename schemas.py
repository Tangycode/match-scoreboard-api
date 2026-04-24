from pydantic import BaseModel
from typing import List, Optional, Dict

# -----------------------------
# MATCH
# -----------------------------
class Match(BaseModel):
    match_id: str
    format: Optional[str] = "T20"

# -----------------------------
# INNINGS
# -----------------------------
class Innings(BaseModel):
    innings_id: str
    team: str
    overs: float

# -----------------------------
# TEAM
# -----------------------------
class Team(BaseModel):
    name: str

# -----------------------------
# PLAYER
# -----------------------------
class Player(BaseModel):
    player_id: str
    team: str

# -----------------------------
# BALL EVENT
# -----------------------------
class BallEvent(BaseModel):
    innings_id: str
    over: int
    ball: int
    batsman: str
    bowler: str
    runs: int
    wicket: bool = False

# -----------------------------
# MAIN PAYLOAD
# -----------------------------
class MatchSchema(BaseModel):
    match: Match
    innings: List[Innings]
    teams: Dict[str, Team]
    players: List[Player]
    ball_events: List[BallEvent]

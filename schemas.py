from pydantic import BaseModel
from typing import List, Optional

class Match(BaseModel):
    match_id: str
    format: Optional[str] = "T20"

class Innings(BaseModel):
    innings_id: str
    team: str
    overs: float

class Team(BaseModel):
    name: str

class Player(BaseModel):
    player_id: str
    team: str

class BallEvent(BaseModel):
    innings_id: str
    over: int
    ball: int
    batsman: str
    bowler: str
    runs: int
    wicket: bool = False

class MatchSchema(BaseModel):
    match: Match
    innings: List[Innings]
    teams: dict
    players: List[Player]
    ball_events: List[BallEvent]

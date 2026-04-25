from pydantic import BaseModel
from typing import List, Optional

class BallEvent(BaseModel):
    over: int
    ball: int
    runs_off_bat: int = 0
    wides: int = 0
    no_balls: int = 0
    byes: int = 0
    leg_byes: int = 0
    wicket: bool = False
    batsman: Optional[str]
    bowler: Optional[str]

class Innings(BaseModel):
    innings_number: int
    batting_team: str
    bowling_team: str
    ball_events: List[BallEvent]

class MatchInput(BaseModel):
    match_id: str
    venue: Optional[str] = "Unknown"
    innings: List[Innings]

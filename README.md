{
"match_id": "string",
"venue": "string",
"innings": [
{
"innings_number": number,
"batting_team": "string",
"bowling_team": "string",
"ball_events": [
{
"over": number,
"ball": number,
"runs_off_bat": number,
"wides": number,
"no_balls": number,
"byes": number,
"leg_byes": number,
"wicket": boolean
}
]
}
]
}


---

## Output Schema


{
"match_id": "string",
"innings": [
{
"match": "string",
"venue": "string",
"innings_number": number,
"batting_team": "string",
"bowling_team": "string",
"score": number,
"wickets": number,
"overs": number,
"run_rate": number,
"top_batter": "string",
"top_bowler": "string",
"recent_balls": []
}
]
}


---

## Validation Errors (400)

- missing match_id
- empty innings
- missing innings_number
- duplicate innings_number
- missing team info
- empty ball_events
- invalid ball range (1–6)
- negative runs or extras
- invalid over value
- no legal deliveries in innings

---

## Sample Request


{
"match_id": "M001",
"venue": "Stadium A",
"innings": [
{
"innings_number": 1,
"batting_team": "A",
"bowling_team": "B",
"ball_events": [
{
"over": 1,
"ball": 1,
"runs_off_bat": 4,
"wides": 0,
"no_balls": 0,
"byes": 0,
"leg_byes": 0,
"wicket": false
}
]
}
]
}


---

## Sample Response


{
"match_id": "M001",
"innings": [
{
"match": "M001",
"venue": "Stadium A",
"innings_number": 1,
"batting_team": "A",
"bowling_team": "B",
"score": 4,
"wickets": 0,
"overs": 0.2,
"run_rate": 12.0,
"top_batter": "P1",
"top_bowler": "P2",
"recent_balls": []
}
]
}


---

## Integration Notes

- main.py handles routing + validation only  
- services.py handles all computation  
- schemas.py defines data contract  
- API is deterministic and stateless  

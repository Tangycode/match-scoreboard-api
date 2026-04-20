# Match Scoreboard api

## Overview
This API provides a live cricket match scoreboard in a clean and frontend-ready format. It accepts a match identifier along with innings data and computes the current score, wickets, overs, run rate, batting team, bowling team, and key performers. The API is designed to be integration-ready for the Khel AI MVP system and supports payload-driven usage without relying on hardcoded data.

---

## Endpoint
POST /match/scoreboard

---

## Input Format
```json
{
  "match_id": "match_001",
  "innings_data": [
    {
      "batting_team": "Team A",
      "bowling_team": "Team B",
      "ball_events": [
        {
          "runs": 4,
          "batter": "Player A",
          "bowler": "Player X",
          "is_wicket": false,
          "extra_type": null
        }
      ]
    }
  ]
}

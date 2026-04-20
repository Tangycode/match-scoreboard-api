def generate_match_scoreboard(match_id, innings_data):
    if not innings_data or len(innings_data) == 0:
        return {
            "match_id": match_id,
            "status": "No innings data available yet",
            "score": "0/0",
            "overs": "0.0",
            "run_rate": 0,
            "batting_team": None,
            "bowling_team": None,
            "key_performers": []
        }

    current_innings = innings_data[-1]

    ball_events = current_innings.get("ball_events", [])

    if not isinstance(ball_events, list) or len(ball_events) == 0:
        return {
            "match_id": match_id,
            "status": "No ball events available",
            "score": "0/0",
            "overs": "0.0",
            "run_rate": 0,
            "batting_team": current_innings.get("batting_team"),
            "bowling_team": current_innings.get("bowling_team"),
            "key_performers": []
        }

    total_runs = 0
    wickets = 0
    legal_balls = 0

    batter_stats = {}
    bowler_stats = {}

    for ball in ball_events:
        # Validate ball structure
        if not isinstance(ball, dict):
            continue

        runs = ball.get("runs", 0)
        batter = ball.get("batter")
        bowler = ball.get("bowler")
        is_wicket = ball.get("is_wicket", False)
        extra_type = ball.get("extra_type")

        # Type safety
        if not isinstance(runs, (int, float)):
            continue

        total_runs += runs

        if not extra_type:
            legal_balls += 1

        if is_wicket:
            wickets += 1

        # Batter stats
        if batter:
            if batter not in batter_stats:
                batter_stats[batter] = {"runs": 0}
            batter_stats[batter]["runs"] += runs

        # Bowler stats
        if bowler:
            if bowler not in bowler_stats:
                bowler_stats[bowler] = {"runs_conceded": 0, "wickets": 0}
            bowler_stats[bowler]["runs_conceded"] += runs

            if is_wicket:
                bowler_stats[bowler]["wickets"] += 1

    overs = f"{legal_balls // 6}.{legal_balls % 6}"
    run_rate = round((total_runs / legal_balls) * 6, 2) if legal_balls > 0 else 0

    # Safe key performer selection
    top_batter = max(batter_stats.items(), key=lambda x: x[1]["runs"], default=(None, {"runs": 0}))
    top_bowler = max(bowler_stats.items(), key=lambda x: x[1]["wickets"], default=(None, {"wickets": 0}))

    return {
        "match_id": match_id,
        "score": f"{int(total_runs)}/{wickets}",
        "overs": overs,
        "run_rate": run_rate,
        "batting_team": current_innings.get("batting_team"),
        "bowling_team": current_innings.get("bowling_team"),
        "key_performers": [
            {"type": "batter", "name": top_batter[0], "runs": top_batter[1]["runs"]},
            {"type": "bowler", "name": top_bowler[0], "wickets": top_bowler[1]["wickets"]}
        ]
    }

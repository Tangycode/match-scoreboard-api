class ScoreboardService:

    @staticmethod
    def compute(payload):

        results = []

        for inn in payload.innings:

            score = 0
            wickets = 0
            legal_balls = 0

            batter_runs = {}
            bowler_runs = {}

            recent_balls = []

            for e in inn.ball_events:

                # -------------------------
                # RUN CALCULATION
                # -------------------------
                total_runs = (
                    e.runs_off_bat +
                    e.wides +
                    e.no_balls +
                    e.byes +
                    e.leg_byes
                )

                score += total_runs

                # -------------------------
                # LEGAL BALL LOGIC
                # -------------------------
                if e.wides == 0 and e.no_balls == 0:
                    legal_balls += 1

                # -------------------------
                # WICKET
                # -------------------------
                if e.wicket:
                    wickets += 1

                # -------------------------
                # BATTER STATS
                # -------------------------
                if e.batsman:
                    batter_runs[e.batsman] = batter_runs.get(e.batsman, 0) + e.runs_off_bat

                # -------------------------
                # BOWLER STATS
                # -------------------------
                if e.bowler:
                    conceded = e.runs_off_bat + e.wides + e.no_balls
                    bowler_runs[e.bowler] = bowler_runs.get(e.bowler, 0) + conceded

                # -------------------------
                # RECENT BALLS
                # -------------------------
                recent_balls.append({
                    "over": e.over,
                    "ball": e.ball,
                    "runs": total_runs,
                    "wicket": e.wicket
                })

            overs = round(legal_balls / 6, 1)
            run_rate = round(score / overs, 2) if overs > 0 else 0

            top_batter = max(batter_runs, key=batter_runs.get) if batter_runs else None
            top_bowler = min(bowler_runs, key=bowler_runs.get) if bowler_runs else None

            results.append({
                "match": payload.match_id,
                "venue": payload.venue,
                "innings_number": inn.innings_number,
                "batting_team": inn.batting_team,
                "bowling_team": inn.bowling_team,
                "score": score,
                "wickets": wickets,
                "overs": overs,
                "run_rate": run_rate,
                "top_batter": top_batter,
                "top_bowler": top_bowler,
                "recent_balls": recent_balls[-6:]
            })

        return {"match_id": payload.match_id, "innings": results}

    @staticmethod
    def no_data(match_id):
        return {
            "match_id": match_id,
            "status": "no_data",
            "message": "No innings data available",
            "innings": []
        }

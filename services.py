class ScoreboardService:

    @staticmethod
    def compute(payload):

        # -----------------------------
        # STATE INITIALIZATION
        # -----------------------------
        state = {
            "innings_to_team": {},
            "team_score": {},
            "team_wickets": {},
            "team_overs": {}
        }

        # -----------------------------
        # BUILD INNINGS MAPPING
        # -----------------------------
        for inn in payload.innings:
            state["innings_to_team"][inn.innings_id] = inn.team

            state["team_score"][inn.team] = 0
            state["team_wickets"][inn.team] = 0
            state["team_overs"][inn.team] = 0.0

        # -----------------------------
        # PROCESS BALL EVENTS
        # -----------------------------
        for event in payload.ball_events:

            team = state["innings_to_team"].get(event.innings_id)

            if team is None:
                team = "UNKNOWN"

            # INIT SAFETY (EDGE CASES)
            if team not in state["team_score"]:
                state["team_score"][team] = 0
                state["team_wickets"][team] = 0
                state["team_overs"][team] = 0.0

            # -------------------------
            # SCORE UPDATE
            # -------------------------
            state["team_score"][team] += event.runs

            # -------------------------
            # WICKET UPDATE
            # -------------------------
            if event.wicket:
                state["team_wickets"][team] += 1

            # -------------------------
            # OVER CALCULATION
            # -------------------------
            state["team_overs"][team] = round(
                event.over + (event.ball / 6),
                1
            )

        # -----------------------------
        # BUILD INNINGS OUTPUT
        # -----------------------------
        innings_output = []

        for team in state["team_score"]:
            innings_output.append({
                "team": team,
                "score": state["team_score"][team],
                "wickets": state["team_wickets"][team],
                "overs": state["team_overs"][team]
            })

        # -----------------------------
        # FINAL RESPONSE (FRONTEND SAFE)
        # -----------------------------
        return {
            "match_id": payload.match.match_id,
            "innings": innings_output,
            "live_state": {
                "total_innings": len(payload.innings),
                "teams_count": len(state["team_score"])
            }
        }

    # -----------------------------
    # PLAYER TEAM RESOLUTION (FALLBACK)
    # -----------------------------
    @staticmethod
    def resolve_team(event, payload):

        for player in payload.players:
            if player.player_id == event.batsman:
                return player.team

        return "UNKNOWN"

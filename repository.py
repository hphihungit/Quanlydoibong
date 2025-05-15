from db import connect_db

def fetch_players():
    conn = connect_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT name, goals, assists FROM players")
            result = cursor.fetchall()
            return [{"name": r[0], "goals": r[1], "assists": r[2]} for r in result]
    finally:
        conn.close()


def fetch_matches():
    conn = connect_db()
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT result, team_score, opponent_score, location FROM matchs")
            result = cursor.fetchall()
            return [
                {
                    "result": normalize_result(r[0]),
                    "team_score": r[1],
                    "opponent_score": r[2],
                    "location": r[3]
                } for r in result
            ]
    finally:
        conn.close()


def normalize_result(result_str):
    result_str = result_str.lower().strip()
    if "thắng" in result_str or "th?ng" in result_str:
        return "win"
    elif "thua" in result_str:
        return "loss"
    else:
        return "draw"


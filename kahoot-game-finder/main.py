from flask import Flask, Response
import requests
import random
import time

app = Flask(__name__)

digits = "0123456789"

def is_game_active(code):
    try:
        response = requests.get(
            f"https://kahoot.it/reserve/session/{code}",
            timeout=10
        )

        if response.status_code != 200:
            return False, None

        data = response.json()

        # Check if game has a live session ID
        if not data.get('liveGameId'):
            return False, "No live game session"

        # Check if game is locked by host
        if data.get('loginRequired', False) or data.get('twoFactorAuth', False):
            return False, "Game locked by host"

        # Check if game started recently (last 10 minutes)
        start_time = data.get('startTime', 0)
        current_time = int(time.time() * 1000)
        time_diff = current_time - start_time

        if time_diff > 600000:
            return False, "Game too old"
        if time_diff < -300000:
            return False, "Game not started yet"

        return True, data

    except requests.exceptions.RequestException:
        return False, None
    except (ValueError, KeyError):
        return False, "Invalid response"

def generate_code():
    return ''.join(random.choices(digits, k=6))

def stream_scanner():
    codes_checked = 900000  # Start from 900000 to avoid common codes
    codes_found = 0
    codes_skipped = {"old":0, "no_session":0, "locked":0, "other":0}

    while True:
        code = generate_code()
        is_active, data = is_game_active(code)
        codes_checked += 1

        if is_active:
            codes_found += 1
            yield f"data: ACTIVE {code}\n\n"
        elif data == "Game too old":
            codes_skipped["old"] += 1
        elif data == "No live game session":
            codes_skipped["no_session"] += 1
        elif data == "Game locked by host":
            codes_skipped["locked"] += 1
        elif data:
            codes_skipped["other"] += 1

        if codes_checked % 100 == 0:
            total_skipped = sum(codes_skipped.values())
            stats = f"Checked {codes_checked} codes | Active: {codes_found} | Skipped old/ended: {total_skipped}"
            yield f"data: {stats}\n\n"

        time.sleep(0.1)

@app.route("/scan")
def scan():
    return Response(stream_scanner(), mimetype="text/event-stream")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

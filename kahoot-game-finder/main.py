from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import requests
import random
import time
import threading

app = Flask(__name__)
CORS(app)  # enable CORS for all routes

# Shared scanner state
scanner_data = {
    "codes_checked": 0,
    "codes_found": [],
    "codes_skipped": {"old": 0, "no_session": 0, "locked": 0, "other": 0},
    "new_codes": []  # store codes found since last poll
}

digits = "0123456789"

# -------------------- Flask Routes -------------------- #

@app.route("/")
def index():
    return send_from_directory(".", "index.html")  # index.html in root

@app.route("/status")
def status():
    # Return a copy of the data and clear new_codes
    data_to_send = scanner_data.copy()
    data_to_send["new_codes"] = scanner_data["new_codes"][:]
    scanner_data["new_codes"].clear()
    return jsonify(data_to_send)

# -------------------- Kahoot Scanner -------------------- #

def is_game_active(code):
    try:
        response = requests.get(f"https://kahoot.it/reserve/session/{code}", timeout=10)
        if response.status_code != 200:
            return False, None

        data = response.json()

        if not data.get('liveGameId'):
            return False, "No live game session"
        if data.get('loginRequired', False) or data.get('twoFactorAuth', False):
            return False, "Game locked by host"

        start_time = data.get('startTime', 0)
        current_time = int(time.time() * 1000)  # ms
        time_diff = current_time - start_time

        if time_diff > 600000:
            return False, "Game too old"
        if time_diff < -300000:
            return False, "Game not started yet"

        return True, data

    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return False, None
    except (ValueError, KeyError) as e:
        return False, f"Invalid response: {e}"

def generate_code():
    return ''.join(random.choices(digits, k=6))

def scanner_loop():
    print("Starting Kahoot code scanner...")
    print("Filtering for FRESH games only (started within last 10 minutes)...")
    print("Press Ctrl+C to stop\n")

    try:
        while True:
            code = generate_code()
            is_active, data = is_game_active(code)

            scanner_data["codes_checked"] += 1

            if is_active:
                scanner_data["codes_found"].append(code)
                scanner_data["new_codes"].append(code)
            elif data == "Game too old":
                scanner_data["codes_skipped"]["old"] += 1
            elif data == "No live game session":
                scanner_data["codes_skipped"]["no_session"] += 1
            elif data == "Game locked by host":
                scanner_data["codes_skipped"]["locked"] += 1
            elif data:
                scanner_data["codes_skipped"]["other"] += 1

            time.sleep(0.1)  # scan interval

    except KeyboardInterrupt:
        print("Scanner stopped by user.")

# -------------------- Main -------------------- #

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))

    # Start scanner in background thread
    thread = threading.Thread(target=scanner_loop, daemon=True)
    thread.start()

    app.run(host="0.0.0.0", port=port)

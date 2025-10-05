from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import requests
import random
import time
import threading
import os

app = Flask(__name__)
CORS(app)

scanner_data = {
    "codes_checked": 0,
    "codes_found": [],
    "new_codes": [],
    "codes_skipped": {"old": 0, "no_session": 0, "locked": 0, "other": 0}
}

digits = "0123456789"

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
        current_time = int(time.time() * 1000)
        age = current_time - start_time
        if age > 600000:
            return False, "Game too old"
        if age < -300000:
            return False, "Game not started yet"
        return True, data
    except:
        return False, None

def generate_code():
    return ''.join(random.choices(digits, k=6))

def scanner_loop():
    while True:
        code = generate_code()
        is_active, data = is_game_active(code)
        scanner_data["codes_checked"] += 1

        if is_active:
            scanner_data["codes_found"].append(code)
            scanner_data["new_codes"].append(code)
            with open("games.txt", "a") as f:
                f.write(code + "\n")
        else:
            if data == "Game too old":
                scanner_data["codes_skipped"]["old"] += 1
            elif data == "No live game session":
                scanner_data["codes_skipped"]["no_session"] += 1
            elif data == "Game locked by host":
                scanner_data["codes_skipped"]["locked"] += 1
            elif data:
                scanner_data["codes_skipped"]["other"] += 1

        time.sleep(0.1)

threading.Thread(target=scanner_loop, daemon=True).start()

# Serve index.html from root
@app.route("/")
def index():
    return send_from_directory(os.getcwd(), "index.html")

@app.route("/status")
def status():
    data_to_send = scanner_data.copy()
    data_to_send["new_codes"] = scanner_data["new_codes"][:]
    scanner_data["new_codes"].clear()
    return jsonify(data_to_send)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

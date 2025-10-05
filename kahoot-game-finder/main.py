from flask import Flask, jsonify
from flask_cors import CORS
import requests
import random
import time

app = Flask(__name__)
CORS(app)  # allow requests from your website

digits = "0123456789"

# -------- Helper functions --------

def is_game_active(code):
    """Check if a Kahoot game code is active."""
    try:
        response = requests.get(
            f"https://kahoot.it/reserve/session/{code}",
            timeout=10
        )
        if response.status_code != 200:
            return False, "No live game session"
        
        data = response.json()
        
        # Check for live game ID
        if not data.get("liveGameId"):
            return False, "No live game session"
        
        # Check if game is locked
        if data.get("loginRequired", False) or data.get("twoFactorAuth", False):
            return False, "Game locked by host"
        
        # Check game start time (only last 10 min)
        start_time = data.get("startTime", 0)
        current_time = int(time.time() * 1000)
        age = current_time - start_time
        
        if age > 600000:  # older than 10 min
            return False, "Game too old"
        if age < -300000:  # starts in more than 5 min
            return False, "Game not started yet"
        
        return True, data

    except requests.exceptions.RequestException as e:
        return False, f"Network error: {e}"
    except (ValueError, KeyError) as e:
        return False, f"Invalid response: {e}"

def generate_code():
    """Generate a random 6-digit Kahoot code."""
    return ''.join(random.choices(digits, k=6))

# -------- Flask routes --------

@app.route("/run", methods=["GET"])
def run_script():
    """Return a new random code and its status as JSON."""
    code = generate_code()
    active, data = is_game_active(code)

    # Add human-readable age if possible
    age_str = ""
    if isinstance(data, dict) and "startTime" in data:
        start_time = data["startTime"]
        current_time = int(time.time() * 1000)
        age_minutes = (current_time - start_time) / 60000
        if age_minutes < 0:
            age_str = f"starts in {abs(int(age_minutes))}m"
        else:
            age_str = f"{int(age_minutes)}m old"

    return jsonify({
        "code": code,
        "active": active,
        "age": age_str,
        "data": data if isinstance(data, dict) else None,
        "message": data if isinstance(data, str) else ""
    })

# -------- Main --------
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

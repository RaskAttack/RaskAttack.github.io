from flask import Flask, Response
import time
import random
import json
import threading

app = Flask(__name__)

digits = "0123456789"

def is_game_active(code):
    # Simulated logic for demonstration
    active = random.random() < 0.02  # ~2% chance active
    if active:
        return True, {"gameType":"quiz","startTime":int(time.time()*1000)}
    return False, "No live game session"

def generate_code():
    return ''.join(random.choices(digits, k=6))

def stream_scanner():
    codes_checked = 0
    codes_found = 0
    while True:
        code = generate_code()
        is_active, data = is_game_active(code)
        codes_checked += 1
        if is_active:
            yield f"data: ACTIVE {code}\n\n"
        if codes_checked % 100 == 0:
            yield f"data: Checked {codes_checked} codes | Active {codes_found}\n\n"
        time.sleep(0.1)

@app.route("/scan")
def scan():
    return Response(stream_scanner(), mimetype="text/event-stream")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

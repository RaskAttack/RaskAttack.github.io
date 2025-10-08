from flask import Flask, Response, stream_with_context, request, jsonify
from flask_cors import CORS
import requests
import random
import time
import threading
import queue
import string

# -----------------------
# Config (tweak here)
# -----------------------
WORKER_COUNT = 20
REQUEST_TIMEOUT = 5
STATS_INTERVAL = 100
CODE_LENGTH_MIN = 5
CODE_LENGTH_MAX = 10
SLEEP_BETWEEN_BATCHES = 0
# -----------------------

app = Flask(__name__)
CORS(app)

digits = "0123456789"

def human_age_from_start(start_time_ms):
    if not start_time_ms:
        return "unknown"
    now_ms = int(time.time() * 1000)
    delta_ms = now_ms - start_time_ms
    neg = delta_ms < 0
    delta_ms = abs(delta_ms)
    seconds = int(delta_ms / 1000)
    minutes, secs = divmod(seconds, 60)
    if minutes >= 60:
        hours, minutes = divmod(minutes, 60)
        age_str = f"{hours}h{minutes}m"
    elif minutes > 0:
        age_str = f"{minutes}m{secs}s"
    else:
        age_str = f"{secs}s"
    if neg:
        return f"starts in {age_str}"
    else:
        return f"{age_str} old"

def is_game_active(code):
    url = f"https://kahoot.it/reserve/session/{code}"
    try:
        resp = requests.get(url, timeout=REQUEST_TIMEOUT)
    except requests.exceptions.RequestException as e:
        return False, f"network_error: {e}"
    if resp.status_code != 200:
        return False, None
    try:
        data = resp.json()
    except Exception as e:
        return False, f"invalid_json: {e}"
    if not data.get("liveGameId"):
        return False, "No live game session"
    if data.get("loginRequired", False) or data.get("twoFactorAuth", False):
        return False, "Game locked by host"
    start_time = data.get("startTime", 0) or 0
    now_ms = int(time.time() * 1000)
    diff = now_ms - start_time
    if diff > 600000:
        return False, "Game too old"
    if diff < -300000:
        return False, "Game not started yet"
    return True, data

def generate_code():
    length = random.randint(CODE_LENGTH_MIN, CODE_LENGTH_MAX)
    return ''.join(random.choices(digits, k=length))

def worker_task(out_q, stop_event, stats):
    while not stop_event.is_set():
        code = generate_code()
        is_active, data = is_game_active(code)
        stats['checked'] += 1
        if is_active:
            stats['found'] += 1
            out_q.put(("active", code, data))
        else:
            reason = data if isinstance(data, str) else None
            if reason == "Game too old":
                stats['old'] += 1
            elif reason == "No live game session" or reason is None:
                stats['no_session'] += 1
            elif reason == "Game locked by host":
                stats['locked'] += 1
            else:
                stats['other'] += 1

def format_active_message(code, data):
    game_type = data.get("gameType") or data.get("type") or "unknown"
    start_time = data.get("startTime", 0) or 0
    age_str = human_age_from_start(start_time)
    return f"ACTIVE {code} | Type: {game_type} | Age: {age_str}"

def stream_scanner():
    out_q = queue.Queue(maxsize=1000)
    stop_event = threading.Event()
    stats = {'checked': 0, 'found': 0, 'old': 0, 'no_session': 0, 'locked': 0, 'other': 0}
    workers = []
    for _ in range(max(1, WORKER_COUNT)):
        t = threading.Thread(target=worker_task, args=(out_q, stop_event, stats), daemon=True)
        t.start()
        workers.append(t)
    print("✅ Scanner started with", len(workers), "workers (Render logs).")
    try:
        last_yield_checked = 0
        while True:
            try:
                item = out_q.get(timeout=1.0)
            except queue.Empty:
                if stats['checked'] - last_yield_checked >= STATS_INTERVAL:
                    total_skipped = stats['old'] + stats['no_session'] + stats['locked'] + stats['other']
                    stats_line = f"Checked {stats['checked']} codes | Active: {stats['found']} | Skipped: {total_skipped}"
                    yield f"data: {stats_line}\n\n"
                    last_yield_checked = stats['checked']
                continue
            kind, code, data = item
            if kind == "active":
                msg = format_active_message(code, data)
                yield f"data: {msg}\n\n"
            if stats['checked'] - last_yield_checked >= STATS_INTERVAL:
                total_skipped = stats['old'] + stats['no_session'] + stats['locked'] + stats['other']
                stats_line = f"Checked {stats['checked']} codes | Active: {stats['found']} | Skipped: {total_skipped}"
                yield f"data: {stats_line}\n\n"
                last_yield_checked = stats['checked']
            if SLEEP_BETWEEN_BATCHES:
                time.sleep(SLEEP_BETWEEN_BATCHES)
    except GeneratorExit:
        pass
    finally:
        stop_event.set()
        print("Stopping workers...")
        for t in workers:
            t.join(timeout=1.0)
        print("Workers stopped. Scanner ended.")

@app.route("/scan")
def scan():
    print("📡 /scan endpoint hit (Render logs).")
    return Response(stream_with_context(stream_scanner()), mimetype="text/event-stream")

@app.route("/flood", methods=["POST"])
def flood():
    data = request.json
    pin = str(data.get("pin"))
    amount = int(data.get("amount", 50))
    name = data.get("name", "Player")
    random_names = data.get("randomNames", False)
    amount = min(amount, 500)
    results = []
    for i in range(amount):
        if random_names:
            bot_name = "Player" + ''.join(random.choices(string.ascii_letters + string.digits, k=6))
        else:
            bot_name = name
        # Stub: Simulate join (real would use kahoot.py or similar for websocket join)
        results.append({"name": bot_name, "pin": pin})
    return jsonify({"ok": True, "joined": len(results)}), 200

if __name__ == "__main__":
    print("Starting Flask app (main.py).")
    app.run(host="0.0.0.0", port=5000)

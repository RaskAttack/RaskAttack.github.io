from flask import Flask, Response, stream_with_context
from flask_cors import CORS
import requests
import random
import time
import threading
import queue
from concurrent.futures import ThreadPoolExecutor

# -----------------------
# Config (tweak here)
# -----------------------
WORKER_COUNT = 20         # number of parallel worker threads (reduce if you see errors or rate-limits)
REQUEST_TIMEOUT = 5       # seconds per requests.get timeout
STATS_INTERVAL = 100      # yield a stats line every STATS_INTERVAL checks
CODE_LENGTH_MIN = 5       # min digits for PIN
CODE_LENGTH_MAX = 10      # max digits for PIN
SLEEP_BETWEEN_BATCHES = 0 # optional tiny pause in main loop (seconds). 0 = max throughput
# -----------------------

app = Flask(__name__)
CORS(app)

digits = "0123456789"

def human_age_from_start(start_time_ms):
    """Return friendly age string (e.g. '2m30s old' or 'starts in 1m')."""
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
    """
    Uses Kahoot reserve endpoint to determine whether a session is live & fresh.
    Returns: (is_active:bool, detail: dict or reason string or None)
    """
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

    # liveGameId indicates a session
    if not data.get("liveGameId"):
        return False, "No live game session"

    # Locked by host
    if data.get("loginRequired", False) or data.get("twoFactorAuth", False):
        return False, "Game locked by host"

    # Start time filtering (ms)
    start_time = data.get("startTime", 0) or 0
    now_ms = int(time.time() * 1000)
    diff = now_ms - start_time

    # older than 10 minutes -> skip
    if diff > 600000:
        return False, "Game too old"
    # more than 5 minutes in the future -> not started yet
    if diff < -300000:
        return False, "Game not started yet"

    return True, data

def generate_code():
    length = random.randint(CODE_LENGTH_MIN, CODE_LENGTH_MAX)
    return ''.join(random.choices(digits, k=length))

# Worker / concurrency machinery
def worker_task(out_q, stop_event, stats):
    """
    Worker thread: generate codes, check, and put results to out_q.
    Stats is a dict shared for counting (protected by simple atomic ops since ints).
    """
    while not stop_event.is_set():
        code = generate_code()
        is_active, data = is_game_active(code)
        stats['checked'] += 1
        if is_active:
            stats['found'] += 1
            out_q.put(("active", code, data))
        else:
            # categorize skips for stats
            reason = data if isinstance(data, str) else None
            if reason == "Game too old":
                stats['old'] += 1
            elif reason == "No live game session" or reason is None:
                stats['no_session'] += 1
            elif reason == "Game locked by host":
                stats['locked'] += 1
            else:
                stats['other'] += 1
        # no sleep here to maximize throughput; control via WORKER_COUNT
    # worker ends when stop_event is set

def format_active_message(code, data):
    # data is the JSON response from Kahoot
    game_type = data.get("gameType") or data.get("type") or "unknown"
    start_time = data.get("startTime", 0) or 0
    age_str = human_age_from_start(start_time)
    # build a compact message with details
    # Avoid dumping too much data; show type and age
    return f"ACTIVE {code} | Type: {game_type} | Age: {age_str}"

def stream_scanner():
    """
    Main generator used by Flask Response. Starts workers, yields messages as SSE data: lines.
    """
    # thread-safe queue for worker -> streamer
    out_q = queue.Queue(maxsize=1000)
    stop_event = threading.Event()

    # shared stats dict
    stats = {'checked': 0, 'found': 0, 'old': 0, 'no_session': 0, 'locked': 0, 'other': 0}

    # start thread pool
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
                item = out_q.get(timeout=1.0)  # wait for results
            except queue.Empty:
                # periodically yield stats even if no active found
                if stats['checked'] - last_yield_checked >= STATS_INTERVAL:
                    total_skipped = stats['old'] + stats['no_session'] + stats['locked'] + stats['other']
                    stats_line = f"Checked {stats['checked']} codes | Active: {stats['found']} | Skipped: {total_skipped}"
                    yield f"data: {stats_line}\n\n"
                    last_yield_checked = stats['checked']
                continue

            kind, code, data = item
            if kind == "active":
                # format message including age and type
                msg = format_active_message(code, data)
                yield f"data: {msg}\n\n"

            # produce stats every STATS_INTERVAL checks
            if stats['checked'] - last_yield_checked >= STATS_INTERVAL:
                total_skipped = stats['old'] + stats['no_session'] + stats['locked'] + stats['other']
                stats_line = f"Checked {stats['checked']} codes | Active: {stats['found']} | Skipped: {total_skipped}"
                yield f"data: {stats_line}\n\n"
                last_yield_checked = stats['checked']

            # tiny optional throttle to avoid busy-loop on streamer side
            if SLEEP_BETWEEN_BATCHES:
                time.sleep(SLEEP_BETWEEN_BATCHES)

    except GeneratorExit:
        # client disconnected
        pass
    finally:
        # signal workers to stop and join them
        stop_event.set()
        print("Stopping workers...")
        for t in workers:
            t.join(timeout=1.0)
        print("Workers stopped. Scanner ended.")

@app.route("/scan")
def scan():
    print("📡 /scan endpoint hit (Render logs).")
    return Response(stream_with_context(stream_scanner()), mimetype="text/event-stream")

if __name__ == "__main__":
    # helpful log line for Render
    print("Starting Flask app (main.py).")
    app.run(host="0.0.0.0", port=5000)

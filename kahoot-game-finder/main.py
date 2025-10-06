from flask import Flask, Response, stream_with_context
from flask_cors import CORS
import requests
import time

app = Flask(__name__)
CORS(app)  # ✅ make sure this comes AFTER app = Flask(...)

def stream_scanner():
    print("✅ Kahoot scanner started (Render logs).")
    start_code = 900000
    end_code = 999999
    checked = 0
    active = 0
    skipped = 0

    for code in range(start_code, end_code):
        url = f"https://kahoot.it/reserve/session/{code}"
        try:
            response = requests.get(url, timeout=3)
            if response.status_code == 200:
                data = response.json()
                if "liveGameId" in data:
                    active += 1
                    yield f"data: 🎯 ACTIVE GAME FOUND — PIN {code}\n\n"
                else:
                    skipped += 1
            else:
                skipped += 1
        except Exception as e:
            yield f"data: ⚠️ Error checking {code}: {e}\n\n"

        checked += 1

        if checked % 100 == 0:
            yield f"data: Checked {checked} codes | Active: {active} | Skipped: {skipped}\n\n"
            time.sleep(0.1)

@app.route("/scan")
def scan():
    print("📡 /scan endpoint hit (Render logs).")
    return Response(stream_with_context(stream_scanner()), mimetype="text/event-stream")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

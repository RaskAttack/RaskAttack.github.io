from flask import Flask, jsonify
from flask_cors import CORS
import threading
import random
import time
import requests

app = Flask(__name__)
CORS(app)

@app.route("/run", methods=["GET"])
def run_script():
    def scanner():
        digits = "0123456789"
        
        def generate_code():
            return ''.join(random.choices(digits, k=6))

        def is_game_active(code):
            try:
                response = requests.get(f"https://kahoot.it/reserve/session/{code}", timeout=10)
                if response.status_code != 200:
                    return False, None
                data = response.json()
                if not data.get('liveGameId'):
                    return False, "No live game session"
                return True, data
            except:
                return False, None

        codes_checked = 900000
        codes_found = 0

        while True:
            code = generate_code()
            active, data = is_game_active(code)
            if active:
                with open("games.txt", "a") as f:
                    f.write(code + "\n")
            codes_checked += 1
            time.sleep(0.1)

    # Start the scanner in a new thread
    thread = threading.Thread(target=scanner)
    thread.daemon = True
    thread.start()

    return jsonify({"status": "scanner started"}), 200

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

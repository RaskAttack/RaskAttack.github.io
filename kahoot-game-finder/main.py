from flask import Flask, jsonify
from flask_cors import CORS
import requests
import random
import time

app = Flask(__name__)
CORS(app)  # <-- enable CORS for all routes

@app.route("/run", methods=["GET"])
def run_script():
    num = random.randint(1, 100)
    response = requests.get("https://api.github.com")
    time.sleep(1)
    return jsonify({
        "random_number": num,
        "github_status": response.status_code
    })

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

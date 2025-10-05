from flask import Flask, jsonify
import requests
import random
import time
import os

app = Flask(__name__)

@app.route("/run", methods=["GET"])
def run_script():
    # Replace this with your actual script
    num = random.randint(1, 100)          # random number
    response = requests.get("https://api.github.com")  # example request
    time.sleep(1)                          # simulate delay

    return jsonify({
        "random_number": num,
        "github_status": response.status_code
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Use Render’s assigned port
    app.run(host="0.0.0.0", port=port)


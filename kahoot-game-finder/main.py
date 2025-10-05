from flask import Flask, jsonify
import requests
import random
import time

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
    app.run(host="0.0.0.0", port=5000)


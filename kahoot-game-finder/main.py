from flask import Flask, jsonify
from flask_cors import CORS
import requests
import random
import time

app = Flask(__name__)
CORS(app)  # <-- enable CORS for all routes

@app.route("/run", methods=["GET"])
def run_script():
   digits = "0123456789"


   def is_game_active(code):
       try:
           response = requests.get(
               f"https://kahoot.it/reserve/session/{code}",
               timeout=10
           )
           
           if response.status_code != 200:
               return False, None
           
           data = response.json()
           
           # Check if game has a live session ID
           if not data.get('liveGameId'):
               return False, "No live game session"
           
           # Check if game is locked by host (requires login)
           if data.get('loginRequired', False) or data.get('twoFactorAuth', False):
               return False, "Game locked by host"
           
           # Check if game started very recently (within last 10 minutes = 600000 ms)
           # This strict window ensures we only catch games that are likely still active
           start_time = data.get('startTime', 0)
           current_time = int(time.time() * 1000)  # Convert to milliseconds
           time_diff = current_time - start_time
           
           # Only accept games that started in the last 10 minutes
           if time_diff > 600000:  # More than 10 minutes old
               return False, "Game too old"
           
           # Accept games starting in the next 5 minutes (lobby phase)
           if time_diff < -300000:  # More than 5 minutes in the future
               return False, "Game not started yet"
           
           return True, data
           
       except requests.exceptions.RequestException as e:
           print(f"Network error: {e}")
           return False, None
       except (ValueError, KeyError) as e:
           return False, f"Invalid response: {e}"
   
   
   def generate_code():
       return ''.join(random.choices(digits, k=6))
   
   
   def main():
       codes_checked = 900000  # Start from 900000 to avoid common codes
       codes_found = 0
       codes_skipped = {"old": 0, "no_session": 0, "locked": 0, "other": 0}
       
       print("Starting Kahoot code scanner...")
       print("Filtering for FRESH games only (started within last 10 minutes)...")
       print("Press Ctrl+C to stop\n")
       
       try:
           while True:
               code = generate_code()
               is_active, data = is_game_active(code)
               
               if is_active:
                   with open("games.txt", "a") as file:
                       file.write(code + "\n")
                   codes_found += 1
                   
                   # Show game details with age - BIG PIN DISPLAY
                   print("\n" + "="*50)
                   print(f"  🎯 GAME PIN: {code}")
                   print("="*50)
                   
                   
                   if isinstance(data, dict):
                       game_type = data.get('gameType', 'unknown')
                       start_time = data.get('startTime', 0)
                       current_time = int(time.time() * 1000)
                       age_minutes = (current_time - start_time) / 60000
                       if age_minutes < 0:
                           age_str = f"starts in {abs(int(age_minutes))}m"
                       else:
                           age_str = f"{int(age_minutes)}m old"
                       print(f"  Type: {game_type} | Age: {age_str}")
                   print()
               elif data == "Game too old":
                   codes_skipped["old"] += 1
               elif data == "No live game session":
                   codes_skipped["no_session"] += 1
               elif data == "Game locked by host":
                   codes_skipped["locked"] += 1
               elif data:
                   codes_skipped["other"] += 1
               
               codes_checked += 1
               
               if codes_checked % 100 == 0:
                   total_skipped = sum(codes_skipped.values())
                   print(f"Checked {codes_checked} codes | Active: {codes_found} | Skipped old/ended: {total_skipped}")
               
               time.sleep(0.1)
       
       except KeyboardInterrupt:
           print(f"\n\nStopped by user.")
           print(f"Total codes checked: {codes_checked}")
           print(f"Total ACTIVE games found: {codes_found}")
           print(f"Skipped: {codes_skipped['old']} old games, {codes_skipped['no_session']} ended games, {codes_skipped['locked']} locked games")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

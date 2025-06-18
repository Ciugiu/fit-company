from flask import Flask, request, jsonify
import logging
import sys
from .services import google
from pydantic import ValidationError
import threading
import schedule
import time

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Create Flask app
app = Flask(__name__)
app.logger.setLevel(logging.DEBUG)

# Force stdout to be unbuffered
sys.stdout.reconfigure(line_buffering=True)

@app.route("/health")
def health():
    return {"status": "UP"}

def daily_check():
    pass

def run_scheduler():
    schedule.every(24).hours.do(daily_check)
    while True:
        schedule.run_pending()
        time.sleep(60)

def run_app():
    """Entry point for the application script"""
    # Start the scheduler in a separate thread
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()
    app.run(host="0.0.0.0", port=5000, debug=True)

if __name__ == "__main__":
    run_app()
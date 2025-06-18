from flask import Flask, jsonify
from .database import init_db
from .models import WorkoutStat

app = Flask(__name__)

@app.route("/stats", methods=["GET"])
def get_workout_stats():
    stats = WorkoutStat.query.all()
    return jsonify([stat.to_dict() for stat in stats]), 200

def run_app():
    init_db()
    app.run(host="0.0.0.0", port=5001, debug=True)

if __name__ == "__main__":
    run_app()
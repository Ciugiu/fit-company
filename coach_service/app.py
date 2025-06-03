from flask import Flask, request, jsonify
import requests
import os
from shared_fit.wod import request_wod
from src.fit.models_db import ExerciseModel, MuscleGroupModel, exercise_muscle_groups
from src.fit.database import db_session

app = Flask(__name__)

MONOLITH_URL = os.environ.get("MONOLITH_URL", "http://monolith:5000")

@app.route("/generate-wod", methods=["POST"])
def generate_wod():
    user_email = request.json.get("email")
    if not user_email:
        return jsonify({"error": "email required"}), 400

    resp = requests.get(f"{MONOLITH_URL}/api/users/{user_email}/history?day=yesterday")
    if resp.status_code != 200:
        return jsonify({"error": "Could not fetch user history"}), 500
    history = resp.json()

    exclude_exercise_ids = []  # TODO: fetch exclude_exercise_ids from monolith

    wod = request_wod(
        db_session,
        ExerciseModel,
        MuscleGroupModel,
        exercise_muscle_groups,
        exclude_exercise_ids=exclude_exercise_ids
    )

    # TODO: serialize and return wod
    return jsonify(wod)
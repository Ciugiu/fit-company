from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from ..database import get_db
from ..models_db import WorkoutModel, UserExerciseHistory
from ..models_dto import WodUpdateSchema

wod_bp = Blueprint("wod", __name__, url_prefix="/wods")


@wod_bp.route("/<int:wod_id>", methods=["PUT"])
def update_wod(wod_id):
    """
    Updates a WOD (Workout of the Day).
    Expects a JSON body with a new list of exercise IDs.
    """
    db = next(get_db())
    
    try:
        data = request.get_json()
        if not data:
            return jsonify({"message": "No input data provided"}), 400

        update_data = WodUpdateSchema.model_validate(data)

        workout = db.query(WorkoutModel).filter(WorkoutModel.id == wod_id).first()
        if not workout:
            return jsonify({"message": f"WOD with id {wod_id} not found"}), 404

        # Delete old exercises for this workout
        db.query(UserExerciseHistory).filter(UserExerciseHistory.workout_id == wod_id).delete(synchronize_session=False)

        # Add new exercises
        new_exercises = []
        for exercise_id in update_data.exercises:
            new_exercise = UserExerciseHistory(workout_id=wod_id, exercise_id=exercise_id)
            new_exercises.append(new_exercise)
        
        db.add_all(new_exercises)
        db.commit()

        return jsonify({"message": f"WOD {wod_id} updated successfully."})

    except ValidationError as e:
        db.rollback()
        return jsonify({"error": "Invalid data", "details": e.errors()}), 400
    except Exception as e:
        db.rollback()
        return jsonify({"error": "An error occurred", "details": str(e)}), 500
    finally:
        db.close()
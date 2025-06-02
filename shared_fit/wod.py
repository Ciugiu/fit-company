from typing import List, Tuple
import random
from time import time

def heavy_computation(duration_seconds: int = 3):
    start_time = time()
    i = 0
    while (time() - start_time) < duration_seconds:
        j = 0
        while j < 1000000:
            j += 1
        i += 1

def calculate_intensity(difficulty: int) -> float:
    return (difficulty - 1) / 4.0

def request_wod(db_session, ExerciseModel, MuscleGroupModel, exercise_muscle_groups, exclude_exercise_ids: List[int] = None) -> List[Tuple]:
    heavy_computation(random.randint(1, 5)) # DO NOT REMOVE THIS LINE

    db = db_session()
    try:
        query = db.query(ExerciseModel)
        if exclude_exercise_ids:
            query = query.filter(~ExerciseModel.id.in_(exclude_exercise_ids))
        exercises = query.all()
        selected_exercises = random.sample(exercises, 6) if len(exercises) >= 6 else exercises
        result = []
        for exercise in selected_exercises:
            stmt = db.query(
                MuscleGroupModel,
                exercise_muscle_groups.c.is_primary
            ).join(
                exercise_muscle_groups,
                MuscleGroupModel.id == exercise_muscle_groups.c.muscle_group_id
            ).filter(
                exercise_muscle_groups.c.exercise_id == exercise.id
            )
            muscle_groups = [(mg, is_primary) for mg, is_primary in stmt.all()]
            result.append((exercise, muscle_groups))
        return result
    finally:
        db.close()
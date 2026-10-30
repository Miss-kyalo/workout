from flask import request, jsonify, make_response
from datetime import datetime
from marshmallow import ValidationError

from config import app, db
from models import Workout, Exercise, WorkoutExercise
from schemas import (
    workout_schema,
    workouts_schema,
    exercise_schema,
    exercises_schema,
    workout_exercise_schema,
)


@app.route('/workouts', methods=['GET'])
def get_workouts():
    """List of all workouts."""
    workouts = Workout.query.all()
    return make_response(jsonify(workouts_schema.dump(workouts)), 200)


@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout_by_id(id):
    """Show workout with its associated exercises and metrics."""
    workout = db.session.get(Workout, id)
    if not workout:
        return make_response(jsonify({'error': 'Workout not found'}), 404)
    return make_response(jsonify(workout_schema.dump(workout)), 200)


@app.route('/workouts', methods=['POST'])
def create_workout():
    """Create a new workout."""
    json_data = request.get_json()
    if not json_data:
        return make_response(jsonify({'error': 'No input data provided'}), 400)

    try:
        data = workout_schema.load(json_data)
        workout = Workout(
            date=data['date'],
            duration_minutes=data['duration_minutes'],
            notes=data.get('notes')
        )
        db.session.add(workout)
        db.session.commit()
        return make_response(jsonify(workout_schema.dump(workout)), 201)
    except ValidationError as err:
        return make_response(jsonify({'errors': err.messages}), 422)
    except ValueError as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), 422)
    except Exception:
        db.session.rollback()
        return make_response(jsonify({'error': 'Could not process request'}), 400)


@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    """Delete a workout and its WorkoutExercises."""
    workout = db.session.get(Workout, id)
    if not workout:
        return make_response(jsonify({'error': 'Workout not found'}), 404)

    db.session.delete(workout)
    db.session.commit()
    return make_response(jsonify({'message': f'Workout {id} deleted successfully'}), 200)



@app.route('/exercises', methods=['GET'])
def get_exercises():
    """List all exercises."""
    exercises = Exercise.query.all()
    return make_response(jsonify(exercises_schema.dump(exercises)), 200)


@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise_by_id(id):
    """Show an exercise and its details."""
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return make_response(jsonify({'error': 'Exercise not found'}), 404)
    return make_response(jsonify(exercise_schema.dump(exercise)), 200)


@app.route('/exercises', methods=['POST'])
def create_exercise():
    """Create a new exercise."""
    json_data = request.get_json()
    if not json_data:
        return make_response(jsonify({'error': 'No input data provided'}), 400)

    try:
        data = exercise_schema.load(json_data)
        exercise = Exercise(
            name=data['name'],
            category=data['category'],
            equipment_needed=data['equipment_needed']
        )
        db.session.add(exercise)
        db.session.commit()
        return make_response(jsonify(exercise_schema.dump(exercise)), 201)
    except ValidationError as err:
        return make_response(jsonify({'errors': err.messages}), 422)
    except ValueError as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), 422)
    except Exception:
        db.session.rollback()
        return make_response(jsonify({'error': 'Could not process request'}), 400)


@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    """Delete an exercise and its associated WorkoutExercises."""
    exercise = db.session.get(Exercise, id)
    if not exercise:
        return make_response(jsonify({'error': 'Exercise not found'}), 404)

    db.session.delete(exercise)
    db.session.commit()
    return make_response(jsonify({'message': f'Exercise {id} deleted successfully'}), 200)


@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    """Add an existing exercise to an existing workout with sets/reps/duration."""
    workout = db.session.get(Workout, workout_id)
    if not workout:
        return make_response(jsonify({'error': 'Workout not found'}), 404)

    exercise = db.session.get(Exercise, exercise_id)
    if not exercise:
        return make_response(jsonify({'error': 'Exercise not found'}), 404)

    json_data = request.get_json() or {}

    try:
        data = workout_exercise_schema.load(json_data)
        workout_exercise = WorkoutExercise(
            workout_id=workout.id,
            exercise_id=exercise.id,
            reps=data.get('reps'),
            sets=data.get('sets'),
            duration_seconds=data.get('duration_seconds')
        )
        db.session.add(workout_exercise)
        db.session.commit()
        return make_response(jsonify(workout_exercise_schema.dump(workout_exercise)), 201)
    except ValidationError as err:
        return make_response(jsonify({'errors': err.messages}), 422)
    except ValueError as e:
        db.session.rollback()
        return make_response(jsonify({'error': str(e)}), 422)
    except Exception:
        db.session.rollback()
        return make_response(jsonify({'error': 'Could not process request'}), 400)


if __name__ == '__main__':
    app.run(port=5555, debug=True)


"""Seed script to populate initial sample data into app.db."""

from datetime import date
from config import app, db
from models import Workout, Exercise, WorkoutExercise

with app.app_context():
    print("Clearing existing database tables...")
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    print("Creating sample exercises...")
    ex_pushup = Exercise(name="Push Up", category="Strength", equipment_needed=False)
    ex_squat = Exercise(name="Back Squat", category="Strength", equipment_needed=True)
    ex_running = Exercise(name="Treadmill Run", category="Cardio", equipment_needed=True)
    ex_plank = Exercise(name="Plank Hold", category="Balance", equipment_needed=False)

    db.session.add_all([ex_pushup, ex_squat, ex_running, ex_plank])
    db.session.commit()

    print("Creating sample workouts...")
    w1 = Workout(date=date(2026, 3, 15), duration_minutes=45, notes="Leg day and core session.")
    w2 = Workout(date=date(2026, 3, 16), duration_minutes=30, notes="Morning light cardio.")

    db.session.add_all([w1, w2])
    db.session.commit()

    print("Associating exercises with workouts...")
    we1 = WorkoutExercise(workout_id=w1.id, exercise_id=ex_squat.id, sets=4, reps=10)
    we2 = WorkoutExercise(workout_id=w1.id, exercise_id=ex_plank.id, duration_seconds=120)
    we3 = WorkoutExercise(workout_id=w2.id, exercise_id=ex_running.id, duration_seconds=1800)

    db.session.add_all([we1, we2, we3])
    db.session.commit()

    print("Database seeding completed successfully!")
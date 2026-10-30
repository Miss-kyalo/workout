from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint
from config import db

class Exercise(db.Model):
    __tablename__ = "exercises"

    id= db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    equipment_needed=db.Column(db.Boolean,nullable=False,default=False)

#relationships
    workout_exercises = db.relationship(
        "WorkoutExercise"
        back_populates='exercise',
        cascade='all, delete-orphan'
    )
    workouts = db.relationship(
        'Workout',
        secondary='workout_exercises',
        back_populates='exercises',
        viewonly=True
    )
    #validations
    
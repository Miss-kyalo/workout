from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint
from config import db

class Exercise(db.Model):
    __tablename__ = "exercises"

    id= db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    category = db.Column(db.String, nullable=False)
    equipment_needed=db.Column(db.Boolean,nullable=False,default=False)

    workout_exercises = db.relationship(
        "WorkoutExercise",
        back_populates='exercise',
        cascade='all, delete-orphan'
    )
    workouts = db.relationship(
        'Workout',
        secondary='workout_exercises',
        back_populates='exercises',
        viewonly=True
    )
    @validates('name')
    def validate_name(self, key, value):
        if not value or not isinstance(value,str) or len(value.strip())==0:
            raise ValueError("Exercise cannot be blank")
        return value.strip()
    
    @validates('category')
    def validate_category(self, key, value):
        allowed_categories = {'Cardio', 'Strength', 'Flexibility', 'Balance'}
        if value not in allowed_categories:
            raise ValueError(
                f"Category must be one of: {', '.join(sorted(allowed_categories))}."
            )
        return value
    def __repr__(self):
        return f"<Exercise id={self.id} name='{self.name}' category='{self.category}'>"
    
    
class Workout(db.Model):
    __tablename__= 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text, nullable=True)

    __table_args__ =(
        CheckConstraint('duration_minutes > 0', name='check_duration_positive'),
    )
    workout_exercises = db.relationship(
        'WorkoutExercise',
        back_populates='workout',
        cascade='all, delete-orphan'
    )
    exercises = db.relationship(
        'Exercise',
        secondary='workout_exercises',
        back_populates='workouts',
        viewonly=True
    )
    @validates('duration_minutes')
    def validates_duration(self,key,value):
        if value is None or not isinstance(value, int) or value <= 0:
            raise ValueError('Workout duration_minutes must be greater than 0.')
        return value
    
    def __repr__(self):
        return f"<Workout id={self.id} date='{self.date}' duration={self.duration_minutes}m>"

class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer, nullable=True)
    sets = db.Column(db.Integer, nullable=True)
    duration_seconds = db.Column(db.Integer, nullable=True)

    __table_args__ = (
        CheckConstraint('reps IS NULL OR reps >= 0', name='check_reps_non_negative'),
        CheckConstraint('sets IS NULL OR sets >= 0', name='check_sets_non_negative'),
        CheckConstraint('duration_seconds IS NULL OR duration_seconds >= 0', name='check_duration_seconds_non_negative'),
    )
    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    def __repr__(self):
        return f"<WorkoutExercise id={self.id} workout_id={self.workout_id} exercise_id={self.exercise_id}>"
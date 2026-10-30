from marshmallow import Schema,fields,validate,validates_schema,ValidationError

class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))
    category = fields.Str(
        required=True,
        validate=validate.OneOf(['Cardio', 'Strength', 'Flexibility', 'Balance'])
    )
    equipment_needed = fields.Bool(required=True)

class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(dump_only=True)
    exercise_id = fields.Int(dump_only=True)
    reps = fields.Int(allow_none=True, validate=validate.Range(min=0))
    sets = fields.Int(allow_none=True, validate=validate.Range(min=0))
    duration_seconds = fields.Int(allow_none=True, validate=validate.Range(min=0))

    exercise = fields.Nested(ExerciseSchema, dump_only=True)

    @validates_schema
    def validate_metrics(self, data, **kwargs):
        reps = data.get('reps')
        sets = data.get('sets')
        duration = data.get('duration_seconds')
        
        if reps is None and sets is None and duration is None:
            raise ValidationError("Must supply either (reps/sets) or duration_seconds for an exercise.")
class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1))
    notes = fields.Str(allow_none=True)

workout_exercises = fields.List(fields.Nested(WorkoutExerciseSchema), dump_only=True)

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)

workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)

workout_exercise_schema = WorkoutExerciseSchema()
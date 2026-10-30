# Workout Application API Backend

A robust, RESTful backend API designed for personal trainers to track client workouts and reusable exercises. Built with Flask, SQLAlchemy, and Marshmallow, this application provides full relational data management, strict data validations, and clean REST endpoints following industry best practices.

## Table of Contents

- [Features](#features)
- [Tech Stack & Dependencies](#tech-stack--dependencies)
- [Database Architecture](#database-architecture)
- [Installation & Setup](#installation--setup)
- [Running the Application](#running-the-application)
- [API Endpoints Reference](#api-endpoints-reference)
- [Validations & Error Handling](#validations--error-handling)

## Features

- **Workout Management:** Create, view, and delete workouts along with duration and custom notes.
- **Exercise Library:** Build and maintain a reusable list of exercises categorized by type and equipment requirements.
- **Workout-Exercise Junction:** Connect exercises to specific workouts with tailored volume metrics (sets, reps, duration).
- **Cascading Deletions:** Deleting a workout or exercise safely cleans up associated join table entries without leaving orphan records.
- **Multi-Level Validations:** Full data integrity enforced across database constraints, model-level `@validates`, and Marshmallow schema validations.

## Tech Stack & Dependencies

- **Python:** 3.8.13+
- **Framework:** Flask (2.2.2)
- **ORM & Migrations:** Flask-SQLAlchemy (3.0.3), Flask-Migrate (3.1.0)
- **Serialization & Validation:** Marshmallow (3.20.1)
- **Database:** SQLite
- **Environment Management:** Pipenv

## Database Architecture

### Exercise

| Field | Type | Notes |
|-------|------|-------|
| `id` | Integer | Primary key |
| `name` | String | Non-empty |
| `category` | String | Cardio, Strength, Flexibility, Balance |
| `equipment_needed` | Boolean | |

### Workout

| Field | Type | Notes |
|-------|------|-------|
| `id` | Integer | Primary key |
| `date` | Date | |
| `duration_minutes` | Integer | Must be > 0 |
| `notes` | Text | Optional |

### WorkoutExercise (Join Table)

| Field | Type | Notes |
|-------|------|-------|
| `id` | Integer | Primary key |
| `workout_id` | Foreign key | `workouts.id` |
| `exercise_id` | Foreign key | `exercises.id` |
| `reps` | Integer | Optional, non-negative |
| `sets` | Integer | Optional, non-negative |
| `duration_seconds` | Integer | Optional, non-negative |

## Installation & Setup

1. **Clone the repository**

   ```bash
   git clone <your-github-repo-url>
   cd <your-repo-folder>
   ```

2. **Set up the virtual environment** — install all required dependencies using pipenv:

   ```bash
   pipenv install
   pipenv shell
   ```

3. **Initialize & migrate the database** — from the `server/` directory:

   ```bash
   cd server
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade head
   ```

4. **Seed the database** — populate sample workouts, exercises, and performance logs:

   ```bash
   python seed.py
   ```

## Running the Application

Start the Flask development server on port 5555:

```bash
python app.py
```

The server listens at: <http://127.0.0.1:5555>

## API Endpoints Reference

### Workouts

| Method | Endpoint | Description | Sample Payload / Params |
|--------|----------|-------------|-------------------------|
| GET | `/workouts` | Retrieve a list of all workouts. | None |
| GET | `/workouts/<id>` | Retrieve a single workout with all attached exercises, reps, sets, and duration metrics. | URL param: `id` |
| POST | `/workouts` | Create a new workout. | `{"date": "2026-03-15", "duration_minutes": 45, "notes": "Leg day"}` |
| DELETE | `/workouts/<id>` | Delete a workout and its associated exercise logs. | URL param: `id` |

### Exercises

| Method | Endpoint | Description | Sample Payload / Params |
|--------|----------|-------------|-------------------------|
| GET | `/exercises` | Retrieve a list of all reusable exercises. | None |
| GET | `/exercises/<id>` | Retrieve details for a specific exercise. | URL param: `id` |
| POST | `/exercises` | Create a new reusable exercise. | `{"name": "Squat", "category": "Strength", "equipment_needed": true}` |
| DELETE | `/exercises/<id>` | Delete an exercise and remove its association from existing workouts. | URL param: `id` |

### Workout-Exercise Association

| Method | Endpoint | Description | Sample Payload / Params |
|--------|----------|-------------|-------------------------|
| POST | `/workouts/<workout_id>/exercises/<exercise_id>/workout_exercises` | Add an exercise to a workout with performance stats (sets/reps or `duration_seconds`). | `{"sets": 4, "reps": 10, "duration_seconds": null}` |

## Validations & Error Handling

The application protects against invalid operations at three levels:

1. **Database table constraints (`CheckConstraint`):** Enforces positive numeric constraints at the database level (e.g., `duration_minutes > 0`).
2. **SQLAlchemy model validations (`@validates`):** Restricts category values (Cardio, Strength, Flexibility, Balance) and prevents empty text fields before committing session data.
3. **Marshmallow schema validations:** Validates request parameters and payload structure on incoming POST requests, returning `422 Unprocessable Entity` responses with field-specific error messages.

from datetime import datetime, timezone
import json
import os
from typing import Any, Dict, List

from flask import Flask, jsonify, request

app = Flask(__name__)

# Keep data in a JSON file next to this script.
DATA_FILE = os.path.join(os.path.dirname(__file__), "courses.json")

# Allowed course progress values.
VALID_STATUS = {"Not Started", "In Progress", "Completed"}


def ensure_data_file_exists() -> None:
    """Create courses.json with an empty list if it does not exist yet."""
    if not os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "w", encoding="utf-8") as file:
                json.dump([], file)
        except OSError as exc:
            raise IOError(f"Could not create data file: {exc}") from exc


def load_courses() -> List[Dict[str, Any]]:
    """Read all courses from the JSON file."""
    ensure_data_file_exists()

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
    except OSError as exc:
        raise IOError(f"Could not read data file: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise ValueError(f"Data file contains invalid JSON: {exc}") from exc

    if not isinstance(data, list):
        raise ValueError("Data file format is invalid. Expected a list of courses.")

    return data


def save_courses(courses: List[Dict[str, Any]]) -> None:
    """Write all courses back to the JSON file."""
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(courses, file, indent=2)
    except OSError as exc:
        raise IOError(f"Could not write data file: {exc}") from exc


def get_next_id(courses: List[Dict[str, Any]]) -> int:
    """Generate the next numeric id, starting from 1."""
    if not courses:
        return 1
    return max(course.get("id", 0) for course in courses) + 1


def is_valid_date(date_text: str) -> bool:
    """Validate a date string in YYYY-MM-DD format."""
    try:
        datetime.strptime(date_text, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_course_payload(payload: Dict[str, Any]) -> str | None:
    """Return an error message if payload is invalid, otherwise return None."""
    required_fields = ["name", "description", "target_date", "status"]

    missing = [field for field in required_fields if not payload.get(field)]
    if missing:
        return f"Missing required fields: {', '.join(missing)}"

    if payload["status"] not in VALID_STATUS:
        return (
            "Invalid status value. Must be one of: "
            "Not Started, In Progress, Completed"
        )

    if not is_valid_date(payload["target_date"]):
        return "Invalid target_date. Use YYYY-MM-DD format."

    return None


def api_error(message: str, status_code: int):
    """Small helper for consistent JSON error responses."""
    return jsonify({"error": message}), status_code


@app.route("/api/courses", methods=["POST"])
@app.route("/api/courses/", methods=["POST"])
def create_course():
    """Create and store a new course."""
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return api_error("Request body must be valid JSON.", 400)

    validation_error = validate_course_payload(payload)
    if validation_error:
        return api_error(validation_error, 400)

    try:
        courses = load_courses()

        new_course = {
            "id": get_next_id(courses),
            "name": payload["name"],
            "description": payload["description"],
            "target_date": payload["target_date"],
            "status": payload["status"],
            # Use UTC timestamp for consistency across systems.
            "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        }

        courses.append(new_course)
        save_courses(courses)
    except (IOError, ValueError) as exc:
        return api_error(str(exc), 500)

    return jsonify(new_course), 201


@app.route("/api/courses", methods=["GET"])
@app.route("/api/courses/", methods=["GET"])
def get_all_courses():
    """Return every stored course."""
    try:
        courses = load_courses()
    except (IOError, ValueError) as exc:
        return api_error(str(exc), 500)

    return jsonify(courses), 200


@app.route("/api/courses/stats", methods=["GET"])
@app.route("/api/courses/stats/", methods=["GET"])
def get_course_stats():
    """Return aggregate statistics about all stored courses."""
    try:
        courses = load_courses()
    except (IOError, ValueError) as exc:
        return api_error(str(exc), 500)

    # Start each status counter at zero so all categories are always present.
    by_status = {"Not Started": 0, "In Progress": 0, "Completed": 0}

    for course in courses:
        status = course.get("status")
        if status in by_status:
            by_status[status] += 1

    stats = {
        "total_courses": len(courses),
        "by_status": by_status,
    }

    return jsonify(stats), 200


@app.route("/api/courses/<int:course_id>", methods=["GET"])
@app.route("/api/courses/<int:course_id>/", methods=["GET"])
def get_course(course_id: int):
    """Return one course by id."""
    try:
        courses = load_courses()
    except (IOError, ValueError) as exc:
        return api_error(str(exc), 500)

    course = next((item for item in courses if item.get("id") == course_id), None)
    if not course:
        return api_error("Course not found.", 404)

    return jsonify(course), 200


@app.route("/api/courses/<int:course_id>", methods=["PUT"])
@app.route("/api/courses/<int:course_id>/", methods=["PUT"])
def update_course(course_id: int):
    """Replace a course's editable fields by id."""
    payload = request.get_json(silent=True)
    if not isinstance(payload, dict):
        return api_error("Request body must be valid JSON.", 400)

    validation_error = validate_course_payload(payload)
    if validation_error:
        return api_error(validation_error, 400)

    try:
        courses = load_courses()

        course = next((item for item in courses if item.get("id") == course_id), None)
        if not course:
            return api_error("Course not found.", 404)

        course["name"] = payload["name"]
        course["description"] = payload["description"]
        course["target_date"] = payload["target_date"]
        course["status"] = payload["status"]

        save_courses(courses)
    except (IOError, ValueError) as exc:
        return api_error(str(exc), 500)

    return jsonify(course), 200


@app.route("/api/courses/<int:course_id>", methods=["DELETE"])
@app.route("/api/courses/<int:course_id>/", methods=["DELETE"])
def delete_course(course_id: int):
    """Delete one course by id."""
    try:
        courses = load_courses()

        course = next((item for item in courses if item.get("id") == course_id), None)
        if not course:
            return api_error("Course not found.", 404)

        courses.remove(course)
        save_courses(courses)
    except (IOError, ValueError) as exc:
        return api_error(str(exc), 500)

    return jsonify({"message": "Course deleted successfully."}), 200


if __name__ == "__main__":
    # Ensure data file exists before the first request.
    try:
        ensure_data_file_exists()
    except IOError as exc:
        # If file creation fails, stop startup with a clear error.
        raise RuntimeError(str(exc)) from exc

    app.run(debug=True)

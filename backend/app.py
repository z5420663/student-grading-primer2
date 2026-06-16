from flask import Flask, jsonify, request
from flask_cors import CORS

import db

app = Flask(__name__)
CORS(app)

# Instructions:
# - Use the functions in backend/db.py in your implementation.
# - You are free to use additional data structures in your solution
# - You must define and tell your tutor one edge case you have devised and how you have addressed this

@app.route("/students")
def get_students():
    """
    Route to fetch all students from the database
    return: Array of student objects
    """
    # TODO: replace with your implementation. This is a mock response

    return jsonify(db.get_all_students()), 200
  #  return jsonify([
  #      {'course': 'COMP1531', 'id': 1, 'mark': 85, 'name': 'Alice Zhang'},
  #      {'course': 'COMP1531', 'id': 2, 'mark': 72, 'name': 'Bob Smith'}
  #  ]), 200


@app.route("/students", methods=["POST"])
def create_student():
    """
    Route to create a new student
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The created student if successful
    """
    # Getting the request body - replace with your implementation
    try:
        student_data = request.json
        s = db.insert_student(student_data["name"], student_data["course"], student_data.get("mark"))
        return jsonify(s), 200
    except Exception as e:
        return str(e), 404



@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """
    Route to update student details by id
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The updated student if successful
    """
    try:
        student_data = request.json
        if db.update_student(student_id, student_data["name"], student_data["course"], student_data.get("mark")) is None:
            return "id not found", 404
        return jsonify(db.get_student_by_id(student_id)), 200
    except Exception as e:
        return str(e) , 404



@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """
    Route to delete student by id
    return: The deleted student
    """
    student_data = db.get_student_by_id(student_id)
    if db.delete_student(student_id) is None:
        return "id not found", 404
    return student_data, 200
    


@app.route("/stats")
def get_stats():
    """
    Route to show the stats of all student marks 
    return: An object with the stats (count, average, min, max)
    """
    try:
        students = db.get_all_students()
        scores = []
        if len(students) == 0:
            return jsonify(
                {
                    "count":0,
                    "average": 0,
                    "min": 0,
                    "max": 0}), 200
            
        for s in students:
            m = s.get("mark")
            if m:
                scores.append(m)
        return jsonify(
                {
                    "count":len(scores), 
                    "average":sum(scores)/len(scores), 
                    "min": min(scores), 
                    "max": max(scores)}), 200

    except Exception as e:
        return (str(e), (404))



@app.route("/")
def health():
    """Health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

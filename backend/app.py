from flask import Flask, jsonify, request, abort, Response
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

    return jsonify(db.get_all_students())
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
    student_data = request.json
    db.insert_student(student_data["name"], student_data["course"], student_data["mark"])
    return Response( response=student_data, status=200)



@app.route("/students/<int:student_id>", methods=["PUT"])
def update_student(student_id):
    """
    Route to update student details by id
    param name: The name of the student (from request body)
    param course: The course the student is enrolled in (from request body)
    param mark: The mark the student received (from request body)
    return: The updated student if successful
    """
    student_data = request.json
    db.update_student(student_id, student_data["name"], student_data["course"], student_data["mark"])
    return db.get_student_by_id(student_id)



@app.route("/students/<int:student_id>", methods=["DELETE"])
def delete_student(student_id):
    """
    Route to delete student by id
    return: The deleted student
    """
    student_data = db.get_student_by_id(student_id)
    db.delete_student(student_id)
    return student_data
    


@app.route("/stats")
def get_stats():
    """
    Route to show the stats of all student marks 
    return: An object with the stats (count, average, min, max)
    """
    try:
        students = db.get_all_students()
        scores = [ s["mark"] for s in students]
        return (len(students), sum(scores)/len(scores), min(scores), max(scores))
    except Exception:
        return abort(404)



@app.route("/")
def health():
    """Health check."""
    return {"status": "ok"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

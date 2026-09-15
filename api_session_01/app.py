# #Bai1
# from flask import Flask
# app = Flask(__name__)
# @app.route("/")
# def index():
#     return {"message": "Hello"}
# if __name__ == "__main__":
#     app.run(host="127.0.0.1", port=5000, debug=True)

# # Bai2
# from flask import Flask, jsonify, request
# app = Flask(__name__)
# # GET /health - kiểm tra tình trạng của server
# @app.route("/health", methods = ["GET"])
# def health():
#     return jsonify({"status": "good"}), 200

# # POST /echo - phản hồi lại client gửi tới
# @app.route("/echo", methods=["POST"])
# def echo():
#     data = request.get_json(silent=True) or {}
#     return jsonify({"you_sent": data}), 200
# if __name__ == "__main__":
#     app.run(host="127.0.0.1", port=5000, debug=True)
    
# # Bài 3
# from flask import Flask, jsonify, request
# from uuid import uuid4
# app = Flask(__name__)
# STUDENTS = []

# @app.route("/students", methods=["POST"])
# def create_student():
#     body = request.get_json(silent=True) or {}
#     name = body.get("name")
#     if not name:
#         return jsonify({"error":"name la bat buoc"}), 400
#     student = {
#         "id": str(uuid4()),
#         "name": name,
#         "gpa": body.get("gpa", 0.0),
#     }
#     STUDENTS.append(student)
#     return student, 201, {"Location":f"/students/{student['id']}"}

# if __name__ == "__main__":
#     app.run(host="127.0.0.1", port=5000, debug=True)

# # Bai 4
# from flask import Flask, jsonify, request
# from uuid import uuid4
# app = Flask(__name__)
# STUDENTS = [
#     {"id": "ab-156", "name": "Nguyen Van A", "gpa": 3.5},
#     {"id": "xy-567", "name": "Tran Thi B", "gpa": 3.8},
#     {"id": "lk-135",   "name": "Le Van Cuong", "gpa": 3.2},
#     {"id": "mn-168",   "name": "Lai Tung Lam", "gpa": 3.9},
#     {"id": "zt-159",   "name": "Hoang Thi Mai", "gpa": 3.6},
#     {"id": "hk-364",   "name": "Dang Van Nam", "gpa": 2.8}
# ]

# def find_by_id(student_id):
#     for s in STUDENTS:
#         if s["id"] == student_id:
#             return s
#     return None


# @app.route("/students/<student_id>", methods=["GET"])
# def get_students(student_id):
#     student = find_by_id(student_id)
#     if student is None:
#         return jsonify({"error": "not found"}), 404
#     return jsonify(student), 200


# @app.route("/students", methods = ["GET"])
# def list_students():
#     limit = int(request.args.get("limit", 20))
#     q = request.args.get("q","").strip().lower()
#     items = [s for s in STUDENTS if q in s["name"].lower()]
#     return jsonify ({"items": items[:limit]}), 200

# if __name__ == "__main__":
#     app.run(host="127.0.0.1", port=5000, debug=True)

# Bai 5
from flask import Flask, jsonify, request
from uuid import uuid4
app = Flask(__name__)
STUDENTS = [
    {"id": "ab-156", "name": "Nguyen Van A", "gpa": 3.5, "status": "active"},
    {"id": "xy-567", "name": "Tran Thi B", "gpa": 3.8, "status": "graduated"},
    {"id": "lk-135", "name": "Le Van Cuong", "gpa": 3.2, "status": "active"},
    {"id": "mn-168", "name": "Lai Tung Lam", "gpa": 3.9, "status": "active"},
    {"id": "zt-159", "name": "Hoang Thi Mai", "gpa": 3.6, "status": "graduated"},
    {"id": "hk-364", "name": "Dang Van Nam", "gpa": 2.8, "status": "active"}
]

def find_by_id(student_id):
    for s in STUDENTS:
        if s["id"] == student_id:
            return s
    return None


@app.route("/students/<student_id>", methods=["GET"])
def get_students(student_id):
    student = find_by_id(student_id)
    if student is None:
        return jsonify({"error": "not found"}), 404
    return jsonify(student), 200


@app.route("/students", methods = ["GET"])
def list_students():
    limit = int(request.args.get("limit", 20))
    q = request.args.get("q","").strip().lower()
    items = [s for s in STUDENTS if q in s["name"].lower()]
    return jsonify ({"items": items[:limit]}), 200

@app.route("/students/<student_id>", methods=["DELETE"])
def delete_student(student_id):
    student = find_by_id(student_id)
    if student is None:
        return jsonify({"error": "not found"}), 404
    if student.get("status") == "graduated":
        return jsonify({"error": "cannot delete"}), 409
    STUDENTS.remove(student)
    return "", 204

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

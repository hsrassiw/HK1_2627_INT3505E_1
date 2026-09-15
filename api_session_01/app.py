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
    
# Bài 3
from flask import Flask, jsonify, request
from uuid import uuid4
app = Flask(__name__)
STUDENTS = []

@app.route("/students", methods=["POST"])
def create_student():
    body = request.get_json(silent=True) or {}
    name = body.get("name")
    if not name:
        return jsonify({"error":"name la bat buoc"}), 400
    student = {
        "id": str(uuid4()),
        "name": name,
        "gpa": body.get("gpa", 0.0),
    }
    STUDENTS.append(student)
    return student, 201, {"Location":f"/students/{student['id']}"}

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)

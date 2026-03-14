from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from models import db, Task

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route("/")
def home():
    return render_template("index.html")


# READ
@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])


# CREATE
@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.json

    if not data or not data.get("title"):
        return jsonify({"error": "Title is required"}), 400

    task = Task(
        title=data["title"],
        description=data.get("description", ""),
        status=data.get("status", "pending")
    )

    db.session.add(task)
    db.session.commit()

    return jsonify(task.to_dict()), 201


# UPDATE
@app.route("/tasks/<int:id>", methods=["PUT"])
def update_task(id):

    task = Task.query.get(id)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    data = request.json

    task.title = data.get("title", task.title)
    task.description = data.get("description", task.description)
    task.status = data.get("status", task.status)

    db.session.commit()

    return jsonify(task.to_dict())


# DELETE
@app.route("/tasks/<int:id>", methods=["DELETE"])
def delete_task(id):

    task = Task.query.get(id)

    if not task:
        return jsonify({"error": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({"message": "Task deleted"})


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
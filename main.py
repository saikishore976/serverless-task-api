import functions_framework
from flask import jsonify, request
from google.cloud import firestore

# Firestore client
db = firestore.Client()
collection_name = "tasks"

# API Function
@functions_framework.http
def tasks_api(request):
    request_json = request.get_json(silent=True)
    request_args = request.args
    method = request.method

    # Create Task
    if method == "POST":
        if not request_json or "title" not in request_json:
            return jsonify({"error": "Title is required"}), 400
        new_task = {"title": request_json["title"], "done": False}
        db.collection(collection_name).add(new_task)
        return jsonify({"message": "Task created"}), 201

    # Get All Tasks
    if method == "GET":
        tasks = []
        docs = db.collection(collection_name).stream()
        for doc in docs:
            task = doc.to_dict()
            task["id"] = doc.id
            tasks.append(task)
        return jsonify(tasks), 200

    # Update Task
    if method == "PUT":
        if not request_json or "id" not in request_json:
            return jsonify({"error": "Task ID is required"}), 400
        task_ref = db.collection(collection_name).document(request_json["id"])
        task_ref.update({"done": request_json.get("done", True)})
        return jsonify({"message": "Task updated"}), 200

    # Delete Task
    if method == "DELETE":
        if not request_json or "id" not in request_json:
            return jsonify({"error": "Task ID is required"}), 400
        db.collection(collection_name).document(request_json["id"]).delete()
        return jsonify({"message": "Task deleted"}), 200

    return jsonify({"error": "Unsupported method"}), 405

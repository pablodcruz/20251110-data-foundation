# Flask is a micro web framework for Python, used for building web applications and APIs
# https://flask.palletsprojects.com/en/stable/quickstart/

from flask import Flask, request, jsonify
from service import TodoService
from repo import init_db

app = Flask(__name__)
svc = TodoService()

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/todos")
def create_todo():
    data = request.get_json(force=True) or {}
    title = (data.get("title") or "").strip()
    description = data.get("description")
    try:
        todo = svc.create(title, description)
        return jsonify(todo.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

@app.get("/todos")
def list_todos():
    is_done = request.args.get("is_done")
    q = request.args.get("q")
    limit = int(request.args.get("limit", 50))
    offset = int(request.args.get("offset", 0))
    todos = svc.list(is_done=is_done, q=q, limit=limit, offset=offset)
    return jsonify([t.to_dict() for t in todos])

@app.get("/todos/<int:todo_id>")
def get_todo(todo_id):
    try:
        todo = svc.get(todo_id)
        return jsonify(todo.to_dict())
    except ValueError:
        return jsonify({"error": "todo not found"}), 404

@app.patch("/todos/<int:todo_id>/done")
def mark_done(todo_id):
    try:
        todo = svc.mark_done(todo_id)
        return jsonify(todo.to_dict())
    except ValueError:
        return jsonify({"error": "todo not found"}), 404

@app.put("/todos/<int:todo_id>")
def update_todo(todo_id):
    data = request.get_json(force=True) or {}
    try:
        todo = svc.update(
            todo_id,
            title=data.get("title"),
            description=data.get("description"),
            is_done=data.get("is_done"),
        )
        return jsonify(todo.to_dict())
    except ValueError as e:
        msg = str(e)
        return jsonify({"error": msg}), 404 if "not found" in msg else 400

@app.delete("/todos/<int:todo_id>")
def delete_todo(todo_id):
    try:
        svc.delete(todo_id)
        return "", 204
    except ValueError:
        return jsonify({"error": "todo not found"}), 404

if __name__ == "__main__":
    init_db()                # create table if missing
    app.run(host="127.0.0.1", port=8000, debug=True)

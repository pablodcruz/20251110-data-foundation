from domain import Todo
from repo import TodoRepo

class TodoService:
    # The service depends on an abstract "repo" behavior (here: concrete class)
    def __init__(self, repo=None):
        self.repo = repo or TodoRepo()

    def create(self, title, description=None):
        todo = Todo(id=None, title=title, description=description)
        return self.repo.create(todo)

    def get(self, todo_id):
        todo = self.repo.get(todo_id)
        if not todo:
            raise ValueError("todo not found")
        return todo

    def list(self, is_done=None, q=None, limit=50, offset=0):
        return self.repo.list(is_done=is_done, q=q, limit=limit, offset=offset)

    def mark_done(self, todo_id):
        todo = self.get(todo_id)
        todo.mark_done()
        return self.repo.update(todo)

    def update(self, todo_id, title=None, description=None, is_done=None):
        todo = self.get(todo_id)
        if title is not None:
            todo.rename(title)
        if description is not None:
            todo.describe(description)
        if is_done is not None:
            todo.is_done = bool(is_done)
            todo.touch()
        return self.repo.update(todo)

    def delete(self, todo_id):
        ok = self.repo.delete(todo_id)
        if not ok:
            raise ValueError("todo not found")

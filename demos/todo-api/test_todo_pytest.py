"""
Tests for Todo and TodoService using pytest.

This file mirrors the unittest example, but shows:

- pytest's function-based tests
- Fixtures instead of setUp()
- Cleaner assertions (no self.assertEqual, just assert)

This shows the difference in style between unittest and pytest.
"""

import pytest
from datetime import datetime, timezone

from domain import Todo
from service import TodoService


class FakeTodoRepo:
    """
    Same FakeTodoRepo as in the unittest example.

    In pytest, we'll inject this into tests using fixtures.
    """

    def __init__(self):
        self._store = {}
        self._next_id = 1

    def create(self, todo):
        todo.id = self._next_id
        self._next_id += 1
        self._store[todo.id] = todo
        return todo

    def get(self, todo_id):
        return self._store.get(todo_id)

    def list(self, is_done=None, q=None, limit=50, offset=0):
        todos = list(self._store.values())

        if is_done is not None:
            todos = [t for t in todos if t.is_done == bool(is_done)]

        if q:
            q_lower = q.lower()
            todos = [
                t
                for t in todos
                if q_lower in (t.title or "").lower()
                or q_lower in (t.description or "").lower()
            ]

        return todos[offset : offset + limit]

    def update(self, todo):
        if todo.id not in self._store:
            return None
        self._store[todo.id] = todo
        return todo

    def delete(self, todo_id):
        if todo_id in self._store:
            del self._store[todo_id]
            return True
        return False


# ---------- pytest fixtures ----------

@pytest.fixture
def repo():
    """
    Provides a fresh FakeTodoRepo to each test that needs it.
    """
    return FakeTodoRepo()


@pytest.fixture
def service(repo):
    """
    Provides a TodoService that uses the FakeTodoRepo.

    This is a good illustration of DI (dependency injection):
    we're injecting the repo dependency into the service.
    """
    return TodoService(repo=repo)


# ---------- Domain tests ----------

def test_todo_initialization_sets_fields():
    todo = Todo(
        id=None,
        title="  Buy milk  ",
        description="2% gallon",
        is_done=False,
    )

    assert todo.title == "Buy milk"
    assert todo.description == "2% gallon"
    assert todo.is_done is False
    assert isinstance(todo.created_at, datetime)
    assert isinstance(todo.updated_at, datetime)


def test_mark_done_sets_flag_and_updates_timestamp():
    todo = Todo(id=1, title="Test", description=None, is_done=False)
    before = todo.updated_at

    todo.mark_done()

    assert todo.is_done is True
    assert todo.updated_at >= before


def test_rename_raises_for_empty_title():
    todo = Todo(id=1, title="Old", description=None)

    # Happy path
    todo.rename("New title")
    assert todo.title == "New title"

    # Error case: too short after strip
    # TODO: provide comments
    with pytest.raises(ValueError):
        todo.rename("   ")


# ---------- Service tests ----------

def test_service_create_persists_and_assigns_id(service, repo):
    """
    With pytest, dependencies are simply function parameters that match fixtures.
    """
    todo = service.create("Buy eggs", "Free range")

    assert todo.id is not None
    assert todo.title == "Buy eggs"
    assert todo.description == "Free range"

    # Verify it is in the fake repo
    stored = repo.get(todo.id)
    assert stored is not None
    assert stored.title == "Buy eggs"


def test_service_get_raises_for_missing_id(service):
    with pytest.raises(ValueError):
        service.get(999)


def test_service_mark_done_updates_repo(service, repo):
    created = service.create("Wash car", None)
    todo_id = created.id

    updated = service.mark_done(todo_id)

    assert updated.is_done is True
    # Ensure repo reflects change
    assert repo.get(todo_id).is_done is True


def test_service_update_changes_title_and_description(service):
    created = service.create("Old title", "Old description")

    updated = service.update(
        todo_id=created.id,
        title="New title",
        description="New description",
        is_done=None,
    )

    assert updated.title == "New title"
    assert updated.description == "New description"


def test_service_delete_removes_todo_or_raises(service, repo):
    created = service.create("Temp", None)
    todo_id = created.id

    # First delete should succeed
    service.delete(todo_id)
    assert repo.get(todo_id) is None

    # Second delete should raise ValueError
    with pytest.raises(ValueError):
        service.delete(todo_id)

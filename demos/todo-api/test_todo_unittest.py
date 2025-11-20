"""
Tests for the Todo domain model and TodoService using Python's built-in unittest.

We intentionally DO NOT hit the real Postgres database here.
Instead, we use a FakeTodoRepo that stores todos in memory (a dict).

This shows students:
- How to test business logic in isolation
- Why the repository pattern + dependency injection makes testing easier
"""

import unittest
from datetime import datetime, timezone

from domain import Todo
from service import TodoService


class FakeTodoRepo:
    """
    In-memory "fake" repository used only for tests.

    It implements the same methods as TodoRepo, but instead of running SQL,
    it stores Todo objects in a Python dict.

    This is a classic pattern:
      - Real code in production uses TodoRepo (Postgres).
      - Tests swap in FakeTodoRepo to run fast and deterministically.
    """

    def __init__(self):
        self._store = {}
        self._next_id = 1

    def create(self, todo):
        # Simulate auto-increment id behavior from the database.
        todo.id = self._next_id
        self._next_id += 1
        self._store[todo.id] = todo
        return todo

    def get(self, todo_id):
        # Return the Todo or None if it doesn't exist.
        return self._store.get(todo_id)

    def list(self, is_done=None, q=None, limit=50, offset=0):
        # Very simple implementation: return all todos, ignoring filters for now.
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

        # Simulate limit/offset
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


class TestTodoDomain(unittest.TestCase):
    """
    Unit tests for the Todo domain object itself.

    Here we test:
    - validation
    - behavior methods like mark_done(), rename(), etc.
    """

    def test_todo_initialization_sets_fields(self):
        todo = Todo(
            id=None,
            title="  Buy milk  ",
            description="2% gallon",
            is_done=False,
        )

        # Title should be stripped
        self.assertEqual(todo.title, "Buy milk")
        self.assertEqual(todo.description, "2% gallon")
        self.assertFalse(todo.is_done)
        self.assertIsInstance(todo.created_at, datetime)
        self.assertIsInstance(todo.updated_at, datetime)
        

    def test_mark_done_sets_flag_and_updates_timestamp(self):
        # Arrange 
        todo = Todo(id=1, title="Test", description=None, is_done=False)
        before = todo.updated_at

        # Act
        todo.mark_done()
        
        # Assert
        self.assertTrue(todo.is_done)
        self.assertGreaterEqual(todo.updated_at, before)

    def test_rename_validates_title_length(self):
        todo = Todo(id=1, title="Old", description=None)

        todo.rename("New title")
        self.assertEqual(todo.title, "New title")

        # Very short / empty title should raise ValueError (see domain.py logic)
        # This test verifies error handling behavior — specifically, that the service raises a ValueError when someone tries to retrieve a todo that does NOT exist.
        with self.assertRaises(ValueError):
            todo.rename("  ")  # too short after strip


class TestTodoService(unittest.TestCase):
    """
    Unit tests for TodoService using a FakeTodoRepo.

    This makes it very clear that:
    - Service = business logic (use-cases)
    - Repo    = data access (here, faked)
    """

    def setUp(self):
        # setUp runs before each test method.
        self.repo = FakeTodoRepo()
        self.service = TodoService(repo=self.repo)

    def test_create_persists_todo_and_assigns_id(self):
        """
        Given a title and description,
        when we call service.create(...),
        then a Todo is created, assigned an id, and stored in the repo.
        """
        todo = self.service.create("Buy eggs", "Free range")

        self.assertIsNotNone(todo.id)
        self.assertEqual(todo.title, "Buy eggs")
        self.assertEqual(todo.description, "Free range")

        # Ensure the repo actually stored it.
        stored = self.repo.get(todo.id)
        self.assertIsNotNone(stored)
        self.assertEqual(stored.title, "Buy eggs")

    def test_get_raises_value_error_if_not_found(self):
        """
        Service.get() wraps repo.get()
        and converts 'not found' into a ValueError.
        """
        with self.assertRaises(ValueError):
            self.service.get(999)  # no such id

    def test_mark_done_updates_todo(self):
        """
        Given an existing Todo,
        when we call mark_done(id),
        then is_done should become True.
        """
        created = self.service.create("Wash car", None)
        todo_id = created.id

        updated = self.service.mark_done(todo_id)

        self.assertTrue(updated.is_done)
        # Also check that the repo has the updated object
        stored = self.repo.get(todo_id)
        self.assertTrue(stored.is_done)

    def test_update_can_change_title_and_description(self):
        """
        Service.update should pass through changes to the domain object
        and then back to the repo.
        """
        created = self.service.create("Old title", "Old description")

        updated = self.service.update(
            todo_id=created.id,
            title="New title",
            description="New description",
            is_done=None,  # unchanged
        )

        self.assertEqual(updated.title, "New title")
        self.assertEqual(updated.description, "New description")

    def test_delete_removes_todo_or_raises(self):
        """
        delete(todo_id) should remove the todo from the repo.
        If id does not exist, it should raise ValueError.
        """
        created = self.service.create("Temp", None)
        todo_id = created.id

        # First call should succeed.
        self.service.delete(todo_id)
        self.assertIsNone(self.repo.get(todo_id))

        # Second call should raise because it's already gone.
        with self.assertRaises(ValueError):
            self.service.delete(todo_id)


if __name__ == "__main__":
    # Allows: python test_todo_unittest.py
    unittest.main()

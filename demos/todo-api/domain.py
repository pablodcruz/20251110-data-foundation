# Domain model: holds data + behavior (encapsulation)
# Consider making some attributes private and creating getters and setters

from datetime import datetime, timezone

class Todo:
    def __init__(self, id, title, description=None, is_done=False, created_at=None, updated_at=None):
        if not (1 <= len(title.strip()) <= 120):
            raise ValueError("title must be 1..120 characters")
        self.id = id
        self.title = title.strip()
        self.description = description
        self.is_done = bool(is_done)
        self.created_at = created_at or datetime.now(timezone.utc)
        self.updated_at = updated_at or datetime.now(timezone.utc)

    # ---- Behavior (business rules) ----
    def rename(self, title):
        title = (title or "").strip()
        if not (1 <= len(title) <= 120):
            raise ValueError("title must be 1..120 characters")
        self.title = title
        self.touch()

    def describe(self, text):
        self.description = text
        self.touch()

    def mark_done(self):
        self.is_done = True
        self.touch()

    def touch(self):
        self.updated_at = datetime.now(timezone.utc)

    # ---- Mapping helpers (domain <-> persistence) ----
    @classmethod
    def from_row(cls, row):
        # row can be a dict from RealDictCursor
        return cls(
            id=row.get("id"),
            title=row.get("title"),
            description=row.get("description"),
            is_done=row.get("is_done"),
            created_at=row.get("created_at"),
            updated_at=row.get("updated_at"),
        )

    def to_dict(self):
        # clean JSON shape for the API
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "is_done": self.is_done,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

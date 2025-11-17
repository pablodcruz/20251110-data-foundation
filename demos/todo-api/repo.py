# 🗄️ repo.py (Repository = DB adapter; hides SQL from the rest)

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from domain import Todo

DB_NAME = os.getenv("PGDB", "todo_db")
DB_USER = os.getenv("PGUSER", "postgres")
DB_PASS = os.getenv("PGPASS", "final2kk")  # your postgres password for this user
DB_HOST = os.getenv("PGHOST", "127.0.0.1") # 127.0.0.1 is localhost
DB_PORT = int(os.getenv("PGPORT", "5432")) # 5432 is the default port for postgres dbs

#
def get_conn():
    return psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST, port=DB_PORT
    )

def init_db():
    # one-time schema init (safe to re-run)
    with get_conn() as conn, conn.cursor() as cur:
        with open("schema.sql", "r", encoding="utf-8") as f:
            cur.execute(f.read())
        conn.commit()

class TodoRepo:
    # CRUD using SQL; returns/accepts Todo domain objects

    def create(self, todo):
        sql = """
        INSERT INTO todos (title, description, is_done, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s) 
        RETURNING id, title, description, is_done, created_at, updated_at
        """
        with get_conn() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, (todo.title, todo.description, todo.is_done, todo.created_at, todo.updated_at))
            row = cur.fetchone()
            conn.commit()
            return Todo.from_row(row)

    def get(self, todo_id):
        with get_conn() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("""
                SELECT id, title, description, is_done, created_at, updated_at
                FROM todos WHERE id = %s
            """, (todo_id,))
            row = cur.fetchone()
            if not row:
                return None
            return Todo.from_row(row)

    def list(self, is_done=None, q=None, limit=50, offset=0):
        clauses, params = [], []
        if is_done is not None:
            clauses.append("is_done = %s")
            params.append(bool(str(is_done).lower() in ("1","true","t","yes","y")))
        if q:
            clauses.append("(title ILIKE %s OR description ILIKE %s)")
            params.extend([f"%{q}%", f"%{q}%"])
        where = (" WHERE " + " AND ".join(clauses)) if clauses else ""
        sql = f"""
            SELECT id, title, description, is_done, created_at, updated_at
            FROM todos
            {where}
            ORDER BY created_at DESC
            LIMIT %s OFFSET %s
        """
        params.extend([limit, offset])
        with get_conn() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, tuple(params))
            rows = cur.fetchall()
            return [Todo.from_row(r) for r in rows]

    def update(self, todo):
        sql = """
        UPDATE todos
        SET title=%s, description=%s, is_done=%s, updated_at=now()
        WHERE id=%s
        RETURNING id, title, description, is_done, created_at, updated_at
        """
        with get_conn() as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, (todo.title, todo.description, todo.is_done, todo.id))
            row = cur.fetchone()
            if not row:
                return None
            conn.commit()
            return Todo.from_row(row)

    def delete(self, todo_id):
        with get_conn() as conn, conn.cursor() as cur:
            cur.execute("DELETE FROM todos WHERE id = %s", (todo_id,))
            deleted = cur.rowcount
            conn.commit()
            return deleted > 0

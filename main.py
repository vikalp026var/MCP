from fastmcp import FastMCP
import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")

mcp = FastMCP(name="Expense Tracker")


def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                subcategory TEXT DEFAULT NULL,
                note TEXT DEFAULT NULL
            )
            """
        )


init_db()


@mcp.tool
def add_expense(
    date: str,
    amount: float,
    category: str,
    subcategory: str | None = None,
    note: str | None = None,
):
    """Add a new expense to the database."""
    with sqlite3.connect(DB_PATH) as conn:
        curr = conn.execute(
            """
            INSERT INTO expenses (date, amount, category, subcategory, note)
            VALUES (?, ?, ?, ?, ?)
            """,
            (date, amount, category, subcategory, note),
        )

        return {
            "status": "ok",
            "id": curr.lastrowid,
        }


@mcp.tool
def list_expenses():
    """List all expenses in the database."""
    with sqlite3.connect(DB_PATH) as conn:
        curr = conn.execute(
            """
            SELECT id, date, amount, category, subcategory, note
            FROM expenses
            ORDER BY id ASC
            """
        )
        cols = [col[0] for col in curr.description]
        return [dict(zip(cols, row)) for row in curr.fetchall()]


@mcp.tool
def summarize_expenses(start_date: str, end_date: str):
    """Summarize expenses between two dates"""
    with sqlite3.connect(DB_PATH) as conn:
        curr = conn.execute(
            """
            SELECT SUM(amount) FROM expenses WHERE date BETWEEN ? AND ?
            """,
            (start_date, end_date)
        )
        return {
            "total": curr.fetchone()[0],
        }

if __name__ == "__main__":
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=8000,
    )
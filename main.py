from fastmcp import FastMCP
import os
import asyncio
import aiosqlite

DB_PATH = os.path.join(os.path.dirname(__file__), "expenses.db")

mcp = FastMCP(name="Expense Tracker")


async def init_db():
    async with aiosqlite.connect(DB_PATH) as conn:  # fix: async with, not with
        await conn.execute(
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
        await conn.commit()  # fix: commit the CREATE TABLE


@mcp.tool
async def add_expense(
    date: str,
    amount: float,
    category: str,
    subcategory: str | None = None,
    note: str | None = None,
):
    """Add a new expense to the database."""
    async with aiosqlite.connect(DB_PATH) as conn:  # fix: async with, not with
        curr = await conn.execute(  # fix: await the execute call
            """
            INSERT INTO expenses (date, amount, category, subcategory, note)
            VALUES (?, ?, ?, ?, ?)
            """,
            (date, amount, category, subcategory, note),
        )
        await conn.commit()  # fix: commit the INSERT

        return {
            "status": "ok",
            "id": curr.lastrowid,
        }


@mcp.tool
async def list_expenses():
    """List all expenses in the database."""
    async with aiosqlite.connect(DB_PATH) as conn:  # fix: async with + aiosqlite (was sqlite3)
        curr = await conn.execute(  # fix: await + closing paren was missing
            """
            SELECT id, date, amount, category, subcategory, note
            FROM expenses
            ORDER BY id ASC
            """
        )
        rows = await curr.fetchall()  # fix: was missing entirely — cut off mid-function
        return [
            {
                "id": row[0],
                "date": row[1],
                "amount": row[2],
                "category": row[3],
                "subcategory": row[4],
                "note": row[5],
            }
            for row in rows
        ]


@mcp.tool
async def summarize_expenses(start_date: str, end_date: str):  # fix: was merged into list_expenses
    """Summarize expenses between two dates."""
    async with aiosqlite.connect(DB_PATH) as conn:  # fix: async with
        curr = await conn.execute(
            """
            SELECT SUM(amount) FROM expenses WHERE date BETWEEN ? AND ?
            """,
            (start_date, end_date),
        )
        return {
            "total": (await curr.fetchone())[0],
        }


async def main():  # fix: can't call `await` at module top-level; wrap in main()
    await init_db()
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=8000,
    )  # fix: removed asyncio_loop= (not a valid FastMCP.run() parameter)


if __name__ == "__main__":
    asyncio.run(main())
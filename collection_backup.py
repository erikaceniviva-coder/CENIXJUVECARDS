import sqlite3
from pathlib import Path

DB = Path(__file__).parent / "collection.db"

def connect():
    return sqlite3.connect(DB)

def initialize():
    with connect() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS collection (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                slug TEXT NOT NULL,
                name TEXT NOT NULL,
                rarity TEXT NOT NULL,
                rating INTEGER NOT NULL,
                quantity INTEGER DEFAULT 1,
                acquired_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(slug, rarity)
            )
        """)

def add_card(card):
    initialize()
    with connect() as db:
        db.execute("""
            INSERT INTO collection (slug, name, rarity, rating)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(slug, rarity)
            DO UPDATE SET quantity = quantity + 1
        """, (
            card["slug"],
            card["name"],
            card["rarity"],
            card["rating"]
        ))

def get_collection():
    initialize()
    with connect() as db:
        rows = db.execute("""
            SELECT slug, name, rarity, rating, quantity
            FROM collection
            ORDER BY
                CASE rarity
                    WHEN 'LEGENDARY' THEN 1
                    WHEN 'EPIC' THEN 2
                    WHEN 'RARE' THEN 3
                    ELSE 4
                END,
                name
        """).fetchall()

    return [
        {
            "slug": r[0],
            "name": r[1],
            "rarity": r[2],
            "rating": r[3],
            "quantity": r[4]
        }
        for r in rows
    ]

initialize()

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
                collection_type TEXT NOT NULL DEFAULT 'JUVE',
                UNIQUE(slug, rarity, collection_type)
            )
        """)

        columns = [
            row[1] for row in db.execute(
                "PRAGMA table_info(collection)"
            ).fetchall()
        ]

        if "collection_type" not in columns:
            db.execute("""
                ALTER TABLE collection
                ADD COLUMN collection_type TEXT NOT NULL DEFAULT 'LEGENDS'
            """)

        indexes = db.execute(
            "PRAGMA index_list(collection)"
        ).fetchall()

        old_unique = False

        for index in indexes:
            if index[2]:
                info = db.execute(
                    f'PRAGMA index_info("{index[1]}")'
                ).fetchall()

                fields = [row[2] for row in info]

                if fields == ["slug", "rarity"]:
                    old_unique = True

        if old_unique:
            db.execute("""
                CREATE TABLE collection_new (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    slug TEXT NOT NULL,
                    name TEXT NOT NULL,
                    rarity TEXT NOT NULL,
                    rating INTEGER NOT NULL,
                    quantity INTEGER DEFAULT 1,
                    acquired_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    collection_type TEXT NOT NULL DEFAULT 'JUVE',
                    UNIQUE(slug, rarity, collection_type)
                )
            """)

            db.execute("""
                INSERT INTO collection_new
                (id, slug, name, rarity, rating, quantity,
                 acquired_at, collection_type)
                SELECT id, slug, name, rarity, rating, quantity,
                       acquired_at, collection_type
                FROM collection
            """)

            db.execute("DROP TABLE collection")
            db.execute(
                "ALTER TABLE collection_new RENAME TO collection"
            )


def add_card(card):
    initialize()

    with connect() as db:
        db.execute("""
            INSERT INTO collection
            (slug, name, rarity, rating, collection_type)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(slug, rarity, collection_type)
            DO UPDATE SET quantity = quantity + 1
        """, (
            card["slug"],
            card["name"],
            card["rarity"],
            card["rating"],
            card.get("collection_type", "JUVE")
        ))


def get_collection():
    initialize()

    with connect() as db:
        rows = db.execute("""
            SELECT slug, name, rarity, rating,
                   quantity, collection_type
            FROM collection
            ORDER BY collection_type, name
        """).fetchall()

    return [
        {
            "slug": r[0],
            "name": r[1],
            "rarity": r[2],
            "rating": r[3],
            "quantity": r[4],
            "collection_type": r[5]
        }
        for r in rows
    ]


initialize()

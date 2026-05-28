import sqlite3
from dataclasses import fields, asdict
from src.core.models.domain_model import AnimeDataModel
from src.core.models.protocols import TransformerProtocol


class LoadToSQLite:
    MODEL_FIELDS = [f.name for f in fields(AnimeDataModel)]
    COLUMNS = ", ".join(MODEL_FIELDS)
    PLACEHOLDER = ", ".join("?" * len(MODEL_FIELDS))

    def __init__(self, transformer: TransformerProtocol) -> None:
        self.transformer = transformer

    async def load_data(self, start_year: int, end_year: int) -> None:
        with sqlite3.connect("database/data.db") as conn:
            cur = conn.cursor()
            self._ensure_table_exists(cur)
            async for data in self.transformer.get_transformed_data(
                start_year, end_year
            ):
                self._insert_data(cur, data)

    def _insert_data(self, cursor: sqlite3.Cursor, data: AnimeDataModel) -> None:
        cursor.execute(
            f"""
            INSERT INTO anime ({self.COLUMNS})
            VALUES ({self.PLACEHOLDER})
            """,
            self._unpack_data(data),
        )

    def _ensure_table_exists(self, cursor: sqlite3.Cursor) -> None:
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS anime (
                           id INTEGER PRIMARY KEY AUTOINCREMENT,
                           id_anilist INTEGER,
                           id_mal INTEGER,
                           romaji_title TEXT NOT NULL,
                           english_title TEXT,
                           native_title TEXT,
                           preferred_title TEXT,
                           type TEXT,
                           format TEXT,
                           description TEXT,
                           start_date TEXT,
                           end_date TEXT,
                           season TEXT,
                           season_year INTEGER,
                           episodes INTEGER,
                           duration INTEGER,
                           country_of_origin TEXT,
                           source TEXT,
                           hashtag TEXT,
                           updated_at TEXT,
                           genres TEXT,
                           synonyms TEXT,
                           average_score INTEGER,
                           mean_score INTEGER,
                           popularity INTEGER,
                           trending INTEGER,
                           favourites INTEGER,
                           animation_studio TEXT
                       )
                       """)

    def _unpack_data(self, data: AnimeDataModel) -> tuple[str | int | None, ...]:
        return tuple(asdict(data).values())

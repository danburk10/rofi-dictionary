# providers/sqlite_provider.py

import sqlite3

from models.dictionary_entry import DictionaryEntry
from providers.base import DictionaryProvider


class SqliteProvider(DictionaryProvider):

    def __init__(self, database: str):
        self.database = database

    def get_entry(self, word: str) -> DictionaryEntry | None:
        with sqlite3.connect(self.database) as conn:
            conn.row_factory = sqlite3.Row

            row = conn.execute(
                """
                SELECT
                    word,
                    definition,
                    part_of_speech,
                    phonetic,
                    example
                FROM dictionary
                WHERE lower(word) = lower(?)
                """,
                (word,)
            ).fetchone()

        if row is None:
            return None

        return DictionaryEntry(
            word=row["word"],
            definition=row["definition"],
            part_of_speech=row["part_of_speech"],
            phonetic=row["phonetic"],
            example=row["example"],
            source="sqlite"
        )

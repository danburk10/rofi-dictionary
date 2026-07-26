# providers/sqlite_provider.py

import sqlite3

from models.dictionary_entry import WordEntry
#from providers.base import DictionaryProvider


class SqliteProvider():

    def __init__(self, database: str):
        self.database = "data/dictionary.db"


    def get_entry(self, word: str) -> WordEntry | None:
        sql = """
            SELECT
                id,
                word,
                part_of_speech,
                definition,
                examples,
                synonyms,
                pronunciation,
                synset_id
            FROM dictionary
            WHERE LOWER(word) = lower(?)
            ORDER BY part_of_speech, id;
        """


        with sqlite3.connect(self.database) as conn:
            conn.row_factory = sqlite3.Row

            rows = conn.execute(sql, (word,)).fetchall()

        if rows is None:
            return None

        """
        return WordEntry(
            word=row["word"],
            definitions=row["definition"],
            part_of_speech=row["part_of_speech"],
            source="sqlite"
        )
        (definition: str, 
        part_of_speech: str, 
        examples: list[str], 
        synonyms: list[str], 
        antonyms: list[str], **kwargs: Any) -> None

        """
        entry = WordEntry(word)
        for r in rows:
            entry.add_definition(r["definition"],
                                 r["part_of_speech"],
                                 r["examples"],
                                 r["synonyms"],
                                 None)
        
        return entry
        """
        for r in rows:
            entry.add_definition()
            results.append({
                "id": r["id"],
                "word": r["word"],
                "part_of_speech": r["part_of_speech"],
                "definition": r["definition"],
                "examples": load_json_maybe(r["examples"]),
                "synonyms": load_json_maybe(r["synonyms"]),
                "pronunciation": load_json_maybe(r["pronunciation"]),
                "synset_id": r["synset_id"],
            })
        """


        """
        return WordEntry(
            word=row["word"],
            definitions=row["definition"],
            source="sqlite"
        )
        """

    

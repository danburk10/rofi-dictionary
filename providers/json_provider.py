# providers/json_provider.py

import json

from models.dictionary_entry import DictionaryEntry
from providers.base import DictionaryProvider


class JsonProvider(DictionaryProvider):

    def __init__(self, file_path: str):
        self.file_path = file_path

    def get_entry(self, word: str) -> DictionaryEntry | None:
        with open(self.file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        item = data.get(word.lower())

        if item is None:
            return None

        return DictionaryEntry(
            word=item.get("word", word),
            definition=item.get("definition", ""),
            part_of_speech=item.get("part_of_speech"),
            phonetic=item.get("phonetic"),
            example=item.get("example"),
            synonyms=item.get("synonyms", []),
            source="json"
        )

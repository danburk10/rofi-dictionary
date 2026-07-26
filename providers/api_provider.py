# providers/api_provider.py
"""
import requests

from models.dictionary_entry import DictionaryEntry
from providers.base import DictionaryProvider


class ApiProvider(DictionaryProvider):

    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip("/")

    def get_entry(self, word: str) -> DictionaryEntry | None:
        response = requests.get(
            f"{self.base_url}/api/v2/entries/en/{word}",
            timeout=10
        )

        if response.status_code != 200:
            return None

        data = response.json()

        if not data:
            return None

        item = data[0]
        meaning = item.get("meanings", [{}])[0]
        definition_item = meaning.get("definitions", [{}])[0]

        return DictionaryEntry(
            word=item.get("word", word),
            phonetic=item.get("phonetic"),
            part_of_speech=meaning.get("partOfSpeech"),
            definition=definition_item.get("definition", ""),
            example=definition_item.get("example"),
            synonyms=definition_item.get("synonyms", []),
            source="api"
        )
 """
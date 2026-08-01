# services/dictionary_service.py

from models.dictionary_entry import WordEntry
from providers.base import DictionaryProvider


class DictionaryService:

    def __init__(self, provider: DictionaryProvider):
        self.provider = provider

    def lookup(self, word: str) -> WordEntry | None:
        cleaned_word = word.strip()

        if not cleaned_word:
            return None

        return self.provider.get_entry(cleaned_word)

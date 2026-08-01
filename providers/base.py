# providers/base.py

from abc import ABC, abstractmethod
from models.dictionary_entry import WordEntry


class DictionaryProvider(ABC):

    @abstractmethod
    def get_entry(self, word: str) -> WordEntry | None:
        pass
